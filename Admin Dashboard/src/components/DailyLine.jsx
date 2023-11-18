import { ResponsiveLine } from "@nivo/line";
import React, { useState, useEffect } from "react";
import { useTheme } from "@mui/material";
import { tokens } from "../theme";

const DailyLine = ({ isCustomLineColors = false, isDashboard = false }) => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

  const [lineChartData, setLineChartData] = useState(null);

  const fetchData = async () => {
    try {
      const response = await fetch("http://192.168.18.132:8080/daily_line_chart");
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      const jsonData = await response.json();

      // Convert the received data into the required format
      const convertedData = [
        {
          id: "ENTERED",
          color: tokens("dark").redAccent[600],
          data: Object.keys(jsonData).map(interval => ({
            x: interval.split('-')[0],
            y: jsonData[interval].Enter === null ? 0 : jsonData[interval].Enter,
          })),
        },
        {
          id: "LEFT",
          color: tokens("dark").blueAccent[400],
          data: Object.keys(jsonData).map(interval => ({
            x: interval.split('-')[0],
            y: jsonData[interval].Enter === null ? 0 : jsonData[interval].Enter,
          })),
        },
        {
          id: "MIN",
          color: tokens("dark").greenAccent[600],
          data: Object.keys(jsonData).map(interval => ({
            x: interval.split('-')[0],
            y: jsonData[interval].Enter === null ? 0 : jsonData[interval].Enter,
          })),
        },
        {
          id: "MAX",
          color: tokens("dark").redAccent[300],
          data: Object.keys(jsonData).map(interval => ({
            x: interval.split('-')[0],
            y: jsonData[interval].Enter === null ? 0 : jsonData[interval].Enter,
          })),
        },
      ];

      setLineChartData(convertedData);
      // console.log(convertedData);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  useEffect(() => {
    fetchData(); // Initial fetch

    // Fetch data every hour (3600000 milliseconds)
    const intervalId = setInterval(() => {
      fetchData();
    }, 600); // Set the interval to a more reasonable value, e.g., 3600000 milliseconds (1 hour)

    // Clean up interval when the component unmounts
    return () => clearInterval(intervalId);
  }, []); // Fetch data once when the component mounts

  if (!lineChartData) {
    // Render loading or placeholder if data is not yet available
    return <div>Loading...</div>;
  }

  return (
    <ResponsiveLine
      data={lineChartData}
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
      colors={isDashboard ? { datum: "color" } : { scheme: "nivo" }} // added
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
        legend: isDashboard ? undefined : "time", // added
        legendOffset: 36,
        legendPosition: "middle",
      }}
      axisLeft={{
        orient: "left",
        //tickValues: 5, // added
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

export default DailyLine;
