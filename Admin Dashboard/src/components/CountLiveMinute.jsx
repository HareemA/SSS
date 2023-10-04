import { ResponsiveLine } from "@nivo/line";
import { useTheme } from "@mui/material";
import { tokens } from "../theme";
import React, { useState, useEffect } from "react";
import { useApi } from "../scenes/global/ApiContext";

const CountLiveMinute = ({ isCustomLineColors = false, isDashboard = false }) => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  const { count, time } = useApi();

  // State to store the line chart data
  const [chartData, setChartData] = useState([
    {
      id: "maxCount",
      data: [{ x: 0, y: 0 }], // Initialize with a single data point
    },
    {
      id: "minCount",
      data: [{ x: 0, y: 0 }], // Initialize with a single data point
    },
  ]);

  // State variables to track maximum and minimum values within a minute
  let maxCountWithinMinute = count;
  let minCountWithinMinute = count;
  
  // State to track the number of data points added
  const [dataPointCount, setDataPointCount] = useState(0);

  // Timer to reset maximum and minimum values and update chart data at the end of each minute
  useEffect(() => {
    const timer = setInterval(() => {
      // Update maximum and minimum values at the end of each minute
      const newMaxCountDataPoint = {
        x: time,
        y: maxCountWithinMinute,
      };
      const newMinCountDataPoint = {
        x: time,
        y: minCountWithinMinute,
      };

      // Add the maximum and minimum values to the chart data
      const newChartData = [...chartData];
      newChartData[0].data.push(newMaxCountDataPoint);
      newChartData[1].data.push(newMinCountDataPoint);

      // Limit the number of data points to keep on the chart (e.g., 10 data points)
      if (newChartData[0].data.length > 10) {
        newChartData[0].data.shift();
        newChartData[1].data.shift();
      }

      setChartData(newChartData);

      // Reset maximum and minimum values for the next minute
      maxCountWithinMinute = count;
      minCountWithinMinute = count;
      
      // Increment dataPointCount
      setDataPointCount(dataPointCount + 1);
    }, 1000); // Reset every 60 seconds (1 minute)

    return () => clearInterval(timer); // Cleanup timer on unmount
  }, [chartData, count, time, dataPointCount]);

  // Use useEffect to continuously update the maximum and minimum values when new API data arrives
  useEffect(() => {
    // Update maximum and minimum values for the current minute
    if (count > maxCountWithinMinute) {
      maxCountWithinMinute = count;
    }
    if (count < minCountWithinMinute) {
      minCountWithinMinute = count;
    }
  }, [count]);


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
            stacked: true,
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

export default CountLiveMinute;
