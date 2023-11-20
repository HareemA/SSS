import { useTheme } from "@mui/material";
import { ResponsiveBar } from "@nivo/bar";
import { tokens } from "../theme";
import { mockBarData as data } from "../data/mockData";
import React, { useState, useEffect } from "react";
import { API_IP } from "../config";

const BarChart = ({ isDashboard = false }) => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

  const [chartData, setChartData] = useState([
    {
      time: "8:00",
      Men: 0,
      Women: 0,
      Unidentified: 0,
    },
    {
      time: "9:00",
      Men: 0,
      Women: 0,
      Unidentified: 0,
    },
    {
      time: "10:00",
      Men: 0,
      Women: 0,
      Unidentified: 0,
    },
  ]);

  useEffect(() => {
    const fetchGenderBarData = async () => {
      try {
        const response = await fetch(`${API_IP}/daily_gender_bar`);

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const jsonData = await response.json();

        const genderBarData = convertApiData(jsonData);

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

  const convertApiData = (data) => {
    // Sort the data based on the 'time' property in ascending order
    const sortedData = data.sort((a, b) => {
      const timeA = a.time;
      const timeB = b.time;
      return new Date('1970-01-01T' + timeA) - new Date('1970-01-01T' + timeB);
    });
  
    // Convert the sorted data into the desired format
    return sortedData.map(entry => {
      const convertedEntry = { time: entry.time };
  
      // Loop through keys other than 'time' and convert the data
      Object.keys(entry).forEach(key => {
        if (key !== 'time') {
          convertedEntry[key] = entry[key];
        }
      });
  
      return convertedEntry;
    });
  };
  

  const customColors = ['#065e91', '#8eb7de', '#0f6abf'];
  
  

  return (
    <ResponsiveBar
      data={chartData}
      colors={customColors}
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