import { Box } from "@mui/material";
import Header from "../../components/Header";
import CurrentCountsLine from "../../components/CurrentCountsLine";

const liveCount = () => {
  return (
    <Box m="20px">
      <Header title="LIVE COUNTS" subtitle=" Person Count | Group Count" />
      <Box height="75vh">
        <CurrentCountsLine />
      </Box>
    </Box>
  );
};

export default liveCount;