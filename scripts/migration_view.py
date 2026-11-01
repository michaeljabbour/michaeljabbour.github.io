"""Render the small maintained migration guide without runtime dependencies."""
from html import escape
import json,re,shutil
from urllib.parse import urlsplit
from catalogue_admission import validate_historical_migration

def inline(text):
    pieces=re.split(r'(`[^`]+`|\[[^\]]+\]\([^)]+\))',text);out=[]
    for part in pieces:
        if part.startswith('`') and part.endswith('`'):out.append('<code>'+escape(part[1:-1])+'</code>')
        elif (match:=re.fullmatch(r'\[([^\]]+)\]\(([^)]+)\)',part)):
            label,url=match.groups();parsed=urlsplit(url)
            if not ((parsed.scheme=='https' and parsed.netloc) or url=='mapping.json'):raise ValueError('Unsupported migration link')
            out.append('<a href="'+escape(url,quote=True)+'"'+(' download' if url=='mapping.json' else '')+'>'+escape(label)+'</a>')
        else:out.append(escape(part))
    return ''.join(out)

def markdown_body(source):
    out=[];paragraph=[];code=None;table=False
    def flush():
        if paragraph:out.append('<p>'+inline(' '.join(paragraph))+'</p>');paragraph.clear()
    for line in source.splitlines()+['']:
        if line.startswith('```'):
            flush()
            if code is None:code=[]
            else:out.append('<pre tabindex="0"><code>'+escape('\n'.join(code))+'</code></pre>');code=None
            continue
        if code is not None:code.append(line);continue
        if line.startswith('|'):
            flush();cells=[x.strip() for x in line.strip().strip('|').split('|')]
            if all(re.fullmatch(r'[-: ]+',cell) for cell in cells):continue
            if not table:out.append('<div class="migration-table" role="region" aria-label="Repository migration table" tabindex="0"><table><thead>');table=True;tag='th'
            else:tag='td'
            out.append('<tr>'+''.join('<'+tag+'>'+inline(cell)+'</'+tag+'>' for cell in cells)+'</tr>')
            if tag=='th':out.append('</thead><tbody>')
            continue
        if table:out.append('</tbody></table></div>');table=False
        if not line.strip():flush()
        elif (heading:=re.match(r'^(#{1,3}) (.+)$',line)):
            flush();level=str(len(heading[1]));out.append('<h'+level+'>'+inline(heading[2])+'</h'+level+'>')
        else:paragraph.append(line.strip())
    if code is not None:raise ValueError('Unclosed migration code block')
    return '<article class="wrap migration-guide"><a class="back-link" href="/capabilities/">All capabilities</a>'+''.join(out)+'</article>'

def write_migration(root,out,write,shell,ids):
    source=root/'content/migration';mapping=json.loads((source/'mapping.json').read_text());rows=validate_historical_migration(mapping)
    if mapping['owner']!='michaeljabbour' or len(rows)!=33 or {r['id'] for r in rows}!=ids:raise ValueError('Migration map must match33 capability identities')
    for row in rows:
        if row['portfolio_url']!='https://michaeljabbour.github.io/capabilities/'+row['id']+'/':raise ValueError('Migration guide destination differs')
        for key,name in [('old_url','old_repository'),('new_url','new_repository')]:
            if row[key]!='https://github.com/michaeljabbour/'+row[name] or not re.fullmatch('amplifier-[a-z0-9-]+',row[name]):raise ValueError('Migration repository mapping differs')
    body=markdown_body((source/'MIGRATION.md').read_text())
    write('migration',shell('Update a capability installation','Repository names and installation sources for existing capability users.',body,'','/migration/'))
    shutil.copyfile(source/'mapping.json',out/'migration/mapping.json')
