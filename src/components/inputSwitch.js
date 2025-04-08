// switcher.js
import {html} from "htl";

// Inject styles once
if (!document.getElementById("switcher-styles")) {
    const style = document.createElement("style");
    style.id = "switcher-styles";
    style.textContent = `
        .switcher-container {
        display: inline-flex;
        align-items: center;
        gap: 0.5em;
        background-color: #f3f4f6;
        border-radius: 0.5em;
        padding: 0.4em 0.6em;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }

        .arrow-button {
        font-size: 1.2em;
        padding: 0.2em 0.6em;
        background-color: #e5e7eb;
        border: none;
        border-radius: 0.4em;
        cursor: pointer;
        transition: background-color 0.2s;
        }

        .arrow-button:hover {
        background-color: #d1d5db;
        }

        .switcher-label {
        font-size: 1em;
        font-weight: 700;
        background-color: #ffffff;
        border: none;
        border-radius: 0.3em;
        padding: 0.2em 0.6em;
        text-align: center;
        width: 120px;
        }
    `;
    document.head.appendChild(style);
}

export function createSwitcher(options, onChange) {
  let index = 0;

  const container = html`<div class="switcher-container"></div>`;
  const left = html`<button class="arrow-button">&#8592;</button>`;
  const right = html`<button class="arrow-button">&#8594;</button>`;
  const label = html`<input class="switcher-label" type="text" value="${options[index]}" readonly />`;

  function update() {
    label.value = options[index];
    onChange(options[index]); // Notify the outside world
  }

  left.onclick = () => {
    index = (index - 1 + options.length) % options.length;
    update();
  };

  right.onclick = () => {
    index = (index + 1) % options.length;
    update();
  };

  container.append(left, label, right);
  return container;
}

