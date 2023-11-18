import { Box } from "@mui/material";
import Header from "../../components/Header";
import RepeatRatioPie from "../../components/RepeatRatioPie";

const RepeatRatioPieChart = () => {
  return (
    <Box m="20px">
      <Header title="Repeat Ratio" subtitle=" Pie Chart" />
      <Box height="75vh">
        <RepeatRatioPie />
      </Box>
    </Box>
  );
};

export default RepeatRatioPieChart;