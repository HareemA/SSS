import { ResponsiveLine } from "@nivo/line";
import React, { useState, useEffect } from "react";
import { useTheme } from "@mui/material";
import { tokens } from "../theme";
import { mockLineDataMonthly as data } from "../data/mockData";

const MonthlyLine = ({ isCustomLineColors = false, isDashboard = false }) => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

  const [lineChartData, setLineChartData] = useState(null);

  const fetchData = async () => {
    try {
      const response = await fetch("http://192.168.100.10:8080/monthly_line_chart");
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      const backendData = await response.json();
      console.log(backendData);

      if (!backendData || !backendData.Entered || !backendData.Left || !backendData.Min || !backendData.Max) {
        // Handle the case where the expected properties are not present
        throw new Error("Invalid data format");
      }

      // Convert the received data into the required format
      const labels = Array.from(
        { length: backendData.Entered.length },
        (_, i) => (i + 1).toString()
      );

      const convertedData = [
        {
          id: "Entered",
          color: tokens("dark").blueAccent[300],
          data: labels.map((label, index) => ({
            x: label,
            y: backendData.Entered[index] !== null ? backendData.Entered[index] : 0,
          })),
        },
        {
          id: "Left",
          color: tokens("dark").redAccent[600],
          data: labels.map((label, index) => ({
            x: label,
            y: backendData.Left[index] !== null ? backendData.Left[index] : 0,
          })),
        },
        {
          id: "Min",
          color: tokens("dark").greenAccent[600],
          data: labels.map((label, index) => ({
            x: label,
            y: backendData.Min[index] !== null ? backendData.Min[index] : 0,
          })),
        },
        {
          id: "Max",
          color: tokens("dark").redAccent[300],
          data: labels.map((label, index) => ({
            x: label,
            y: backendData.Max[index] !== null ? backendData.Max[index] : 0,
          })),
        },
      ];
      

      setLineChartData(convertedData);
      console.log(convertedData);
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


  const customColors2 = ['#326887', '#1885c4', '#8eb7de', '#0f6abf'];
  const customColors = ['#d9db95', '#9bdb95', '#95d7db', '#b1abed'];

  return (
    <ResponsiveLine
      data={lineChartData}
      colors={
                  theme.palette.mode === "dark"
                    ? customColors
                    : customColors2
                }
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

export default MonthlyLine;
