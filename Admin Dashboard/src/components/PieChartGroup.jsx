import { ResponsivePie } from "@nivo/pie";
import { tokens } from "../theme";
import { useEffect, useState } from 'react';
import { useTheme } from "@mui/material";
import { useApi } from "../scenes/global/ApiContext";

const PieChartGroup = (isDashboard = false) => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

  const { apiData } = useApi();
  const { inStore, groupCount } = apiData;

  

  const [chartData, setChartData] = useState([
    {
      "id": "group",
      "label": "Group",
      "value": 0,
      "color": "hsl(41, 70%, 50%)"
    },
    {
      "id": "individual",
      "label": "Individual",
      "value": 0,
      "color": "hsl(339, 70%, 50%)"
    },
  ]);

  useEffect(() => {
    const intervalId = setInterval(() => {
      
      setChartData([
        {
          "id": "group",
          "label": `Group: ${apiData.groupCount}`,
          "value": apiData.groupCount ===0 ? 100 : apiData.groupCount,
          "color": "hsla(203, 100%, 50%, 0.9)"
        },
        {
          "id": "individual",
          "label": `Indiv : ${apiData.inStore}`,
          "value": apiData.groupCount ===0 ? 100 : apiData.groupCount,
          "color": "hsla(228, 100%, 50%, 0.9)"
        },
      ]);
    }, 600); // 5 minutes interval

    // Clear the interval on component unmount
    return () => clearInterval(intervalId);
  }, [apiData, "hsla(203, 100%, 50%, 0.9)" , "hsla(228, 100%, 50%, 0.9)" ]);

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
      innerRadius={0}
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
          itemsSpacing: 5,
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