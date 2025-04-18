```js
const data = await FileAttachment('data/peloton.json').json();
```

# Inside the WorldTour-Peloton
The World Tour peloton is a diverse and dynamic group of athletes, each with their own story, background, and journey to the top of professional cycling. In this section, we take a closer look at the riders who make up this elite group. Through visualizations of their ages, nationalities, teams, and other key factors, we uncover the trends and patterns that define the makeup of the peloton. Explore how cycling has become a truly global sport and discover the individuals powering the races that captivate audiences around the world.

## Tour around the world
To gain insight into the global reach of professional cycling, we explore the number of riders representing each country in the World Tour peloton. The map below visualizes the distribution of riders across countries for the selected year, highlighting the extent of cycling's global presence.

```js
// Year slider
const minYear = Math.min.apply(null, Object.keys(data.nations).map(str => +str));
const maxYear = Math.max.apply(null, Object.keys(data.nations).map(str => +str));
const selectedYear = view(Inputs.range([minYear, maxYear], {step: 1, value: maxYear}));
```

```js
// World map
const world = await d3.json("https://cdn.jsdelivr.net/npm/world-atlas@2/countries-50m.json");
const countries = topojson.feature(world, world.objects.countries);

// Mutable stores to keep track of the selected nation id and name on the map
const selectedNationId = Mutable("");
const selectedNationName = Mutable("");

// Define a function that creates a map of the world with the number of riders per nation
function nationsWorldTourMap({ width } = {}) {
    // Filter based on the selected year
    const nations = Object.values(data.nations[selectedYear]);

    // Define a color scale
    const color = d3.scaleSequentialLog(d3.interpolateBlues).domain([1, d3.max(nations, nation => nation.riders.length)]);

    // Create an SVG element
    const svg = d3.create("svg")
        .attr("width", width)
        .attr("height", width / 2.5)
        .call(d3.zoom().scaleExtent([1, 5]) // Allow zooming between 1x and 5x
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
            const nation = nations.find(nation => nation.ison === +d.id);
            return nation ? color(nation.riders.length) : "#eee";
        })
        .on("click", (event, d) => {
        if (selectedNationId.value === +d.id) {
            selectedNationId.value = "";
            selectedNationName.value = "";
        } else {
            selectedNationId.value = +d.id;
            selectedNationName.value = d.properties.name;
        }
        })
        .attr("stroke", "white")
        .attr("stroke-width", 0.7)
        .append("title")
        .text(d => {
            const nation = nations.find(nation => nation.ison === +d.id);
            return nation ? `${d.properties.name}: ${nation.riders.length} riders` : `${d.properties.name}: No riders`;
        });

  return html`
  <div class="map-container">
    ${svg.node()}
  </div>`;
}
```

```js
// Function to display the list with riders of this country in the selected year
function ridersList({ width } = {}) {
    if (selectedNationId == "") return html`<p><strong>Select a country on the map to see the riders</strong></p>`;

    const nation = Object.values(data.nations[selectedYear]).filter(nation => nation.ison == selectedNationId)[0];
    const riders = Object.values(data.riders[selectedYear]).filter(rider => rider.nationality == nation.nationality);

    return html`
        <div class="ranking-container" style="max-width: ${width}px; max-height: ${width * 1.35}px; overflow-y: auto;">
            ${selectedNationId && selectedNationName ? html`<h3><strong>${selectedNationName} (Total: ${riders.length} ${riders.length !== 1 ? 'riders' : 'rider'})</strong></h3>` : ''}
            ${riders.map(rider => html`<li><strong>${rider.name}</strong></li>`)}
        </ul>
    `;
}
```

<div>
    <div class="content">
        <div class="card map-container">
            ${resize((width) => nationsWorldTourMap({width}))}
        </div>
        <div class="card ranking-container">
            ${resize((width) => ridersList({width}))}
        </div>
    </div>
</div>

By sliding over the years, it is clear that the number of countries represented in the World Tour peloton has been increasing over time. This trend reflects the global nature of professional cycling and the sport's growing popularity in different regions around the world. But of course it is not only about riding for a country, it is also about winning. In the next two graphs, we take a look at the winners. The first one shows the top 10 nations with the most wins in the selected year, showing how dominant certain countries are in the world of cycling. The second one shows the podium of the riders with the most wins in the selected year, highlighting the individual achievements of these athletes.

```js
// Define a function that creates a line plot of the number of different nationalities in the World Tour peloton over the years
function topWinnersBarPlot({ width } = {}) {
    const nations = Object.values(data.nations[selectedYear])
        .filter(nation => (nation.wins || 0) > 0)
        .sort((a, b) => d3.descending(a.wins || 0, b.wins || 0))
        .slice(0, 10); // Top 10 nations
    return Plot.plot({
        width,
        height: width * 0.6,
        marginLeft: 100,
        x: { label: "Wins", type: "linear" },
        y: { label: null, domain: nations.map(nation => nation.name) },
        marks: [
        Plot.barX(nations, { 
            x: "wins", 
            y: "name", 
            fill: "steelblue", 
        }),

        // The text labels
        Plot.text(nations, {
            x: nation => nation.wins + 0.2, // Slightly offset to the right of the bar
            y: "name",
            text: nation => nation.wins,
            fill: "black",
            textAnchor: "start",
            fontWeight: "bold",
            fontSize: 12
        })
        ],
        title: `Top 10 winning nations in ${selectedYear}`
    });
}
```

```js
function verticalPodium({width} = {}) {
    // 1. Get the top 3 riders from the selected year
    let top3 = data.wins.top3[selectedYear];
    
    // Update so that picture contains the correct url: 'https://www.procyclingstats.com' + d.picture
    top3 = top3.map(d => ({ ...d, picture: 'https://www.procyclingstats.com/' + d.picture }));

    // 2. Define podium metadata (heights, colors) and assign to riders
    const maxHeight = 2.7;
    const maxWins = Math.max(...top3.map(d => d.number_of_wins));

    top3 = top3.map(d => {
        let normalizedHeight = (d.number_of_wins / maxWins) * maxHeight;
        return {
            ...d,
            podium_height: normalizedHeight,
            podium_color: d.rank === 1 ? "gold" : d.rank === 2 ? "silver" : d.rank === 3 ? "#cd7f32" : "grey"
        };
    });

    // 3. Reorder for visual podium layout: [2nd, 1st, 3rd]
    const riderRankMap = new Map(top3.map(d => [d.rank, d]));
    let podiumLayout = [
        riderRankMap.get(2), // 2nd place
        riderRankMap.get(1), // 1st place
        riderRankMap.get(3)  // 3rd place
    ];

    // 4. Define constants for image placement
    const podiumImageHeightRelative = 0.8;
    const podiumImageWidthPixels = (width / podiumLayout.length) * 0.6 || 60;

    return Plot.plot({
        width: width,
        height: width * 0.6,
        x: {
            domain: podiumLayout.map(d => d.rider_name),
            label: null,
            tickSize: 0,    // Hide tick marks
            padding: 0.2    // Space between podium blocks
        },
        y: {
            domain: [0, 4], // Fixed domain [0, max_podium_height + image_space]
            axis: null      // Hide the y-axis
        },
        marks: [
            // Podium Bars/Blocks
            Plot.barY(podiumLayout, {
                x: "rider_name",
                y: "podium_height",   // Pre-defined podium height
                fill: "podium_color", // Pre-defined podium color
                stroke: "black",
                // Tooltip showing rank, name, nationality, and actual wins
                title: d => `${d.rider_name} (${d.nationality})\nWins: ${d.number_of_wins}`
            }),

            // Rider Images on top of the podium steps
            Plot.image(podiumLayout, {
                x: "rider_name",
                // Calculate y position: top of the bar + half the image's relative height
                // This centers the image vertically slightly above the bar's top edge
                y: d => d.podium_height + podiumImageHeightRelative / 2,
                width: podiumImageWidthPixels,
                src: "picture",
                title: d => `${d.rider_name} (${d.nationality})\nWins: ${d.number_of_wins}`,
            }),

        // Text Label for number of wins ON the podium step
        Plot.text(podiumLayout, {
            x: "rider_name",
            y: d => d.podium_height - 0.25, // Position inside the bar, near the top
            text: d => d.number_of_wins,    // Display the actual number of wins
            fill: "black",
            stroke: "white",                // Add outline for better visibility
            strokeWidth: 3,
            fontWeight: "bold",
            fontSize: 24,
            dy: -4                          // Fine-tune vertical position
        })
      ],
      title: `Podium of the riders with the most World-Tour wins in ${selectedYear}`,
    });
};
```

<div class="grid grid-cols-2">
  <div class="card">
    ${resize((width) => topWinnersBarPlot({width}))}
  </div>
  <div class="card">
    ${resize((width) => verticalPodium({width}))}
  </div>
</div>

## Age is just a number
```js
// Define a function that creates a bar chart of the distribution of the age of the riders in the World Tour peloton over the years
function ageHistogram({width} = {}) {
  var dataList = [];
  Object.values(data.riders[selectedYear]).forEach(rider => {
      // Subtract the difference between the current year and the selected year
      // from the rider's age to get the age in the selected year
      if (rider.birthdate){
          const age = selectedYear - +rider.birthdate.split('-')[0];
          const status = (data.wins.all[selectedYear][rider.name.replace(/\s+/g, ' ').toUpperCase()]) > 0 ? "winner" : "non-winner";

          // Make sure it is a valid age (> 14):
          if (age > 14) {
            dataList.push({age, status});
          }
      }
  });

  // Sort so "non-winner" comes first -> they are drawn later (on top)
  dataList.sort((a, b) => a.status === "winner" ? -1 : 1);

  return Plot.plot({
    width: width,
    height: width / 2,
    x: { label: 'Age', type: 'linear' },
    y: { label: 'Number of riders', type: 'linear' },
    color: {
      legend: true,
      domain: ["winner", "non-winner"],
      range: ["gold", "steelblue"] // green for winners, red for non-winners
    },
    marks: [
      Plot.rectY(
        dataList,
        Plot.binX(
          {y: "count"},
          {
            x: d => d.age,
            fill: d => d.status,
            thresholds: Array.from({length: 100}, (_, i) => i)
          }
        )
      )
    ],
    title: "Age distribution of the active riders in " + selectedYear
  })
};
```

<div class="grid grid-cols-2">
  <div class="card">
    ${resize((width) => ageHistogram({width}))}
  </div>
</div>

<style>
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
