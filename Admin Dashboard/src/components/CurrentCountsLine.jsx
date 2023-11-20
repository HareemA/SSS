import { ResponsiveLine } from "@nivo/line";
import { useTheme } from "@mui/material";
import { tokens } from "../theme";
import React, { useState, useEffect } from "react";
import { useApi } from "../scenes/global/ApiContext";
import { API_IP } from "../config";

const CurrentCountsLine = ({ isCustomLineColors = false, isDashboard = false }) => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  const { apiData } = useApi();
  const { count, groupCount, time } = apiData;


  // State to store the line chart data
  const [chartData, setChartData] = useState([
    {
      id: "count",
      data: [], // Initialize with an empty array
    },
    {
      id: "groupCount",
      data: [], // Initialize with an empty array
    },
  ]);

  // Use useEffect to update the chart data when new API data arrives
  useEffect(() => {
    // Create a new data point with the current time and values

    const newGroupCountDataPoint = {
        x: time,
        y: groupCount,
      };

    const newCountDataPoint = {
      x: time,
      y: count,
    };


    // Create a copy of the chart data and update it with the new data point
    const newChartData = [...chartData];
    newChartData[0].data.push(newCountDataPoint);
    newChartData[1].data.push(newGroupCountDataPoint);

    // Limit the number of data points to keep on the chart (e.g., 10 data points)
    if (newChartData[0].data.length > 10) {
      newChartData[0].data.shift();
    }

    if (newChartData[1].data.length > 10) {
      newChartData[1].data.shift();
    }

    setChartData(newChartData);
  }, [time, count, groupCount]);

  return (
    <ResponsiveLine
      data={chartData}
      theme={{
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
        tooltip: {
          container: {
            color: colors.primary[500],
          },
        },
      }}
      colors={{ scheme: "category10" }}
      margin={{ top: 50, right: 110, bottom: 50, left: 60 }}
      xScale={{ type: "point" }}
      yScale={{
        type: "linear",
        min: "auto",
        max: "auto",
        stacked: false,
        reverse: false,
      }}
      yFormat=" >-.2f"
      curve="catmullRom"
      axisTop={null}
      axisRight={null}
      axisBottom={{
        orient: "bottom",
        tickSize: 0,
        tickPadding: 5,
        tickRotation: 0,
        legend: isDashboard ? undefined : "transportation", // added
        legendOffset: 36,
        legendPosition: "middle",
      }}
      axisLeft={{
        orient: "left",
        // tickValues: 5, // added
        // format: e => Math.floor(e) === e && e,
        tickSize: 3,
        tickPadding: 5,
        tickRotation: 0,
        legend: isDashboard ? undefined : "count", // added
        legendOffset: -40,
        legendPosition: "middle",
      }}
      enableGridX={true}
      enableGridY={true}
      pointSize={8}
      pointColor={{ theme: "background" }}
      pointBorderWidth={2}
      pointBorderColor={{ from: "serieColor" }}
      pointLabelYOffset={-12}
      useMesh={true}
      legends={[
        {
          anchor: "bottom-right",
          direction: "column",
          justify: false,
          translateX: 100,
          translateY: 0,
          itemsSpacing: 0,
          itemDirection: "left-to-right",
          itemWidth: 80,
          itemHeight: 20,
          itemOpacity: 0.75,
          symbolSize: 12,
          symbolShape: "circle",
          symbolBorderColor: "rgba(0, 0, 0, .5)",
          effects: [
            {
              on: "hover",
              style: {
                itemBackground: "rgba(0, 0, 0, .03)",
                itemOpacity: 1,
              },
            },
          ],
        },
      ]}
    />
  );
};

export default CurrentCountsLine;
