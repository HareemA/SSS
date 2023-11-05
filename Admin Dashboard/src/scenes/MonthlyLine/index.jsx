import { Box } from "@mui/material";
import Header from "../../components/Header";
import MonthlyLine from "../../components/MonthlyLine";

const MonthlyLineChart = () => {
  return (
    <Box m="20px">
      <Header title="Weekly Stats" subtitle="This Week" />
      <Box height="75vh">
        <MonthlyLine />
      </Box>
    </Box>
  );
};

export default MonthlyLineChart;