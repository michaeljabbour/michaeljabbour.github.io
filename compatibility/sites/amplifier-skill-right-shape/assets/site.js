/* Small enhancements only: switch fictional placements, run the rubric calculator, and give honest clipboard feedback. */
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

// The calculator reads every band, cap and label from attributes the build wrote from the rubric.
const calc = document.querySelector('.calc');
if (calc) {
  const bands = JSON.parse(calc.dataset.bands);
  const names = JSON.parse(calc.dataset.names);
  const sliders = [...calc.querySelectorAll('input[type=range]')];
  const gates = [...calc.querySelectorAll('input[data-gate]')];
  const checks = [...calc.querySelectorAll('input[data-check]')];
  const update = () => {
    let score = 0;
    sliders.forEach((slider, i) => {
      const value = Number(slider.value);
      score += value;
      document.getElementById(`o${i + 1}`).textContent = value;
      document.getElementById(`h${i + 1}`).textContent = JSON.parse(slider.dataset.hints)[value];
    });
    const wanted = bands.find(([low, high]) => score >= low && score <= high)[2];
    const failed = gates.filter(g => !g.checked);
    const ceiling = Math.min(9, ...failed.map(g => Number(g.dataset.cap)));
    const rung = Math.min(wanted, ceiling);
    const ticked = checks.filter(c => c.checked).map(c => c.dataset.check);
    document.getElementById('calc-rung').textContent = `Rung ${rung} · ${names[rung]}`;
    document.getElementById('calc-meta').textContent = `Need score ${score} wants rung ${wanted}. Ceiling ${ceiling}${failed.length ? ` (failed: ${failed.map(g => g.dataset.gate).join(', ')})` : ''}.`;
    document.getElementById('calc-msg').textContent = wanted > ceiling
      ? 'The job wants more than it can safely have. Lower the need, or fix the failed gates. Never grant it anyway.'
      : 'Need fits under the ceiling. Build at this rung, and check the tiebreakers before going one lower.';
    let shape;
    if (ticked.includes('H4') && ticked.length < 3) shape = 'Shape: decompose first. One worker would be over its size limit.';
    else if (ticked.length >= 2) shape = 'Shape: an outer harness behind an agent interface, or a function if the result is bounded and checkable. Composition does not raise the ceiling.';
    else shape = 'Shape: a single worker. No harness needed yet.';
    document.getElementById('calc-shape').textContent = shape;
  };
  calc.addEventListener('input', update);
  update();
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
