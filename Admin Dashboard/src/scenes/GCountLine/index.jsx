import { Box } from "@mui/material";
import Header from "../../components/Header";
import GCountLineChart from "../../components/GCountLineChart";

const GLine = () => {
  return (
    <Box m="20px">
      <Header title="Daily Group Count" subtitle="No of Groups" />
      <Box height="75vh">
        <GCountLineChart />
      </Box>
    </Box>
  );
};

export default GLine;