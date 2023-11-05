import { Box } from "@mui/material";
import Header from "../../components/Header";
import DailyLine from "../../components/DailyLine";

const DailyLineChart = () => {
  return (
    <Box m="20px">
      <Header title="Daily Stats" subtitle="Today" />
      <Box height="75vh">
        <DailyLine />
      </Box>
    </Box>
  );
};

export default DailyLineChart;