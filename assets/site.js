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
  const reducedMotion = () => matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.querySelectorAll('[data-journey]').forEach(guide => {
    const nav = guide.querySelector('[data-journey-nav]');
    const links = [...guide.querySelectorAll('[data-stage-link]')];
    const panels = [...guide.querySelectorAll('[data-stage-panel]')];
    const controls = guide.querySelector('[data-journey-controls]');
    const previous = guide.querySelector('[data-journey-previous]');
    const next = guide.querySelector('[data-journey-next]');
    const status = guide.querySelector('[data-journey-status]');
    let current = 0;
    if (!links.length || links.length !== panels.length) return;
    guide.classList.add('is-enhanced');
    nav.setAttribute('role', 'tablist');
    controls.hidden = false;
    function show(index, updateURL = false, focusTab = false) {
      current = (index + links.length) % links.length;
      links.forEach((link, i) => {
        link.setAttribute('role', 'tab');
        link.setAttribute('aria-controls', panels[i].id);
        link.setAttribute('aria-selected', String(i === current));
        link.tabIndex = i === current ? 0 : -1;
        link.classList.toggle('is-current', i === current);
        panels[i].hidden = i !== current;
        panels[i].setAttribute('role', 'tabpanel');
        panels[i].setAttribute('aria-labelledby', link.id);
        panels[i].tabIndex = 0;
      });
      previous.disabled = current === 0;
      next.textContent = current === links.length - 1 ? 'Start with a new question' : 'Next: ' + links[current + 1].lastElementChild.textContent;
      status.textContent = `${current + 1} of ${links.length}: ${links[current].lastElementChild.textContent}`;
      if (updateURL) {
        const url = new URL(location.href);
        url.searchParams.delete('moment');
        url.hash = panels[current].id;
        history.pushState(null, '', url.pathname + url.search + url.hash);
      }
      if (focusTab) links[current].focus({preventScroll: true});
    }
    function restore() {
      const id = location.hash.startsWith('#stage-') ? location.hash.slice(7) : new URLSearchParams(location.search).get('moment');
      const index = links.findIndex(link => link.dataset.stageLink === id);
      show(index >= 0 ? index : 0);
    }
    function revealIfNeeded() {
      if (panels[current].getBoundingClientRect().top > innerHeight * 0.6) {
        guide.scrollIntoView({behavior: 'instant', block: 'start'});
      }
    }
    links.forEach((link, index) => {
      link.addEventListener('click', event => { event.preventDefault(); show(index, true); revealIfNeeded(); });
      link.addEventListener('keydown', event => {
        let target;
        if (event.key === 'ArrowRight' || event.key === 'ArrowDown') target = current + 1;
        else if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') target = current - 1;
        else if (event.key === 'Home') target = 0;
        else if (event.key === 'End') target = links.length - 1;
        else return;
        event.preventDefault();
        show(target, true, true);
        revealIfNeeded();
      });
    });
    function advance(offset) {
      show(current + offset, true, true);
      guide.scrollIntoView({behavior: reducedMotion() ? 'instant' : 'smooth', block: 'start'});
    }
    previous.addEventListener('click', () => advance(-1));
    next.addEventListener('click', () => advance(1));
    addEventListener('hashchange', restore);
    addEventListener('popstate', restore);
    restore();
  });
  const story = document.querySelector('[data-overview-video]');
  if (story) {
    let seekRequest = 0;
    function positionStory(chapter) {
      const target = Number(chapter.dataset.filmStart);
      if (!Number.isFinite(target) || target < 0) return;
      const request = ++seekRequest;
      story.pause();
      let status = document.querySelector('.story-status');
      if (!status) {
        status = document.createElement('p');
        status.className = 'story-status';
        status.setAttribute('role', 'status');
        story.parentElement.append(status);
      }
      const seconds = Math.round(target);
      const time = `${Math.floor(seconds / 60)}:${String(seconds % 60).padStart(2, '0')}`;
      status.textContent = `Finding ${time} in the film…`;
      const confirm = () => {
        if (request !== seekRequest) return;
        status.textContent = Math.abs(story.currentTime - target) < 0.5
          ? `Film positioned at ${time}. Press Play to watch.`
          : `The player could not jump to ${time}. Try the video timeline.`;
      };
      const seek = () => {
        if (request !== seekRequest) return;
        if (Math.abs(story.currentTime - target) < 0.1) confirm();
        else {
          story.addEventListener('seeked', confirm, {once: true});
          story.currentTime = Math.min(target, Number.isFinite(story.duration) ? story.duration : target);
        }
      };
      if (story.readyState >= 1) seek();
      else {
        story.addEventListener('loadedmetadata', seek, {once: true});
        story.preload = 'metadata';
        story.load();
      }
      story.scrollIntoView({behavior: reducedMotion() ? 'instant' : 'smooth', block: 'center'});
      story.focus({preventScroll: true});
    }
    document.querySelectorAll('[data-story-moment]').forEach(chapter => chapter.addEventListener('click', event => {
      event.preventDefault();
      const url = new URL(chapter.href);
      history.pushState(null, '', url.pathname + url.search + url.hash);
      positionStory(chapter);
    }));
    const initialMoment = new URLSearchParams(location.search).get('moment');
    if (initialMoment) {
      const chapter = [...document.querySelectorAll('[data-story-moment]')].find(link => link.dataset.storyMoment === initialMoment);
      if (chapter) positionStory(chapter);
    }
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
