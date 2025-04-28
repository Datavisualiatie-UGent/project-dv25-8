```js
const {winners, raceInfo} = await FileAttachment("data/races.json").json();
import {createSwitcher} from "./components/inputSwitch.js";
```

# Race trough the years

Welcome to an interactive journey through the most prestigious cycling races across the globe. Each button represents a major race, and by selecting one, you'll uncover intriguing insights into the history of the race. 

```js
// Mapping of the most important races to their respective logo
const racesList = {
  'tour-de-france': 'https://i.postimg.cc/jd9tP9kP/tour-de-france.png',
  'giro-d-italia': 'https://i.postimg.cc/rpkNrZTj/giro-d-italia.jpg',
  'vuelta-a-espana': 'https://i.postimg.cc/ZKv8DzKj/vuelta-a-espana.png',
  'paris-roubaix': 'https://i.postimg.cc/gJcyMwn6/paris-roubaix.jpg',
  'liege-bastogne-liege': 'https://i.postimg.cc/qqS8MjQ8/liege-bastogne-liege.png',
  'milano-sanremo': 'https://i.postimg.cc/nrC4J6KF/milano-sanremo.jpg',
  'ronde-van-vlaanderen': 'https://i.postimg.cc/Wz1TwPv6/ronde-van-vlaanderen.gif',
  'il-lombardia': 'https://i.postimg.cc/nzd4NHDS/il-lombardia.jpg',
  'world-championship': 'https://i.postimg.cc/1Rv954GW/world-championship.png'
}
```

```js
// Grid with buttons for each race
const buttons = Inputs.button(
  Object.keys(racesList).map(race => [html`
    <div class="race-button">
        <img src="${racesList[race]}" alt="${race}" />
      </div>`, 
      _ => race]
  ), {value: 'tour-de-france'});

// Selected race button
const selectedRace = Generators.input(buttons);
```

<div>
    ${display(buttons)}
</div>

```js	
// Load the world map
const world = await d3.json("https://cdn.jsdelivr.net/npm/world-atlas@2/countries-50m.json");
const countries = topojson.feature(world, world.objects.countries);

// Mutable stores to keep track of the selected country id and name on the map
const selectedCountryId = Mutable("");
const selectedCountryName = Mutable("");

// Define a function that creates a map of the world with the number of riders per country
function winnersRacesMap(race, { width } = {}) {
  // Filter based on the race
  const filteredData = winners[race] || [];

  // Aggregate total wins per country
  const countryWins = d3.rollup(
    filteredData,
    v => d3.sum(v, d => d.first_places),
    d => d.nationality
  );

  // Define a color scale
  const color = d3.scaleSequentialLog(d3.interpolateBlues)
    .domain([1, d3.max(Array.from(countryWins.values()))]);

  // Create an SVG element
  const svg = d3.create("svg")
    .attr("width", width)
    .attr("height", width / 2.5)
    .call(d3.zoom().scaleExtent([1, 15]) // Allow zooming between 1x and 15x
    .on("zoom", (event) => {
      svg.select("g").attr("transform", event.transform);
    }));

  const g = svg.append("g");

  // Draw the map
  g.selectAll("path")
    .data(countries.features)
    .enter()
    .append("path")
    .attr("d", d3.geoPath(d3.geoEquirectangular()))
    .attr("fill", d => {
      const totalWins = countryWins.get(+d.id) || 0;
      return totalWins > 0 ? color(totalWins) : "#eee";
    })
    .on("click", (event, d) => {
      if (selectedCountryId.value === d.id) {
        selectedCountryId.value = "";
        selectedCountryName.value = "";
      } else {
        selectedCountryId.value = d.id;
        selectedCountryName.value = d.properties.name;
      }
    })
    .attr("stroke", "white")
    .attr("stroke-width", 0.7);

  return html`
  <div class="map-container">
    ${svg.node()}
  </div>`;
}
```

```js	
// Function to display the ranking of winners
function winnersRanking(race, { width } = {}) {
    // Filter based on the race
    const filteredData = winners[race] || [];

    // If a country is selected, filter the winners
    const countryfilteredData = selectedCountryId ? 
        filteredData.filter(d => d.nationality === +selectedCountryId) : filteredData;
        
    // Sort winners by most wins
    const sortedWinners = countryfilteredData
        .map(d => ({ name: d.rider_name, wins: d.first_places }))
        .filter(d => d.wins > 0)
        .sort((a, b) => b.wins - a.wins);

    // Count the total number of wins
    const totalWins = d3.sum(sortedWinners, d => d.wins);

    return html`
        <div class="ranking-container" style="max-width: ${width}px; max-height: ${width * 1.35}px; overflow-y: auto;">
            ${selectedCountryId && selectedCountryName ? html`
              <h3><strong>${selectedCountryName} (Total: ${totalWins} ${totalWins !== 1 ? 'wins' : 'win'})</strong></h3>
            ` : html`<h3><strong>All-time winners list</strong></h3>`}

            ${sortedWinners.map(winner => html`
                <li><strong>${winner.name}</strong>: ${winner.wins} ${winner.wins > 1 ? 'wins' : 'win'}</li>
            `)}
        </ul>
    `;
}
```

<div>
  <h2 style="margin-bottom: 1rem;">${selectedRace.replace(/-/g, ' ').toUpperCase()}</h2>
</div>

### Where winners are born
On the left, a dynamic map highlights the countries that have produced the most winners for the selected race. On the right, you'll see a comprehensive list of all race victors.Engage with the map by clicking on any country to filter the winners list by nation. To reset and view the complete list again, simply unclick a country. Explore how different countries have made their mark on the world of cycling!

<div>
    <div class="content">
        <div class="card map-container">
            ${resize((width) => winnersRacesMap(selectedRace, {width}))}
        </div>
        <div class="card ranking-container">
            ${resize((width) => winnersRanking(selectedRace, {width}))}
        </div>
    </div>
</div>

```js

// Function that plots the distance and average of speed for the selected race over the years
function raceDetails(race, metric, { width } = {}) {
  const data = raceInfo[race] || [];
  const filteredData = data.filter(d => d.average_speed > 0 && d.distance > 0);

  // Get the annotations for the current race
  const annotations = customAnnotations.filter(a => a.race === race);

  // Extend data points with annotation if available
  const annotatedData = filteredData.map(d => {
    const annotation = annotations.find(a => a.year === d.year);
    return {
      ...d,
      annotation: annotation?.label || ""
    };
  });

  // Get top 3 entries based on selected metric
  const top3 = [...filteredData]
    .sort((a, b) => b[metric.value] - a[metric.value])
    .slice(0, 3);

  const medals = ["🥇", "🥈", "🥉"];

  // Get year bounds of the data
  const years = filteredData.map(d => d.year);
  const minYear = d3.min(years);
  const maxYear = d3.max(years);

  // List of highlighted periods (WW I and WW II)
  const highlightPeriods = [
    { start: 1914, end: 1918, label: "WW I" },
    { start: 1940, end: 1945, label: "WW II" }
  ];

  // Filter to only show highlightPeriods that overlap with data
  const visiblePeriods = highlightPeriods.filter(p => p.end >= minYear && p.start <= maxYear);

  return Plot.plot({
    width,
    height: width * 0.35,
    grid: true,

    marks: [
      // Line
      Plot.line(filteredData, {
        x: "year",
        y: metric.value,
        stroke: metric.color,
        strokeWidth: 2
      }),

      // Dotted vertical lines for start and end of periods
      Plot.ruleX(
        visiblePeriods.flatMap(p => [p.start, p.end]),
        {
          stroke: "black",
          strokeOpacity: 0.6,
          strokeDasharray: "4,2", // Dotted line
          strokeWidth: 1
        }
      ),

      // Dots
      Plot.dot(filteredData, {
        x: "year",
        y: metric.value,
        fill: metric.color,
        strokeWidth: 1,
        r: 3,
      }),
      
      // Tooltip for each dot
      Plot.tip(annotatedData, Plot.pointer({
        x: "year",
        y: metric.value,
        title: (d) => [`Year: ${d.year}\n${metric.label}: ${d[metric.value]} ${metric.unit}` +
                       `${d.annotation ? '\nNote: ' + d.annotation : ""}`],
      })),

      // Medal annotations for top 3
      Plot.text(
        top3.map((d, i) => ({ ...d, medal: medals[i] })),
        {
          x: "year",
          y: metric.value,
          text: d => d.medal,
          dy: -15,
          fontSize: 18,
          textAnchor: "middle",
        }
      ),

      // Annotation text centered between period start and end
      Plot.text(
        visiblePeriods.map(p => ({
          year: (p.start + p.end) / 2,
          label: `${p.label}`
        })),
        {
          x: "year",
          text: d => d.label,
          dy: 210,
          fontSize: 14,
          fontWeight: "bold",
          fill: "black"
        }
      ),
    ],
    x: { label: "Year", ticks: 10, tickFormat: d3.format("d") },
    y: { label: metric.label, nice: true }
  });
}
```

```js	
// List with custom annotations to make the plot more informative.
const customAnnotations = [
  {
    race: "milano-sanremo",
    year: 2013,
    label: "Race was neutralized due to cold, rain and snow.",
  },
  {
    race: "world-championship",
    year: 2002,
    label: "Completely flat circuit in Zolder, Belgium.",
  },
  {
    race: "world-championship",
    year: 2011,
    label: "Completely flat circuit in Copenhagen, Denmark.",
  },
  {
    race: "world-championship",
    year: 2016,
    label: "Completely flat circuit in Doha, Qatar.",
  },
  {
    race: "ronde-van-vlaanderen",
    year: 1941,
    label: "While the race was canceled during WW I, since the war front lay right trough Flanders, during the second world war the Nazis gave permission to organize the race. They wanted the so-called 'entertainments' to continue, so as not to undermine the morale of the population too much. However, adjustments needed to be made and new roads were discovered that are still part of the route today.",
  },
  {
    race: "ronde-van-vlaanderen",
    year: 1942,
    label: "While the race was canceled during WW I, since the war front lay right trough Flanders, during the second world war the Nazis gave permission to organize the race. They wanted the so-called 'entertainments' to continue, so as not to undermine the morale of the population too much. However, adjustments needed to be made and new roads were discovered that are still part of the route today.",
  },
  {
    race: "ronde-van-vlaanderen",
    year: 1943,
    label: "While the race was canceled during WW I, since the war front lay right trough Flanders, during the second world war the Nazis gave permission to organize the race. They wanted the so-called 'entertainments' to continue, so as not to undermine the morale of the population too much. However, adjustments needed to be made and new roads were discovered that are still part of the route today.",
  },
  {
    race: "ronde-van-vlaanderen",
    year: 1944,
    label: "While the race was canceled during WW I, since the war front lay right trough Flanders, during the second world war the Nazis gave permission to organize the race. They wanted the so-called 'entertainments' to continue, so as not to undermine the morale of the population too much. However, adjustments needed to be made and new roads were discovered that are still part of the route today.",
  },
  {
    race: "ronde-van-vlaanderen",
    year: 1945,
    label: "While the race was canceled during WW I, since the war front lay right trough Flanders, during the second world war the Nazis gave permission to organize the race. They wanted the so-called 'entertainments' to continue, so as not to undermine the morale of the population too much. However, adjustments needed to be made and new roads were discovered that are still part of the route today.",
  },
  {
    race: "tour-de-france",
    year: 1919,
    label: "The first world war had just ended, and a lot of pre-war favorites had lost their lives on the battlefield. The survivors had little opportunity to train or race during war, and were therefore in poor condition. Partly because of this, there were only 69 participants at the start in Paris."
  },
  {
    race: "tour-de-france",
    year: 2018,
    label: "In 2018, the UCI introduced a new rule that the maximum number of riders per team in a Grand Tour was reduced from 9 to 8. This was done to reduce the number of riders in the peloton and to increase the safety."
  },
  {
    race: "giro-d-italia",
    year: 2018,
    label: "In 2018, the UCI introduced a new rule that the maximum number of riders per team in a Grand Tour was reduced from 9 to 8. This was done to reduce the number of riders in the peloton and to increase the safety."
  },
  {
    race: "vuelta-a-espana",
    year: 2018,
    label: "In 2018, the UCI introduced a new rule that the maximum number of riders per team in a Grand Tour was reduced from 9 to 8. This was done to reduce the number of riders in the peloton and to increase the safety."
  }

]

```

### Measuring the madness: how tough was it?
Every race tells a story — not just of who won, but how hard it was to win. In this section, we dive into the details that define the character of each race.
Use the toggle to switch between **total distance** and **average speed** to explore how these iconic races have evolved.
Were they longer in the past? Has the pace picked up over the decades?
We even highlight the top 3 fastest or longest editions, along with periods like the World Wars that left their mark on the sport.


```js
const selectedMetric = Mutable("Distance");
const switcherElement = createSwitcher(
  ["Distance", "Average Speed", "Nr. of participants"],
  (value) => {
    selectedMetric.value = value;
  }
);

const metricMap = {
  "Distance": { value: "distance", label: "Distance (km)", color: "black", unit: "km" },
  "Average Speed": { value: "average_speed", label: "Average Speed (km/h)", color: "black", unit: "km/h" },
  "Nr. of participants": { value: "participants", label: "Number of participants", color: "black", unit: "" },
};
```


<div class="card">
    <div style="display: flex; justify-content: flex-end;">
      ${switcherElement}
    </div>
    <div class="plot-container-wrapper">
      ${resize((width) => raceDetails(selectedRace, metricMap[selectedMetric], { width }))}
    </div>
</div>


<style>

.plot-container-wrapper {
  aspect-ratio: 100 / 35; 
  width: 100%;      /* Ensure width is set for aspect-ratio to work */
  overflow: hidden; /* Prevent temporary overflow during render */
}

button {
  border: none; 
  background: none;
}

.race-button {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 120px;
  height: 120px;
  background: white;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  border-radius: 8px;
  box-shadow: 2px 2px 6px rgba(0, 0, 0, 0.2);
  margin-bottom: 20px;
  }

.race-button:hover {
  transform: scale(1.05);
  box-shadow: 4px 4px 12px rgba(0, 0, 0, 0.3);
}

.race-button img {
  width: 100px;
  height: 100px;
  border-radius: 8px;
}

.race-button.selected {
  border: 3px solid #007BFF; /* Blue border for selected button */
  box-shadow: 0 0 8px rgba(0, 123, 255, 0.6); /* Subtle glow */
}

.content {
  display: flex;
  gap: 20px;
  align-items: flex-start;
}

.card {
  background: white;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 2px 2px 6px rgba(0, 0, 0, 0.2);
}

.map-container {
  flex: 2.5;
}

.ranking-container {
  flex: 0.5;
  min-width: 250px;
}

.ranking-list {
  list-style: none;
  padding: 0;
}

.ranking-list li {
  padding: 5px 0;
  border-bottom: 1px solid #ddd;
}
</style>
