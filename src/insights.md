```js
const {teamsInfo} = await FileAttachment("data/insights.json").json();
import {createSwitcher} from "./components/inputSwitch.js";
```

# Deeper Insights into the Peloton
Cycling isn't just about physical strength — it's also a complex web of strategies, technologies, and team dynamics. On this page, we dive deeper into the data to uncover patterns and correlations that shape race outcomes. From the bikes they ride to the diversity within their teams, let's explore what gives riders their edge.

### Equipment Choices: A Closer Look
Over the years, WorldTour teams have made distinct choices when it comes to the equipment they trust — from the bikes they ride to the wheels and groupsets that drive performance. These choices reflect not only technological partnerships and sponsorships but also evolving trends in the peloton.

In this section, we examine how often different brands have been used by teams between 2010 and 2025. By counting how many teams chose each brand in a given season, we get a sense of which manufacturers have maintained a strong presence in the pro peloton — and which ones have faded or emerged over time.

Use the switcher to explore the most frequently used bike brands, wheels, and groupsets. While popularity doesn’t always equate to performance, this breakdown highlights the brands that have earned the trust of the sport's top-tier teams year after year.

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
    <h2>Number of World-Tour teams using the branch for their equipment (2010-2025)</h2>
    ${switcherElement}
  </div>
  <div id="bike-brands" style="margin-bottom: 2rem;">
    ${resize((width) => absoluteNumbersEquipment({ width }))}
  </div>
</div>

### Performance by Equipment
In professional cycling, equipment isn't just a matter of preference — it can be a decisive factor in a team's success. From cutting-edge bikes to aerodynamic wheels and precision-engineered groupsets, every component contributes to performance on the road.

In this section, we explore how equipment choices correlate with team success by comparing the performance of teams using different brands. To ensure a fair comparison, we calculate the **average number of WorldTour wins** per season for teams using each brand. This is done by dividing the total number of wins by the number of seasons those teams used that brand.

By aggregating this data, we can identify which equipment is more commonly associated with winning performances.
**Of course, this doesn’t imply that the gear alone makes the difference — the strength, strategy, and budget of the teams using the equipment are key factors as well**. Still, it gives us a data-driven look into how certain brands align with competitive success.

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
    <h2>Average number of World-Tour wins per brand (2010-2025)</h2>
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
}

.header-with-switcher h2 {
  margin: 0;
  font-size: 1em;
}

</style>
