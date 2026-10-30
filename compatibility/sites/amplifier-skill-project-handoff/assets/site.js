"use strict";
(function () {
  const chooser = document.getElementById("example-select");
  const panels = Array.from(document.querySelectorAll("[data-example]"));
  if (chooser) chooser.addEventListener("change", function () {
    panels.forEach(function (panel) { panel.hidden = panel.dataset.example !== chooser.value; });
  });
  document.querySelectorAll("[data-answer]").forEach(function (button) {
    button.addEventListener("click", function () {
      const exercise = button.closest(".exercise");
      const chosen = exercise.querySelector("input:checked");
      const output = exercise.querySelector("[role=status]");
      if (!chosen) {
        output.textContent = "Choose an answer first. The evidence is above the question.";
        output.removeAttribute("data-correct");
        return;
      }
      const correct = chosen.value === button.dataset.answer;
      output.dataset.correct = String(correct);
      output.textContent = (correct ? "That follows the evidence. " : "Read the authority and revision again. ") + button.dataset.feedback;
    });
  });
  document.querySelectorAll("[data-copy]").forEach(function (button) {
    button.addEventListener("click", async function () {
      const target = document.getElementById(button.dataset.copy);
      const status = document.getElementById("copy-status");
      const text = target.value === undefined ? target.textContent : target.value;
      try {
        if (!navigator.clipboard || !window.isSecureContext) throw new Error("Clipboard unavailable");
        await navigator.clipboard.writeText(text);
        status.textContent = "Prompt copied. Paste it in your agent's chat.";
      } catch (_) {
        const range = document.createRange();
        range.selectNodeContents(target);
        const selection = window.getSelection();
        selection.removeAllRanges();
        selection.addRange(range);
        status.textContent = "The prompt is selected. Use your browser's Copy command.";
      }
    });
  });
}());
