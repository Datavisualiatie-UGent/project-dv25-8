```js
const {nations, ages} = await FileAttachment("data/peloton.json").json();
```

# Inside the WorldTour-Peloton
The World Tour peloton is a diverse and dynamic group of athletes, each with their own story, background, and journey to the top of professional cycling. In this section, we take a closer look at the riders who make up this elite group. Through visualizations of their ages, nationalities, teams, and other key factors, we uncover the trends and patterns that define the makeup of the peloton. Explore how cycling has become a truly global sport and discover the individuals powering the races that captivate audiences around the world.

## Tour around the world

To gain insight into the global reach of professional cycling, we explore the number of riders representing each country in the World Tour peloton. The map below visualizes the distribution of riders across countries for the selected year, highlighting the extent of cycling's global presence.

```js
// Compute the years available in the data set, first and latest year
const years = Object.keys(nations.ranking).map(d => +d);
const firstYear = Math.min(...years);
const latestYear = Math.max(...years);

// Create a selector for the years
const selector = view(Inputs.range([firstYear, latestYear], {step: 1, value: latestYear}));
```

```js	
const world = await d3.json("https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json");
const countries = topojson.feature(world, world.objects.countries);

// Define a function that creates a map of the world with the number of riders per country
function nationsWorldTourMap({ width } = {}) {
  const filteredData = nations.ranking[selector];
  console.log(filteredData);
  const color = d3.scaleSequentialLog(d3.interpolateBlues)
    .domain([1, d3.max(filteredData, d => d.number_riders)]);

  return Plot.plot({
    width,
    height: width / 2.5,
    projection: "equirectangular",
    marks: [
      Plot.geo(countries, { 
        fill: d => {
          const countryData = filteredData.find(e => e.country_iso3 === +d.id);
          return countryData ? color(countryData.number_riders) : "#eee";
        },
        title: d => {
          const countryData = filteredData.find(e => e.country_iso3 === +d.id);
          return countryData ? `${d.properties.name}: ${countryData.number_riders} riders` : d.properties.name;
        }
      }),
    ]
  });
}
```

<div class="card">
  ${resize((width) => nationsWorldTourMap({width}))}
</div>

By sliding over the years, it is clear that the number of countries represented in the World Tour peloton has been increasing over time. This trend reflects the global nature of professional cycling and the sport's growing popularity in different regions around the world. This can also be seen in the next visualization, which shows the number of different nationalities in the peloton over the years.

```js
// Define a function that creates a line plot of the number of different nationalities in the World Tour peloton over the years
function nationsOverYears({ width } = {}) {
  const data = Object.entries(nations.ranking).map(([year, countries]) => ({
    year: new Date(+year, 0, 1),
    number_countries: countries.length
  }));

  return Plot.plot({
    width,
    height: width / 2,
    x: { label: "Year", type: "time" },
    y: { label: "Number of Countries", type: "linear" },
    marks: [
      Plot.line(data, { x: "year", y: "number_countries", stroke: "steelblue", strokeWidth: 2 }),
      Plot.dot(data, { 
        x: "year", 
        y: "number_countries", 
        fill: "steelblue", 
        r: 2,
        channels: {Year: "year", Countries: "number_countries"},
        tip: {format: {Year: d => d.getFullYear(), Countries: true, stroke: true, x: false, y: false}}
      })
    ],
    title: "Number of different nationalities"
  });
}
```

<div class="grid grid-cols-2">
  <div class="card">
    ${resize((width) => nationsOverYears({width}))}
  </div>
</div>

## Age is just a number

```js	
// Compute the average age per year
const yearlyAverages = Object.entries(ages.average).map(([year, teams]) => ({
  year: new Date(+year, 0, 1),                    // Convert year to date
  average_age: d3.mean(teams, d => d.average_age)   // Compute mean age of teams
}));

// Define a function that creates a line plot of the average age of World Tour riders over the years
function averageAgeOverYears({ width } = {}) {
  return Plot.plot({
    width: width,
    height: width / 2,
    x: { label: "Year", type: "time" },
    y: { label: "Average Age", type: "linear" },
    marks: [
      Plot.line(yearlyAverages, { x: "year", y: "average_age", stroke: "steelblue", strokeWidth: 2 }),
      Plot.dot(yearlyAverages, { 
        x: "year", 
        y: "average_age", 
        fill: "steelblue", 
        r: 2,
        channels: {Year: "year", Age: "average_age"},
        tip: {format: {Year: d => d.getFullYear(), Age: true, stroke: true, x: false, y: false}}
      }),
    ],
    title: "Average age of World Tour riders over the years"
  });
}
```

```js	
// Function to parse age strings in the format "xx y + dd"
function parseAge(ageString) {
    // Extract numbers from the string
    const match = ageString.match(/(\d+)y(?: \+ (\d+)d)?/);
    
    if (!match) return null; // Handle invalid input

    let years = parseInt(match[1], 10);
    let days = match[2] ? parseInt(match[2], 10) : 0;
    
    // Convert days to years and add to total age
    return years + (days / 365);
}

// Compute the average age of the 10 youngest World tour riders per year
const yearlyYoungest = Object.entries(ages.youngest).map(([year, riders]) => {
  const filteredRiders = riders
    .map(d => parseAge(d.min_age))              // Convert to float age
    .filter(age => age !== null && age >= 15)   // Remove null and values < 15 (errors in data set)
    .slice(0, 10);                              // Take the first 10 valid values

  return {
    year: new Date(+year, 0, 1),                // Convert year to date
    min_age: d3.mean(filteredRiders)            // Compute mean
  };
});

// Define a function that creates a line plot of the average age of the 10 youngest World Tour riders over the years
function youngestAgeOverYears({ width } = {}) {
  return Plot.plot({
    width: width,
    height: width / 2,
    x: { label: "Year", type: "time" },
    y: { label: "Age", type: "linear" },
    marks: [
      Plot.line(yearlyYoungest, { x: "year", y: "min_age", stroke: "steelblue", strokeWidth: 2 }),
      Plot.dot(yearlyYoungest, { 
        x: "year", 
        y: "min_age", 
        fill: "steelblue", 
        r: 2,
        channels: {Year: "year", Age: "min_age"},
        tip: {format: {Year: d => d.getFullYear(), Age: true, stroke: true, x: false, y: false}}
      }),
    ],
    title: "Average age of 10 youngest World Tour riders over the years"
  });
}
```

<div class="grid grid-cols-2">
  <div class="card">
    ${resize((width) => averageAgeOverYears({width}))}
  </div>
  <div class="card">
    ${resize((width) => youngestAgeOverYears({width}))}
  </div>
</div>

<style>

</style>
