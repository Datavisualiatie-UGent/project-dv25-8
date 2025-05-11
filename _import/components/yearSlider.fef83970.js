// yearSlider.js
import {html} from "../../_node/htl@0.3.1/index.0caf36e7.js";

// Inject styles once
if (!document.getElementById("year-slider-styles-primevue-skip")) { // New unique ID
    const style = document.createElement("style");
    style.id = "year-slider-styles-primevue-skip";
    style.textContent = `
        .year-slider-container-prime-skip {
            display: inline-flex;
            align-items: center;
            /* Adjust gap for more buttons */
            gap: 0.5em; /* Slightly smaller gap between all elements */
            font-family: sans-serif;
            color: #495057;
        }

        /* Common styles for all buttons */
        .year-slider-container-prime-skip button {
            background: none;
            border: none;
            padding: 0.2em 0.4em;
            margin: 0;
            font-size: 1em; /* Base size */
            line-height: 1;
            color: #6c757d;
            cursor: pointer;
            border-radius: 3px;
            transition: color 0.2s, background-color 0.2s, opacity 0.2s;
            vertical-align: middle; /* Align buttons better with text */
        }

        /* Specific styles for skip buttons */
        .year-skip-button-prime {
             /* font-weight: bold; /* Optional: Make skip buttons bolder */
             padding: 0.2em 0.3em; /* Adjust padding slightly if needed */
        }
        .year-skip-button-prime.skip-prev::before { content: "«"; } /* Double angle quotes */
        .year-skip-button-prime.skip-next::before { content: "»"; }

        /* Specific styles for arrow buttons */
        .year-arrow-button-prime {
             /* No extra styles needed currently */
        }
        .year-arrow-button-prime.prev::before { content: "‹"; } /* Single angle quotes */
        .year-arrow-button-prime.next::before { content: "›"; }

        /* Style for hover state, but not when disabled */
        .year-slider-container-prime-skip button:hover:not(:disabled) {
            color: #343a40;
            background-color: #e9ecef;
        }

        /* Style for disabled state */
        .year-slider-container-prime-skip button:disabled {
            opacity: 0.4; /* Slightly more opacity for disabled */
            cursor: not-allowed;
            background-color: transparent;
            color: #6c757d;
        }

        .year-label-prime-skip {
            font-size: 1.5em;
            font-weight: bold; /* --- Change 1: Make label bold --- */
            color: #343a40; /* Slightly darker color for emphasis */
            padding: 0.1em 0.3em;
            min-width: 3.5em;
            text-align: center;
            user-select: none;
            vertical-align: middle;
        }
    `;
    document.head.appendChild(style);
}

// --- Change 2: Add skip functionality ---
export function createYearSlider(
    startYear,
    minYear,
    maxYear,
    onYearChange,
    skipStep = 10 // Allow customizing the skip step
) {
    let year = startYear;

    const container = html`<div class="year-slider-container-prime-skip"></div>`;

    // Create all four buttons
    const skipLeft = html`<button class="year-skip-button-prime skip-prev" title="Previous ${skipStep} Years"></button>`;
    const left = html`<button class="year-arrow-button-prime prev" title="Previous Year"></button>`;
    const right = html`<button class="year-arrow-button-prime next" title="Next Year"></button>`;
    const skipRight = html`<button class="year-skip-button-prime skip-next" title="Next ${skipStep} Years"></button>`;

    // Use the new bold label class
    const label = html`<span class="year-label-prime-skip">${year}</span>`;

    // Disable the right buttons if the year is at the max
    right.disabled = (year >= maxYear);
    skipRight.disabled = (year >= maxYear);


    function update() {
        label.textContent = year;
        onYearChange(year);

        // Disable buttons at the limits
        // A button is disabled if clicking it would have no effect or go out of bounds.
        left.disabled = (year <= minYear);
        skipLeft.disabled = (year <= minYear); // Disable skip if already at min

        right.disabled = (year >= maxYear);
        skipRight.disabled = (year >= maxYear); // Disable skip if already at max
    }

    // Single step handlers (no change)
    left.onclick = () => {
        if (year > minYear) {
            year--;
            update();
        }
    };

    right.onclick = () => {
        if (year < maxYear) {
            year++;
            update();
        }
    };

    // Skip step handlers
    skipLeft.onclick = () => {
        const targetYear = Math.max(minYear, year - skipStep); // Calculate target, clamp to min
        if (targetYear < year) { // Only update if the year actually changes
            year = targetYear;
            update();
        }
    };

    skipRight.onclick = () => {
        const targetYear = Math.min(maxYear, year + skipStep); // Calculate target, clamp to max
        if (targetYear > year) { // Only update if the year actually changes
            year = targetYear;
            update();
        }
    };

    // Append elements in the correct order: « ‹ YYYY › »
    container.append(skipLeft, left, label, right, skipRight);

    return container;
}