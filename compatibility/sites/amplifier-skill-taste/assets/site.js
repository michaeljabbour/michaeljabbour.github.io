/* Small enhancements only: examples, map states, and honest clipboard feedback. */
'use strict';

const select = document.querySelector('#example-select');
const phaseButtons = [...document.querySelectorAll('[data-phase]')];
let examples = [];
let phase = 'after';

function setText(id, text) {
  document.getElementById(id).textContent = text;
}

function pointAt(coordinate) {
  // Illustrative positions, deliberately separate from a real assessment's anchors.
  // Leave the upper part of each quadrant clear for its explanatory label.
  const heights = { 1: 445, 2: 430, 3: 230, 4: 205, 5: 185 };
  return { x: 75 + (coordinate[0] - 1) * 125, y: heights[coordinate[1]] };
}

function placePoint(id, point) {
  const node = document.getElementById(id);
  node.setAttribute('cx', point.x);
  node.setAttribute('cy', point.y);
}

function renderExample() {
  const example = examples.find(item => item.id === select.value);
  if (!example) return;
  const proposed = phase === 'after';
  setText('map-kind', 'Illustrative ' + example.kind.toLowerCase());
  setText('example-brief', example.brief);
  setText('example-direction', proposed ? example.direction : 'Start with the same brief. Keep this baseline.');
  setText('example-title', proposed ? example.proposal : example.baseline);
  setText('example-detail', proposed ? example.proposal_detail : example.baseline_detail);
  for (const key of ['bottleneck', 'risk', 'verification', 'growth']) setText('example-' + key, example[key]);
  const before = pointAt(example.before);
  const after = pointAt(example.after);
  placePoint('baseline-point', before);
  placePoint('proposal-point', after);
  placePoint('proposal-halo', after);
  const path = document.getElementById('movement-path');
  const dx = after.x - before.x;
  const dy = after.y - before.y;
  const distance = Math.hypot(dx, dy);
  const end = { x: after.x - dx / distance * 20, y: after.y - dy / distance * 20 };
  const middle = { x: (before.x + after.x) / 2 - dy * .12, y: (before.y + after.y) / 2 + dx * .12 };
  const route = before.y === after.y
    ? `M ${before.x} ${before.y} Q ${middle.x} ${middle.y} ${end.x} ${end.y}`
    : `M ${before.x} ${before.y} H 550 Q 575 ${before.y} 575 ${before.y - 25} V ${end.y + 60} Q 575 ${end.y + 30} 550 ${end.y + 25} L ${end.x} ${end.y}`;
  path.setAttribute('d', route);
  for (const id of ['proposal-point', 'proposal-halo', 'movement-path']) document.getElementById(id).setAttribute('visibility', proposed ? 'visible' : 'hidden');
  for (const button of phaseButtons) button.setAttribute('aria-pressed', String(button.dataset.phase === phase));
  setText('plot-title', `${example.label}: ${proposed ? 'baseline and proposed change' : 'baseline'}`);
  setText('plot-description', `${example.baseline_detail} ${proposed ? 'Proposed: ' + example.proposal_detail : ''} Positions and movement are illustrative, not measured. No improvement has been verified.`);
}

async function loadExamples() {
  try {
    const response = await fetch('./assets/examples.json');
    if (!response.ok) throw new Error('Examples unavailable');
    examples = await response.json();
    select.addEventListener('change', () => { phase = 'after'; renderExample(); });
    phaseButtons.forEach(button => button.addEventListener('click', () => { phase = button.dataset.phase; renderExample(); }));
    renderExample();
  } catch {
    select.disabled = true;
    phaseButtons.forEach(button => { button.disabled = true; });
    setText('example-direction', 'Interactive examples could not load. The public-service form remains visible; read the worked example below.');
  }
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

loadExamples();
