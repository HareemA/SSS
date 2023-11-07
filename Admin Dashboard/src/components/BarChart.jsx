import { useTheme } from "@mui/material";
import { ResponsiveBar } from "@nivo/bar";
import { tokens } from "../theme";
import { mockBarData as data } from "../data/mockData";
import React, { useState, useEffect } from "react";
import { useApi } from "../scenes/global/ApiContext";

const BarChart = ({ isDashboard = false }) => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

  // const { apiData } = useApi();
  // const { male, female, unknown, time } = apiData;

  // const currentTime = new Date();
  // const formattedTime = currentTime.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' , second:'2-digit'});

  // const [chartData, setChartData] = useState([
  //   {
  //     time: formattedTime,
  //     Men: male,
  //     Women: 0,
  //     Unidentified: 0,
  //   },
  // ]);

  // useEffect(() => {
  //   const intervalId = setInterval(() => {
  //     // Create a new data entry
  //     const newDataEntry = {
  //       time: formattedTime,
  //       Men: male,
  //       Women: female,
  //       Unidentified: unknown,
  //     };
  
  //     // Create a copy of the chart data and update it with the new data entry
  //     setChartData((prevData) => {
  //       const newChartData = [newDataEntry, ...prevData.slice(0, 4)];
        
  //       // Limit the number of data entries to keep on the chart (e.g., 5 entries)
  //       if (newChartData.length > 5) {
  //         newChartData.pop(); // Use pop() instead of shift() to remove the last entry
  //       }
  
  //       return newChartData;
  //     });
  //   }, 100); // 1000 milliseconds = 1 second for testing, change it accordingly
  
  //   return () => clearInterval(intervalId);
  // }, [male, female, unknown]);

  return (
    <ResponsiveBar
      data={data}
      theme={{
        // added
        axis: {
          domain: {
            line: {
              stroke: colors.grey[100],
            },
          },
          legend: {
            text: {
              fill: colors.grey[100],
            },
          },
          ticks: {
            line: {
              stroke: colors.grey[100],
              strokeWidth: 1,
            },
            text: {
              fill: colors.grey[100],
            },
          },
        },
        legends: {
          text: {
            fill: colors.grey[100],
          },
        },
      }}
      keys={["Men", "Women", "Unidentified"]}
      indexBy="time"
      // margin={{ top: 50, right: 130, bottom: 50, left: 60 }}
      // padding={0.3}
      margin={{ top: 50, right: 30, bottom: 50, left: 60 }} // Adjusted right margin
      padding={0.5} // Adjusted padding for narrower bars
      valueScale={{ type: "linear" }}
      indexScale={{ type: "band", round: true }}
      colors={{ scheme: "nivo" }}
      defs={[
        {
          id: "dots",
          type: "patternDots",
          background: "inherit",
          color: "#38bcb2",
          size: 4,
          padding: 1,
          stagger: true,
        },
        {
          id: "lines",
          type: "patternLines",
          background: "inherit",
          color: "#eed312",
          rotation: -45,
          lineWidth: 6,
          spacing: 10,
        },
      ]}
      borderColor={{
        from: "color",
        modifiers: [["darker", "1.6"]],
      }}
      axisTop={null}
      axisRight={null}
      axisBottom={{
        tickSize: 5,
        tickPadding: 5,
        tickRotation: 0,
        legend: isDashboard ? undefined : "Day", // changed
        legendPosition: "middle",
        legendOffset: 32,
      }}
      axisLeft={{
        tickSize: 5,
        tickPadding: 5,
        tickRotation: 0,
        legend: isDashboard ? undefined : "Number", // changed
        legendPosition: "middle",
        legendOffset: -40,
      }}
      enableLabel={false}
      labelSkipWidth={12}
      labelSkipHeight={12}
      labelTextColor={{
        from: "color",
        modifiers: [["darker", 1.6]],
      }}
      legends={[
        {
          dataFrom: "keys",
          anchor: "bottom-right",
          direction: "column",
          justify: false,
          translateX: 120,
          translateY: 0,
          itemsSpacing: 2,
          itemWidth: 100,
          itemHeight: 20,
          itemDirection: "left-to-right",
          itemOpacity: 0.85,
          symbolSize: 20,
          effects: [
            {
              on: "hover",
              style: {
                itemOpacity: 1,
              },
            },
          ],
        },
      ]}
      role="application"
      barAriaLabel={function (e) {
        return e.id + ": " + e.formattedValue + " in Day: " + e.indexValue;
      }}
      barWidth={5}
    />
  );
};

export default BarChart;