```js
const data = await FileAttachment('data/peloton.json').json();
import { createYearSlider } from "./components/yearSlider.js";
```


<div style="display: flex; align-items: center; justify-content: space-between; width: 100%;">
  <h1 style="margin: 0;">Inside the WorldTour-Peloton</h1>
  <div>${yearSlider}</div>
</div>


The **World Tour peloton** is a diverse and dynamic group of athletes, each with their own story, background, and journey to the top of professional cycling. In this section, we take a closer look at the riders who make up this elite group. Through **clear visualizations** of their **nationalities, ages and other key factors**, we uncover the trends and patterns that define the makeup of the peloton. Explore how cycling has become a truly **global sport** and discover the **individuals** powering the races that captivate audiences around the world.

## Tour around the world
To explore the **global reach** of professional cycling, we visualize the **number of World Tour riders representing each country in a selected year**. The interactive map below highlights how widely the sport is embraced around the world. **Click on a country** to reveal a detailed list of its **riders for that year** — including their **names** and **number of victories** — offering deeper insight into each nation's contribution to the peloton and their success on the road.

```js
const minYear = Math.min.apply(null, Object.keys(data.nations).map(str => +str));
const maxYear = Math.max.apply(null, Object.keys(data.nations).map(str => +str));
const selectedYear = Mutable(maxYear);

// Year slider to select the year at the top of the page
const yearSlider = createYearSlider(
  maxYear,
  minYear,
  maxYear,
  (year) => {
    selectedYear.value = year;
  },
);
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
    let riders;
    if (selectedNationId == ""){
        riders = Object.values(data.riders[selectedYear]);
    } else {
        const nation = Object.values(data.nations[selectedYear]).filter(nation => nation.ison == selectedNationId)[0];
        if (nation){
          riders = Object.values(data.riders[selectedYear]).filter(rider => rider.nationality == nation.nationality);
        }
    }
  
    // Add the number of wins to the rider object
    if (riders && riders.length > 0){
      riders.forEach(rider => {
          rider.name = rider.name.replace(/\s+/g, ' '); // Normalize name format
          const firstName = rider.name.split(" ")[0].toUpperCase();
          const lastName = rider.name.split(" ").slice(1).join(" ").toUpperCase();
          const nameKey = `${lastName} ${firstName} `;
          rider.wins = data.wins.all[selectedYear][nameKey] || 0;
      });

      // Sort the riders by number of wins
      riders.sort((a, b) => d3.descending(a.wins, b.wins));
    }
  
    return html`
        <div class="ranking-container" style="max-width: ${width}px; max-height: ${width * 1.35}px; overflow-y: auto;">
            ${selectedNationId && selectedNationName ? html`<h3><strong>${selectedNationName} (Total: ${riders ? riders.length : 0} ${riders ? (riders.length !== 1 ? 'riders' : 'rider') : 'riders'})</strong></h3>` : html`<h3><strong>List of all World-Tour riders in ${selectedYear}</strong></h3>`}
            ${riders ? riders.map(rider => html`<li><strong>${rider.name}</strong>${(rider.wins != 0) ? `: ${rider.wins} ${(rider.wins == 1) ? "win" : "wins"}` : ""}</li>`) : ""}
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

As you slide through the years, a clear trend emerges: the **number of countries** represented in the World Tour peloton has **steadily increased**. This growth reflects the truly global nature of modern professional cycling and its rising popularity across diverse regions.

But cycling isn’t just about participation — it’s about performance. In the following two graphs, we shift our **focus to the winners**. The first chart highlights the **top 10 nations with the most victories** in the selected year, revealing the countries that dominate the sport. The second spotlights the **top three individual riders** by number of wins, celebrating the standout athletes who consistently cross the finish line first.
```js
// Define a function that creates a line plot of the number of different nationalities in the World Tour peloton over the years
function topWinnersBarPlot({ width } = {}) {
    const nations = Object.values(data.nations[selectedYear])
        .filter(nation => (nation.wins || 0) > 0)
        .sort((a, b) => d3.descending(a.wins || 0, b.wins || 0))
        .slice(0, 10) // Top 10 nations
        .map(n => ({
            ...n,
            flag_url: `https://flagcdn.com/w40/${n.nationality.toLowerCase()}.png`,
            title: `${n.name} (${n.wins} wins)`,
        }));

    return Plot.plot({
        width,
        height: width * 0.6,
        marginLeft: 30,
        x: { label: "Wins", type: "linear" , domain: [0, d3.max(nations, d => d.wins)]},
        y: { label: null, domain: nations.map(nation => nation.name.toUpperCase()), tickFormat: () => ""},  // Hide y-axis labels 
        marks: [
          Plot.barX(nations, { 
              x: "wins", 
              y: nation => nation.name.toUpperCase(),
              fill: "steelblue", 
              title: d => `${d.name.toUpperCase()} (${d.wins} wins)`,
          }),

          // The text labels
          Plot.text(nations, {
              x: nation => nation.wins + 0.1, // Slightly offset to the right of the bar
              y: nation => nation.name.toUpperCase(),
              text: nation => nation.wins,
              fill: "black",
              textAnchor: "start",
              fontWeight: "bold",
              fontSize: 12
          }),

          // Flags replacing the y-axis labels
          Plot.image(nations, {
              x: -d3.max(nations, d => d.wins) * 0.04, // Adjust as needed for spacing
              y: nation => nation.name.toUpperCase(),
              src: "flag_url",
              width: 20,
              height: 14,
              title: d => `${d.name.toUpperCase()}`,
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
            podium_color: d.rank === 1 ? "gold" : d.rank === 2 ? "silver" : d.rank === 3 ? "#cd7f32" : "grey",
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
            }),
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

In professional cycling, **age** plays an **intriguing role** in shaping an athlete’s journey. While peak physical condition is essential, there’s no fixed age for achieving success — champions can emerge both early and late in their careers.

In this section, we examine the **age distribution within the World Tour peloton** and explore how age relates to performance and victories.

The **first graph** visualizes the **overall age distribution** of riders, distinguishing between **winners and non-winners**. The **second graph** takes a broader view, showing **how the age of winners has evolved over time**. Together, these insights shed light on how age impacts success in the high-stakes world of professional cycling.

```js
// Define a function that creates a bar chart of the distribution of the age of the riders in the World Tour peloton over the years
function ageHistogram({width} = {}) {
  var dataList = [];
  Object.values(data.riders[selectedYear]).forEach(rider => {
      // Subtract the difference between the current year and the selected year
      // from the rider's age to get the age in the selected year
      if (rider.birthdate){
          const age = selectedYear - +rider.birthdate.split('-')[0];
          const riderName = rider.name.replace(/\s+/g, ' '); // Normalize name format
          const firstName = riderName.split(" ")[0].toUpperCase();
          const lastName = riderName.split(" ").slice(1).join(" ").toUpperCase();
          const status = (data.wins.all[selectedYear][`${lastName} ${firstName} `]) > 0 ? "Winner" : "Non-winner";

          // Make sure it is a valid age (> 14):
          if (age > 14) {
            dataList.push({age, status});
          }
      }
  });

  // Sort so "non-winner" comes first -> they are drawn later (on top)
  dataList.sort((a, b) => a.status === "Winner" ? -1 : 1);

  return Plot.plot({
    width: width,
    height: width / 2,
    x: { label: 'Age', type: 'linear' },
    y: { label: 'Number of riders', type: 'linear' },
    color: {
      legend: true,
      domain: ["Winner", "Non-winner"],
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

```js
function winHistogram({width} = {}) {
  var dataList = [];
    // Loop over all years
  Object.keys(data.riders).forEach(year => {
    Object.values(data.riders[year]).forEach(rider => {
      if (rider.birthdate) {
        const age = year - rider.birthdate.split('-')[0];
        const riderName = rider.name.replace(/\s+/g, ' ');
        const firstName = riderName.split(" ")[0].toUpperCase();
        const lastName = riderName.split(" ").slice(1).join(" ").toUpperCase();
        const wins = (data.wins.all[year] || {})[`${lastName} ${firstName} `] || 0;

        if (age > 14 && wins > 0) {
            dataList.push({age});
        }
      }
    });
  });

  return Plot.plot({
    width: width,
    height: width / 2,
    x: { label: 'Age', type: 'linear' },
    y: { label: 'Number of winners', type: 'linear' },
    color: {
      legend: true,
      domain: [""],
      range: ["white"] // green for winners, red for non-winners
    },
    marks: [
      Plot.rectY(
        dataList,
        Plot.binX(
          {y: "count"},
          {
            x: d => d.age,
            fill: "steelblue",
            thresholds: Array.from({length: 100}, (_, i) => i)
          }
        )
      )
    ],
    title: "Age distribution of the winners (All Time)"
  });
}
```

<div class="grid grid-cols-2">
  <div class="card">
    ${resize((width) => ageHistogram({width}))}
  </div>
  <div class="card">
    ${resize((width) => winHistogram({width}))}
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
