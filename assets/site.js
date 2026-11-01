(() => {
  document.querySelectorAll('[data-capability-browser]').forEach(browser => {
    const form = browser.querySelector('form');
    const search = form.querySelector('[name="q"]');
    const flowSelect = form.querySelector('select[name="flow"]');
    const flowValue = form.querySelector('input[name="flow"]');
    const category = form.querySelector('[name="category"]');
    const format = form.querySelector('[name="format"]');
    const stageValue = form.querySelector('[name="stage"]');
    const flowButtons = [...browser.querySelectorAll('[data-flow-filter]')];
    const stageRows = [...browser.querySelectorAll('[data-stage-row]')];
    const stageButtons = [...browser.querySelectorAll('[data-stage-filter]')];
    const stageGroup = browser.querySelector('[data-stage-group]');
    const rows = [...browser.querySelectorAll('[data-capability-id]')];
    const status = browser.querySelector('[data-filter-status]');
    const clear = browser.querySelector('[data-filter-clear]');
    const empty = browser.querySelector('[data-filter-empty]');
    const flowNames = new Map(flowButtons.map(button => [button.dataset.flowFilter, button.querySelector('strong').textContent]));
    if (flowSelect) [...flowSelect.options].filter(option => option.value !== 'all').forEach(option => flowNames.set(option.value, option.textContent));
    const categoryNames = new Map([...browser.querySelectorAll('[data-legacy-category]')].map(node => [node.dataset.legacyCategory, node.dataset.categoryTitle]));
    if (category?.options) [...category.options].filter(option => option.value !== 'all').forEach(option => categoryNames.set(option.value, option.textContent));
    const state = {flow: 'all', stage: 'all', category: 'all', format: 'all', q: ''};
    const validStage = (flow, value) => value === 'all' || stageButtons.some(button => button.dataset.stageFlow === flow && button.dataset.stageFilter === value);
    function keepStageVisible() {
      const selected = stageButtons.find(button => button.dataset.stageFlow === state.flow && button.dataset.stageFilter === state.stage);
      if (!selected) return;
      const track = selected.closest('.stage-track');
      const left = selected.getBoundingClientRect().left - track.getBoundingClientRect().left + track.scrollLeft;
      const right = left + selected.offsetWidth;
      if (left < track.scrollLeft) track.scrollLeft = Math.max(0, left - 4);
      else if (right > track.scrollLeft + track.clientWidth) track.scrollLeft = right - track.clientWidth + 4;
    }
    function writeURL(mode) {
      const url = new URL(location.href);
      ['flow','stage','q','category','format','moment'].forEach(key => url.searchParams.delete(key));
      if (state.flow !== 'all') url.searchParams.set('flow', state.flow);
      if (state.flow !== 'all' && state.stage !== 'all') url.searchParams.set('stage', state.stage);
      if (state.q.trim()) url.searchParams.set('q', state.q.trim());
      if (state.category !== 'all') url.searchParams.set('category', state.category);
      if (state.format !== 'all') url.searchParams.set('format', state.format);
      url.hash = browser.hasAttribute('data-work-flows') ? 'journey' : '';
      const target = url.pathname + url.search + url.hash;
      if (target !== location.pathname + location.search + location.hash) history[mode === 'push' ? 'pushState' : 'replaceState'](null, '', target);
    }
    function apply(mode = null) {
      if (flowSelect) flowSelect.value = state.flow;
      if (flowValue) flowValue.value = state.flow;
      if (category) category.value = state.category;
      if (format) format.value = state.format;
      if (stageValue) stageValue.value = state.stage;
      if (search.value !== state.q) search.value = state.q;
      flowButtons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.flowFilter === state.flow)));
      stageGroup.hidden = state.flow === 'all';
      stageRows.forEach(row => { row.hidden = row.dataset.stageRow !== state.flow; });
      stageButtons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.stageFlow === state.flow && button.dataset.stageFilter === state.stage)));
      const terms = state.q.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
      const seen = new Set();
      let visible = 0;
      rows.forEach(row => {
        const id = row.dataset.capabilityId;
        const match = !seen.has(id)
          && (state.flow === 'all' || row.dataset.flows.split(' ').includes(state.flow))
          && (state.stage === 'all' || row.dataset.stageMemberships.split(' ').includes(state.flow + ':' + state.stage))
          && (state.category === 'all' || row.dataset.category === state.category)
          && (state.format === 'all' || row.dataset.format === state.format)
          && terms.every(term => row.dataset.search.includes(term));
        if (match) { seen.add(id); visible++; }
        row.hidden = !match;
      });
      const stageButton = stageButtons.find(button => button.dataset.stageFlow === state.flow && button.dataset.stageFilter === state.stage);
      const title = [state.flow !== 'all' ? flowNames.get(state.flow) : categoryNames.get(state.category), state.stage !== 'all' ? stageButton?.textContent : null].filter(Boolean).join(' / ');
      status.textContent = `${title || 'All workflows'}: ${visible} ${visible === 1 ? 'capability' : 'capabilities'}`;
      clear.hidden = state.flow === 'all' && state.stage === 'all' && state.category === 'all' && state.format === 'all' && !state.q;
      empty.hidden = visible !== 0;
      const resetScope = browser.querySelector('[data-reset-scope]');
      if (resetScope) resetScope.textContent = state.flow === 'all' ? 'Show all capabilities' : 'Show all in this flow';
      if (mode) writeURL(mode);
      keepStageVisible();
    }
    function restore() {
      const params = new URLSearchParams(location.search);
      const hashFlow = location.hash.startsWith('#flow-') ? location.hash.slice(6) : null;
      const requestedFlow = params.get('flow') || hashFlow;
      state.flow = flowNames.has(requestedFlow) ? requestedFlow : 'all';
      state.stage = state.flow !== 'all' && validStage(state.flow, params.get('stage')) ? params.get('stage') : 'all';
      const hashCategory = location.hash.startsWith('#stage-') ? location.hash.slice(7) : null;
      const requestedCategory = params.get('category') || hashCategory;
      state.category = state.flow === 'all' && categoryNames.has(requestedCategory) ? requestedCategory : 'all';
      state.format = format && [...format.options].some(option => option.value === params.get('format')) ? params.get('format') : 'all';
      state.q = params.get('q') || '';
      apply();
    }
    function chooseFlow(flow) {
      state.flow = flowNames.has(flow) ? flow : 'all';
      state.stage = 'all'; state.category = 'all'; apply('push');
    }
    flowButtons.forEach(button => button.addEventListener('click', () => chooseFlow(button.dataset.flowFilter)));
    flowSelect?.addEventListener('change', () => chooseFlow(flowSelect.value));
    stageButtons.forEach(button => {
      button.addEventListener('click', () => {
        if (button.dataset.stageFlow !== state.flow) return;
        state.stage = button.dataset.stageFilter; apply('push');
      });
      button.addEventListener('keydown', event => {
        const peers = stageButtons.filter(peer => peer.dataset.stageFlow === button.dataset.stageFlow);
        let index = peers.indexOf(button);
        if (event.key === 'ArrowRight') index = (index + 1) % peers.length;
        else if (event.key === 'ArrowLeft') index = (index - 1 + peers.length) % peers.length;
        else if (event.key === 'Home') index = 0;
        else if (event.key === 'End') index = peers.length - 1;
        else return;
        event.preventDefault(); peers[index].focus({preventScroll: true});
        const track = peers[index].closest('.stage-track');
        track.scrollLeft += peers[index].getBoundingClientRect().left - track.getBoundingClientRect().left;
      });
    });
    search.addEventListener('input', () => { state.q = search.value; apply('replace'); });
    format?.addEventListener('change', () => { state.format = format.value; apply('push'); });
    form.addEventListener('submit', event => { event.preventDefault(); state.q = search.value; apply('push'); });
    clear.addEventListener('click', () => {
      Object.assign(state, {flow:'all',stage:'all',category:'all',format:'all',q:''}); apply('push'); search.focus({preventScroll:true});
    });
    browser.querySelectorAll('[data-reset-scope]').forEach(button => button.addEventListener('click', () => {
      Object.assign(state, {stage:'all',category:'all',format:'all',q:''}); apply('push'); search.focus({preventScroll:true});
    }));
    addEventListener('popstate', restore);
    addEventListener('hashchange', restore);
    restore();
  });
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
