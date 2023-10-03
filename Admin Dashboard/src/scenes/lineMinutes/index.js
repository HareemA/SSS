import { Box } from "@mui/material";
import Header from "../../components/Header";
import CountLiveMinute from "../../components/CountLiveMinute";

const liveCountMinute = () => {
  return (
    <Box m="20px">
      <Header title="LIVE COUNT (MIN MAX)/ MINUTE" subtitle=" Min Max Person Count | Minute" />
      <Box height="75vh">
        <CountLiveMinute />
      </Box>
    </Box>
  );
};

export default liveCountMinute;