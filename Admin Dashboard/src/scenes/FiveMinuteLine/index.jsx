import { Box } from "@mui/material";
import Header from "../../components/Header";
import FiveMinuteLine from "../../components/FiveMinuteLine";

const FiveMinuteLineChart = () => {
  return (
    <Box m="20px">
      <Header title="LIVE COUNTS" subtitle=" Person Count | Group Count" />
      <Box height="75vh">
        <FiveMinuteLine />
      </Box>
    </Box>
  );
};

export default FiveMinuteLineChart;