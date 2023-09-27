import React from "react";
import { useTheme } from "@mui/material";
import { tokens } from "../theme";
import { useApi } from "../scenes/global/ApiContext"; // Import the useApi hook

const CCTVVideo = ({ isDashboard = false, height }) => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

  const apiData = useApi(); // Use the useApi hook to access the API data

  if (!apiData.frame) {
    return <div>Loading...</div>; // You can replace this with a loading indicator or message
  }


  return (
    <div className="cctv-video">
      <div className="video-container">
        {/* Use apiData.frame instead of frameData.frame */}
        <img
          src={`data:image/jpeg;base64, ${apiData.frame}`}
          alt="Frame"
          height={height}
        />
      </div>
    </div>
  );
};

export default CCTVVideo;
