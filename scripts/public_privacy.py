"""Apply only literal examples reviewed against the exact public file bytes."""
import hashlib

def reviewed_example_text(raw, content, entry):
    examples=entry.get('reviewed_public_examples',[])
    if not isinstance(examples,list):raise ValueError('Invalid public example review list')
    if not examples:return raw
    actual=hashlib.sha256(content).hexdigest()
    if actual!=entry.get('sha256'):raise ValueError('Example review file hash differs')
    scrubbed=raw
    for example in examples:
        if not isinstance(example,dict) or set(example)!={'literal','reason','reviewed_file_sha256'}:raise ValueError('Invalid public example review')
        literal=example['literal']
        if not isinstance(literal,str) or not literal or not isinstance(example['reason'],str) or not example['reason'].strip():raise ValueError('Empty public example review')
        if example['reviewed_file_sha256']!=actual or literal not in raw:raise ValueError('Stale public example review')
    for example in sorted(examples,key=lambda item:len(item['literal']),reverse=True):
        scrubbed=scrubbed.replace(example['literal'],'[REVIEWED_PUBLIC_EXAMPLE]')
    return scrubbed
