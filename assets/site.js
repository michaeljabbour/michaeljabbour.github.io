(() => {
  const form = document.querySelector('#project-filters');
  if (form) {
    const search = form.querySelector('[name="q"]');
    const category = form.querySelector('[name="category"]');
    const format = form.querySelector('[name="format"]');
    const rows = [...document.querySelectorAll('[data-project]')];
    const count = document.querySelector('#result-count');
    const empty = document.querySelector('#no-results');
    const clear = document.querySelector('#clear-filters');
    function apply(updateURL = true) {
      const q = search.value.trim().toLocaleLowerCase();
      const terms = q.split(/\s+/).filter(Boolean);
      let visible = 0;
      rows.forEach(row => {
        const match = (category.value === 'all' || row.dataset.category === category.value)
          && (format.value === 'all' || row.dataset.format === format.value)
          && terms.every(term => row.dataset.search.includes(term));
        row.hidden = !match;
        if (match) visible++;
      });
      count.textContent = `${visible} ${visible === 1 ? 'capability' : 'capabilities'}${visible !== rows.length ? ` of ${rows.length}` : ''}`;
      empty.hidden = visible !== 0;
      clear.hidden = !q && category.value === 'all' && format.value === 'all';
      if (updateURL) {
        const url = new URL(location.href);
        url.search = '';
        if (search.value.trim()) url.searchParams.set('q', search.value.trim());
        if (category.value !== 'all') url.searchParams.set('category', category.value);
        if (format.value !== 'all') url.searchParams.set('format', format.value);
        history.replaceState(null, '', url.pathname + url.search + url.hash);
      }
    }
    function restore() {
      const params = new URLSearchParams(location.search);
      search.value = params.get('q') || '';
      category.value = [...category.options].some(x => x.value === params.get('category')) ? params.get('category') : 'all';
      format.value = [...format.options].some(x => x.value === params.get('format')) ? params.get('format') : 'all';
      apply(false);
    }
    function reset() {
      search.value = '';
      category.value = 'all';
      format.value = 'all';
      apply();
      search.focus();
    }
    form.addEventListener('submit', e => { e.preventDefault(); apply(); });
    search.addEventListener('input', () => apply());
    category.addEventListener('change', () => apply());
    format.addEventListener('change', () => apply());
    clear.addEventListener('click', reset);
    document.querySelectorAll('[data-reset-filters]').forEach(b => b.addEventListener('click', reset));
    addEventListener('popstate', restore);
    restore();
  }
  document.querySelectorAll('[data-copy]').forEach(button => {
    button.addEventListener('click', async () => {
      const source = document.getElementById(button.dataset.copy);
      const status = button.nextElementSibling;
      if (!source || !status) return;
      try {
        if (!navigator.clipboard?.writeText) throw new Error('Clipboard unavailable');
        await navigator.clipboard.writeText(source.textContent.trim());
        status.textContent = 'Copied. Paste it where you need it.';
        button.textContent = 'Copied';
      } catch {
        const selection = getSelection();
        const range = document.createRange();
        range.selectNodeContents(source);
        selection.removeAllRanges();
        selection.addRange(range);
        status.textContent = 'Text selected. Use your keyboard’s copy command.';
      }
    });
  });
})();
