import React from "react";
import { useTheme } from "@mui/material";
import { ResponsiveBar } from "@nivo/bar";
import { tokens } from "../theme";
import { useState, useEffect } from "react";
import { API_IP } from "../config";


const EngagementBarGraph = ({ isDashboard = false }) => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

  const [chartData, setChartData] = useState([
    {
      metric: "Max",
      value: 0,
    },
    {
      metric: "Min",
      value: 0,
    },
    {
      metric: "Avg",
      value: 0,
    },
  ]);

  useEffect(() => {
    const fetchGenderBarData = async () => {
      try {
        const response = await fetch(`${API_IP}/daily_engagement_bar`);

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const jsonData = await response.json();

        const genderBarData = jsonData;

        // Update the chart data with the latest values from the API
        setChartData(genderBarData);
        // console.log("Gender Bar Data: ",genderBarData);
      } catch (error) {
        console.error('Error fetching gender pie chart data:', error);
      }
    };

    // Fetch gender pie chart data initially and then every x minutes
    fetchGenderBarData();
    const intervalId = setInterval(fetchGenderBarData, 6000);  


    return () => clearInterval(intervalId);
  }, []);

  const customColors = ['#065e91', '#8eb7de', '#0f6abf'];

  return (
    <ResponsiveBar
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
      data={chartData}
      colors={customColors}
      keys={["value"]}
      indexBy="metric"
      layout="horizontal"
      margin={{ top: 50, right: 130, bottom: 50, left: 60 }}
      padding={0.3}
      valueScale={{ type: "linear" }}
      indexScale={{ type: "band", round: true }}
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
        modifiers: [["darker", 1.6]],
      }}
      axisBottom={{
        tickSize: 5,
        tickPadding: 5,
        tickRotation: 0,
        legend: isDashboard ? undefined : "Metric",
        legendPosition: "middle",
        legendOffset: 32,
      }}
      axisLeft={{
        tickSize: 5,
        tickPadding: 5,
        tickRotation: 0,
        legend: isDashboard ? undefined : "Value",
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
    //   legends={[
    //     {
    //       dataFrom: "keys",
    //       anchor: "bottom-right",
    //       direction: "column",
    //       justify: false,
    //       translateX: 120,
    //       translateY: 0,
    //       itemsSpacing: 2,
    //       itemWidth: 100,
    //       itemHeight: 20,
    //       itemDirection: "left-to-right",
    //       itemOpacity: 0.85,
    //       symbolSize: 20,
    //       effects: [
    //         {
    //           on: "hover",
    //           style: {
    //             itemOpacity: 1,
    //           },
    //         },
    //       ],
    //     },
    //   ]}
    layers={[
        "axes",
        "bars",
        "markers",
        "legends",
        // Remove the "grid" layer to remove horizontal lines below the bars
      ]}
      role="application"
      barAriaLabel={(e) =>
        `${e.id}: ${e.formattedValue} for Metric: ${e.indexValue}`
      }
    />
  );
};

export default EngagementBarGraph;
