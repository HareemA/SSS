import { Box } from "@mui/material";
import Header from "../../components/Header";
import CCTVVideo from "../../components/CCTVVideo";

const CCTV = () => {
  return (
    <Box m="30px">
      <Header title="CCTV Video" subtitle="Live" />
      <Box height="75vh">
        <CCTVVideo />
      </Box>
    </Box>
  );
};

export default CCTV;