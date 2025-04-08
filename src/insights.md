```js
const {teamsInfo} = await FileAttachment("data/insights.json").json();
import {createSwitcher} from "./components/inputSwitch.js";
```

# Deeper Insights into the Peloton
Cycling isn't just about physical strength — it's also a complex web of strategies, technologies, and team dynamics. On this page, we dive deeper into the data to uncover patterns and correlations that shape race outcomes. From the bikes they ride to the diversity within their teams, let's explore what gives riders their edge.

```js

function absoluteNumbersEquipment({ width } = {} ){
    // Filter the teamInfo data to include only teams with a bike brand, wheels, or groupset
    const filteredTeamsInfo = teamsInfo.filter(d => d.bike && d.wheels && d.groupset);
    
    // Aggregate total number of teams with this brand
    const brandCounts = Array.from(
        d3.rollup(
            filteredTeamsInfo,
            v => v.length,
            d => selectedEquipment === "Bike Brand" ? d.bike : selectedEquipment === "Wheels" ? d.wheels : d.groupset
        ),
        ([brand, count]) => ({ brand, count })
    ).sort((a, b) => d3.descending(a.count, b.count));

  return Plot.plot({
    width,
    height: brandCounts.length * 50 + 50,
    marginLeft: 120,
    marginRight: 50,
    x: { label: "Number of Teams", nice: true },
    y: {
      label: null,
      domain: brandCounts.map(d => d.brand),
    },
    marks: [
      Plot.barX(brandCounts, {
        x: "count",
        y: "brand",
        fill: "steelblue"
      }),
      Plot.text(brandCounts, {
        x: "count",
        y: "brand",
        text: d => d.count,
        dx: 5,
        dy: 3,
        textAnchor: "start",
        fill: "black"
      })
    ]
  });
}
```

```js
const selectedEquipment = Mutable("Bike Brand");
const switcherElement = createSwitcher(
  ["Bike Brand", "Wheels", "Groupset"],
  (value) => {
    selectedEquipment.value = value;
  }
);
```


<div class="chart-container">
  <div class="header-with-switcher">
    <h3>Brands Used by Teams for their Equipment</h3>
    ${switcherElement}
  </div>
  <div id="bike-brands" style="margin-bottom: 2rem;">
    ${resize((width) => absoluteNumbersEquipment({ width }))}
  </div>
</div>

### Performance by Equipment
In the world of professional cycling, the right equipment can be the difference between victory and defeat. From high-performance bikes to specialized wheels and cutting-edge groupsets, each component plays a role in shaping a team's success. In this section, we analyze the relationship between equipment and performance by comparing teams using specific brands of gear.

By calculating the average performance of teams riding with a particular brand, we ensure a fair comparison across different equipment types. This approach allows us to evaluate the impact of each brand on overall performance, taking into account the number of teams using it. By looking at the aggregated data, we can uncover potential correlations and gain deeper insights into how equipment choices may influence race outcomes.

```js
function equipmentComparison({ width } = {}) {
  // Filter the teamInfo data to include only teams with a bike brand, wheels, or groupset
  const filteredTeamsInfo = teamsInfo.filter(d => d.bike && d.wheels && d.groupset);

  // Aggregate total number of wins and number of teams for each equipment type
  const equipmentStats = Array.from(
    d3.rollup(
      filteredTeamsInfo,
      (v) => {
        const totalWins = v.reduce((acc, team) => acc + team.wins, 0);
        const teamCount = v.length;
        return { totalWins, teamCount };
      },
      d => selectedEquipmentBis === "Bike Brand" ? d.bike : selectedEquipmentBis === "Wheels" ? d.wheels : d.groupset
    ),
    ([equipment, { totalWins, teamCount }]) => ({
      equipment,
      averageWins: totalWins / teamCount // Calculate average wins per equipment type
    })
  ).sort((a, b) => d3.descending(a.averageWins, b.averageWins)); // Sort by average wins

  console.log(equipmentStats);

  return Plot.plot({
    width,
    height: equipmentStats.length * 50 + 50,
    marginLeft: 120,
    marginRight: 50,
    x: { label: "Average Wins per Equipment", nice: true },
    y: {
      label: null,
      domain: equipmentStats.map(d => d.equipment),
    },
    marks: [
      Plot.barX(equipmentStats, {
        x: "averageWins",
        y: "equipment",
        fill: "steelblue"
      }),
      Plot.text(equipmentStats, {
        x: "averageWins",
        y: "equipment",
        text: d => d.averageWins.toFixed(2), // Display average wins
        dx: 5,
        dy: 3,
        textAnchor: "start",
        fill: "black"
      })
    ]
  });
}
```

```js
const selectedEquipmentBis = Mutable("Bike Brand");
const switcherElementBis = createSwitcher(
  ["Bike Brand", "Wheels", "Groupset"],
  (value) => {
    selectedEquipmentBis.value = value;
  }
);
```


<div class="chart-container">
  <div class="header-with-switcher">
    <h3>Brands Used by Teams for their Equipment</h3>
    ${switcherElementBis}
  </div>
  <div id="bike-brands" style="margin-bottom: 2rem;">
    ${resize((width) => equipmentComparison({ width }))}
  </div>
</div>

<style>

.header-with-switcher {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
  gap: 1rem;
}

.header-with-switcher h2 {
  margin: 0;
  font-size: 1.5em;
}

</style>
