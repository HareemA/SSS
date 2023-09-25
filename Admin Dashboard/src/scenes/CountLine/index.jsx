import { Box } from "@mui/material";
import Header from "../../components/Header";
import CountLineChart from "../../components/CountLineChart";

const Line = () => {
  return (
    <Box m="20px">
      <Header title="Daily Count" subtitle="Person Count" />
      <Box height="75vh">
        <CountLineChart />
      </Box>
    </Box>
  );
};

export default Line;