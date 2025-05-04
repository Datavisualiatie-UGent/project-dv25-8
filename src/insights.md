```js
const {teamsInfo, teamsDiversity} = await FileAttachment("data/insights.json").json();
import {createSwitcher} from "./components/inputSwitch.js";
```

# Deeper Insights into the Peloton
Cycling is about more than physical strength — it’s a sport shaped by strategy, technology, and teamwork. On this page, we take a closer look at the deeper factors that influence race outcomes. From the **bikes riders use** to the **diversity of their teams**, we examine what might set top performers apart from the rest.

### Equipment Choices: A Closer Look
Over the years, WorldTour teams have made distinct choices about the equipment they rely on — from bikes to wheels to groupsets. These decisions reflect not just performance needs, but also technological partnerships, sponsorships, and evolving trends within the peloton.

In this section, we track **how often different brands were used by teams from 2010 to 2025**. By counting how many teams selected each brand in a given season, we reveal which manufacturers have consistently maintained a strong presence — and which ones have faded or emerged over time.

Use the toggle to explore the most commonly used **bike brands**, **wheels**, and **groupsets (collections of mechanical components like brakes, derailleurs, and chains)**. While popularity doesn’t always guarantee performance, this overview highlights the brands that have earned the trust of pro cycling’s top teams, season after season.

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
    height: brandCounts.length * 25 + 50,
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
        fill: "steelblue",
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


<div>
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

In this section, we explore how equipment choices correlate with team success by comparing the performance of teams using different brands. To ensure a fair comparison, we calculate the **average number of WorldTour wins per season for teams using each brand**. This is done by dividing the total number of wins by the number of seasons those teams used that brand.

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

  return Plot.plot({
    width,
    height: equipmentStats.length * 25 + 50,
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


<div>
  <div class="header-with-switcher">
    <h2>Average number of World-Tour wins per brand (2010-2025)</h2>
    ${switcherElementBis}
  </div>
  <div id="bike-brands" style="margin-bottom: 2rem;">
    ${resize((width) => equipmentComparison({ width }))}
  </div>
</div>

```js
function teamsDiversityPlot({ width } = {}) {
  const teamsDiversityData = teamsDiversity.filter(d => d.nationalities > 0);
  return Plot.plot({
    width: 600,
    height: 400,
    x: {
      label: "Number of nationalities"
    },
    y: {
      label: "Number of wins"
    },
    marks: [
      Plot.dot(teamsDiversityData, {
        x: "nationalities",
        y: "wins",
        stroke: "black",
        fill: "steelblue",
        r: 3,
      }),

      Plot.tip(teamsDiversityData, Plot.pointer({
        x: "nationalities",
        y: "wins",
        title: (d) => `Team: ${d.team_name} (${d.year})\nNumber of nationalities: ${d.nationalities}\nNumber of wins: ${d.wins}`

      })),

      Plot.linearRegressionY(teamsDiversityData, {
        x: "nationalities",
        y: "wins",
        stroke: "red"
      }),
    ],
  });
}
```

### Team Diversity: A Winning Strategy?
In professional cycling, team dynamics go beyond training plans and equipment — diversity within a team may also influence its success. While performance depends on many factors, the variety of nationalities represented can shape how a team communicates, adapts, and competes.

In this section, we **analyze data from WorldTour teams** to examine whether there’s a **correlation between team diversity** — measured by the number of nationalities — and **the number of wins**. The idea is that a broader mix of backgrounds might bring a wider range of skills, strategies, and perspectives to the table.

The scatterplot below shows the relationship between nationality diversity and team victories. A **positive trend suggests** that **more diverse teams tend to win more often**. However, it's important to **interpret this carefully**: such teams are **often backed by larger budgets and international sponsors**, which can provide advantages beyond diversity alone. In other words, while diversity may contribute to success, it's often accompanied by greater resources, experience, and organizational support.

<div class="center-container">
  <div class="header-with-switcher" style="margin-top: 1rem;">
    <h2>Correlation between the diversity of teams and their performance (2000-2025)</h2>
  </div>
  <div style="margin-bottom: 2rem;">
    ${teamsDiversityPlot()}
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

.center-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

</style>
