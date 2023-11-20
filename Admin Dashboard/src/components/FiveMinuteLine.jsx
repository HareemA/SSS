import { ResponsiveLine } from "@nivo/line";
import { useTheme } from "@mui/material";
import { tokens } from "../theme";
import React, { useState, useEffect } from "react";
import { useApi } from "../scenes/global/ApiContext";
import { API_IP } from "../config";

const FiveMinuteLine = ({ isCustomLineColors = false, isDashboard = false }) => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  const { apiData, maxCountWithinMinute, minCountWithinMinute } = useApi();
  const { enter, exit, time } = apiData;

  // State to store the line chart data
  const [chartData, setChartData] = useState([
    {
      id: "entry",
      data: [],
    },
    {
      id: "exit",
      data: [],
    },
    {
        id: "max",
        data: [],
      },
      {
        id: "min",
        data: [],
      },
  ]);


  useEffect(() => {
    const timeoutId = setTimeout(() => {
      // Create a new data point with the current time and values
      const newMaxCountDataPoint = {
        x: new Date().toLocaleTimeString(),
        y: maxCountWithinMinute,
      };
      const newMinCountDataPoint = {
        x: new Date().toLocaleTimeString(),
        y: minCountWithinMinute,
      };
      const newEnterPoint = {
        x: new Date().toLocaleTimeString(),
        y: enter,
      };
      const newExitPoint = {
        x: new Date().toLocaleTimeString(),
        y: exit,
      };

      // Create a copy of the chart data and update it with the new data point
      const newChartData = [...chartData];
      newChartData[0].data.push(newMaxCountDataPoint);
      newChartData[1].data.push(newMinCountDataPoint);
      newChartData[2].data.push(newEnterPoint);
      newChartData[3].data.push(newExitPoint);

      // Limit the number of data points to keep on the chart (e.g., 10 data points)
      if (newChartData[0].data.length > 5) {
        newChartData[0].data.shift();
        newChartData[1].data.shift();
        newChartData[2].data.shift();
        newChartData[3].data.shift();
      }

      // Set the new chart data
      setChartData(newChartData);
    }, 100); // 300000 milliseconds = 5 minute

    // Cleanup the timeout on component unmount or when dependencies change
    return () => clearTimeout(timeoutId);
  }, [maxCountWithinMinute, minCountWithinMinute]);
  

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
        margin={{ top: 50, right: 110, bottom: 50, left: 60 }}
        xScale={{ type: 'point' }}
        yScale={{
            type: 'linear',
            min: 'auto',
            max: 'auto',
            stacked: false,
            reverse: false
        }}
        yFormat=" >-.2f"
        curve="catmullRom"
        axisTop={null}
        axisRight={null}
        axisBottom={{
            tickSize: 5,
            tickPadding: 5,
            tickRotation: 0,
            legend: 'time',
            legendOffset: 26,
            legendPosition: 'middle'
        }}
        axisLeft={{
            tickSize: 3,
            tickPadding: 5,
            // format: e => Math.floor(e) === e && e,
            tickRotation: 0,
            legend: 'count',
            legendOffset: -36,
            legendPosition: 'middle'
        }}
        enableGridX={true}
        enableGridY={true}
        colors={{ scheme: 'category10' }}
        pointSize={10}
        pointColor={{ theme: "background" }}
        pointBorderWidth={2}
        pointBorderColor={{ from: 'serieColor' }}
        pointLabelYOffset={-12}
        enableArea={true}
        enableSlices="x"
        useMesh={true}
        legends={[
            {
                anchor: 'bottom-right',
                direction: 'column',
                justify: false,
                translateX: 100,
                translateY: 0,
                itemsSpacing: 0,
                itemDirection: 'left-to-right',
                itemWidth: 80,
                itemHeight: 20,
                itemOpacity: 0.75,
                symbolSize: 12,
                symbolShape: 'circle',
                symbolBorderColor: 'rgba(0, 0, 0, .3)',
                effects: [
                    {
                        on: 'hover',
                        style: {
                            itemBackground: 'rgba(0, 0, 0, .03)',
                            itemOpacity: 1
                        }
                    }
                ]
            }
        ]}
    />
  );
};

export default FiveMinuteLine;
