/* Small enhancements only: switch fictional runs and give honest clipboard feedback. */
'use strict';

const select = document.querySelector('#example-select');
const stamp = document.querySelector('#trace-stamp');

function showExample(id) {
  for (const node of document.querySelectorAll('[data-example]')) node.hidden = node.dataset.example !== id;
  const panel = document.querySelector(`.example-content[data-example="${id}"]`);
  if (panel && stamp) stamp.textContent = panel.dataset.outcome;
}

if (select) {
  select.addEventListener('change', () => showExample(select.value));
  showExample(select.value);
}

function openSkillSource() {
  if (location.hash === '#skill-source') document.querySelector('#skill-source').open = true;
}
window.addEventListener('hashchange', openSkillSource);
openSkillSource();

document.querySelectorAll('[data-copy]').forEach(button => {
  button.addEventListener('click', async () => {
    const target = document.getElementById(button.dataset.copy);
    const content = target instanceof HTMLTextAreaElement ? target.value : target.textContent;
    const status = document.getElementById(button.dataset.copy === 'skill-text' ? 'skill-copy-status' : 'copy-status');
    try {
      if (!navigator.clipboard) throw new Error('Clipboard unavailable');
      await navigator.clipboard.writeText(content);
      status.textContent = button.dataset.copy === 'skill-text' ? 'SKILL.md copied.' : 'Starting prompt copied.';
    } catch {
      // Keep a manual path when a browser denies clipboard access. Do not claim success.
      if (target instanceof HTMLTextAreaElement) {
        target.focus();
        target.select();
      } else {
        const range = document.createRange();
        range.selectNodeContents(target);
        const selection = window.getSelection();
        selection.removeAllRanges();
        selection.addRange(range);
      }
      status.textContent = 'Clipboard unavailable. The text is selected; use your browser’s Copy command.';
    }
  });
});
