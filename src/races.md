```js
const {winners} = await FileAttachment("data/races.json").json();
console.log(winners);
```

# Where winners are born

Welcome to an interactive journey through the most prestigious cycling races across the globe. Each button represents a major race, and by selecting one, you'll uncover intriguing insights into the history of its winners. On the left, a dynamic map highlights the countries that have produced the most winners for each race. On the right, you'll see a comprehensive list of all race victors.

Engage with the map by clicking on any country to filter the winners list by nation. To reset and view the complete list again, simply unclick a country. Explore how different countries have made their mark on the world of cycling!

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
      const totalWins = countryWins.get(+d.id) || 0;
      return totalWins > 0 ? color(totalWins) : "#eee";
    })
    .on("click", (event, d) => {
      if (selectedCountryId.value === d.id) {
        console.log("Country : ", d.properties.name);
        selectedCountryId.value = "";
        selectedCountryName.value = "";
      } else {
        console.log("Country selected 2: ", d.properties.name);
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
            ` : ''}

            ${sortedWinners.map(winner => html`
                <li><strong>${winner.name}</strong>: ${winner.wins} ${winner.wins > 1 ? 'wins' : 'win'}</li>
            `)}
        </ul>
    `;
}
```

```js
// Grid with buttons for each race
const buttons = Inputs.button(
  Object.keys(racesList).map(race => [html`
      <div class="race-button"}">
        <img src="${racesList[race]}" alt="${race}" />
      </div>`, 
      _ => race]
  ), {value: 'tour-de-france'});

// Selected race button
const selectedRace = Generators.input(buttons);
```

<div>
    ${display(buttons)}
    <div class="content">
        <div class="card map-container">
            ${resize((width) => winnersRacesMap(selectedRace, {width}))}
        </div>
        <div class="card ranking-container">
            <h2>${selectedRace.replace(/-/g, ' ').toUpperCase()}</h2>
            ${resize((width) => winnersRanking(selectedRace, {width}))}
        </div>
    </div>
</div>

<style>

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
