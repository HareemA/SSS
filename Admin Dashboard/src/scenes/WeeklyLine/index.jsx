import { Box } from "@mui/material";
import Header from "../../components/Header";
import WeeklyLine from "../../components/DailyLine";

const WeeklyLineChart = () => {
  return (
    <Box m="20px">
      <Header title="Weekly Stats" subtitle="This Week" />
      <Box height="75vh">
        <WeeklyLine />
      </Box>
    </Box>
  );
};

export default WeeklyLineChart;