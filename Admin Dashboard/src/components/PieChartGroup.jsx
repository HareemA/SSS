import { ResponsivePie } from "@nivo/pie";
import { tokens } from "../theme";
import { useEffect, useState } from 'react';
import { useTheme } from "@mui/material";
import { useApi } from "../scenes/global/ApiContext";

const PieChartGroup = (isDashboard = false) => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

  const [chartData, setChartData] = useState([
    { id: "Individual", label: "Individual", value: 1000, color: 'hsl(104, 70%, 50%)' },
    { id: "Group", label: "Group", value: 1000, color: 'hsl(162, 70%, 50%)' },
  ]);

  useEffect(() => {
    const fetchGRPieData = async () => {
      try {
        const response = await fetch('http://192.168.18.132:8080/group_ratio_pie');
  
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
  
        const jsonData = await response.json();
  
        const GRPieData = [
          {
            id: 'Individual',
            label: `Individual: ${jsonData.total_customers -( jsonData.customers_in_groups || 0)}`,
            value: jsonData.total_customers  === 0 ? 10000 : (jsonData.total_customers - jsonData.customers_in_groups),
            color: 'hsl(219, 55%, 64%)',
          },
          {
            id: 'Group',
            label: `Group: ${jsonData.customers_in_groups || 0}`,
            value: jsonData.customers_in_groups === 0 ? 10000 : jsonData.customers_in_groups ,
            color: 'hsl(162, 70%, 50%)',
          },
        ];
  
        // Update the chart data with the latest values from the API
        setChartData(GRPieData);
      } catch (error) {
        console.error('Error fetching repeat ratio pie chart data:', error);
      }
    };
  
    // Fetch gender pie chart data initially and then every x minutes
    fetchGRPieData();
    const intervalId = setInterval( fetchGRPieData, 6000);
  
    return () => clearInterval(intervalId);
  }, []);


  const customColors = ['#8eb7de', '#0f6abf'];



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
          itemsSpacing: 25,
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

export default PieChartGroup;