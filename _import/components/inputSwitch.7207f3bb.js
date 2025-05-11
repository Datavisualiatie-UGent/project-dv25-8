// toggleSwitcher.js
import {html} from "../../_node/htl@0.3.1/index.0caf36e7.js";

// --- Style Injection ---
const styleId = "toggle-switcher-styles";

if (!document.getElementById(styleId)) {
    const style = document.createElement("style");
    style.textContent = `
        .toggle-switcher-container {
            display: inline-flex;
            background-color: #e5e7eb; /* Slightly darker background */
            border-radius: 0.5em;
            padding: 0.25em; /* Padding around the buttons */
            box-shadow: inset 0 1px 3px rgba(0,0,0,0.1); /* Inner shadow for depth */
            overflow: hidden; /* Ensure rounded corners clip children */
        }

        .toggle-option-button {
            font-size: 0.9em; /* Slightly smaller font */
            font-weight: 500;
            padding: 0.5em 1em; /* More padding for better click area */
            background-color: transparent; /* Default transparent background */
            border: none;
            border-radius: 0.4em; /* Match container rounding */
            cursor: pointer;
            transition: background-color 0.2s ease-in-out, color 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
            color: #374151; /* Default text color */
            margin: 0; /* Remove default button margins */
            white-space: nowrap; /* Prevent text wrapping */
        }

        /* Add margin between buttons using adjacent sibling selector */
        .toggle-option-button + .toggle-option-button {
             /* No margin needed if background handles separation */
        }

        .toggle-option-button:hover:not(.active) {
            background-color: rgba(209, 213, 219, 0.5); /* Subtle hover for non-active */
        }

        .toggle-option-button.active {
            background-color: #ffffff; /* White background for active */
            color: #1f2937; /* Darker text for active */
            font-weight: 600;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1); /* Slight shadow for active */
            cursor: default; /* Indicate it's already selected */
        }

        .toggle-option-button:focus {
            outline: none; /* Remove default focus outline */
        }

        .toggle-option-button:focus-visible {
             /* Optional: Add a visible focus ring for accessibility */
            box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.5);
        }
    `;
    document.head.appendChild(style);
}

// --- Component Function ---
export function createSwitcher(options, onChange, initialIndex = 0) {
  // Validate initialIndex
  let selectedIndex = (options && options.length > 0 && initialIndex >= 0 && initialIndex < options.length) ? initialIndex : 0;

  const container = html`<div class="toggle-switcher-container"></div>`;
  const buttons = []; // Keep track of button elements

  // Create buttons for each option
  options.forEach((option, index) => {
    const button = html`<button class="toggle-option-button">${option}</button>`;

    button.onclick = () => {
      // If already selected, do nothing
      if (index === selectedIndex) {
          return;
      }

      // Remove 'active' class from the previously selected button
      if (buttons[selectedIndex]) {
          buttons[selectedIndex].classList.remove('active');
      }

      // Update selected index
      selectedIndex = index;

      // Add 'active' class to the newly selected button
      button.classList.add('active');

      // Notify the outside world
      onChange(options[selectedIndex], selectedIndex);
    };

    buttons.push(button); // Store the button reference
    container.append(button); // Add button to the container
  });

  // Set initial active state
  if (buttons.length > 0 && buttons[selectedIndex]) {
    buttons[selectedIndex].classList.add('active');
  }

  return container;
}