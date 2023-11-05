import React from "react";
import { useTheme } from "@mui/material";
import { ResponsiveBar } from "@nivo/bar";
import { tokens } from "../theme";

const generateMockData = () => {
  return [
    {
      metric: "Max",
      value: Math.floor(Math.random() * 100),
    },
    {
      metric: "Min",
      value: Math.floor(Math.random() * 100),
    },
    {
      metric: "Avg",
      value: Math.floor(Math.random() * 100),
    },
  ];
};

const EngagementBarGraph = ({ isDashboard = false }) => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

  const data = generateMockData();

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
      data={data}
      keys={["value"]}
      indexBy="metric"
      layout="horizontal"
      margin={{ top: 50, right: 130, bottom: 50, left: 60 }}
      padding={0.3}
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
