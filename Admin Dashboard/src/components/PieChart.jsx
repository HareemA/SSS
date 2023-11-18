import { ResponsivePie } from "@nivo/pie";
import { tokens } from "../theme";
import { useTheme } from "@mui/material";
import React, { useState, useEffect } from "react";

const PieChart = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

  const [chartData, setChartData] = useState([
    { id: "Man", label: "Man", value: 10, color: 'hsl(104, 70%, 50%)' },
    { id: "Woman", label: "Woman", value: 10, color: 'hsl(162, 70%, 50%)' },
    { id: "Unidentified", label: "Unidentified", value: 10, color: 'hsl(291, 70%, 50%)' },
  ]);

  useEffect(() => {
    const fetchGenderPieData = async () => {
      try {
        const response = await fetch('http://192.168.18.132:8080/get_gender_pie_data');

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const jsonData = await response.json();

        const genderPieData = [
          {
            id: 'Man',
            label: `M : ${jsonData.male_percentage}%`,
            value: jsonData.male_percentage === 0 ? 10000 : jsonData.male_percentage,
            color: 'hsl(219, 55%, 64%)',
          },
          {
            id: 'Woman',
            label: `W : ${jsonData.female_percentage}%`,
            value: jsonData.female_percentage === 0 ? 10000 : jsonData.female_percentage,
            color: 'hsl(162, 70%, 50%)',
          },
          {
            id: 'Unidentified',
            label: `U : ${jsonData.unknown_percentage}%`,
            value: jsonData.unknown_percentage === 0 ? 10000 : jsonData.unknown_percentage,
            color: "hsl(274, 70%, 50%)",
          },
        ];

        // Update the chart data with the latest values from the API
        setChartData(genderPieData);
        console.log("Gender Pie Data: ",genderPieData);
      } catch (error) {
        console.error('Error fetching gender pie chart data:', error);
      }
    };

    // Fetch gender pie chart data initially and then every 10 minutes
    fetchGenderPieData();
    const intervalId = setInterval(fetchGenderPieData, 6000);  


    return () => clearInterval(intervalId);
  }, []);

  const customColors = ['#8eb7de', '#1d47e0', '#0f6abf'];

  return (
    <ResponsivePie
      data={chartData}
      colors={customColors}
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
      }}
      margin={{ top: 40, right: 80, bottom: 80, left: 80 }}
      innerRadius={0.5}
      padAngle={0.7}
      cornerRadius={3}
      activeOuterRadiusOffset={8}
      borderColor={{
        from: "color",
        modifiers: [["darker", 0.2]],
      }}
      arcLinkLabelsSkipAngle={10}
      arcLinkLabelsTextColor={colors.grey[100]}
      arcLinkLabelsThickness={2}
      arcLinkLabelsColor={{ from: "color" }}
      enableArcLabels={false}
      arcLabelsRadiusOffset={0.4}
      arcLabelsSkipAngle={7}
      arcLabelsTextColor={{
        from: "color",
        modifiers: [["darker", 2]],
      }}
      defs={[
        {
          id: "dots",
          type: "patternDots",
          background: "inherit",
          color: "rgba(255, 255, 255, 0.3)",
          size: 4,
          padding: 1,
          stagger: true,
        },
        {
          id: "lines",
          type: "patternLines",
          background: "inherit",
          color: "rgba(255, 255, 255, 0.3)",
          rotation: -45,
          lineWidth: 6,
          spacing: 10,
        },
      ]}
      legends={[
        {
          anchor: "bottom",
          direction: "row",
          justify: false,
          translateX: 0,
          translateY: 72,
          itemsSpacing: 10,
          itemWidth: 80,
          itemHeight: 18,
          itemTextColor: "#999",
          itemDirection: "left-to-right",
          itemOpacity: 1,
          symbolSize: 18,
          symbolShape: "circle",
          effects: [
            {
              on: "hover",
              style: {
                itemTextColor: "#000",
              },
            },
          ],
        },
      ]}
    />
  );
};

export default PieChart;
