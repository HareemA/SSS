import React, { useState, useEffect } from "react";
import { useTheme } from "@mui/material";
import { tokens } from "../theme";

const CCTVVideo = ( {isDashboard = false,  height }) => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
  

  const [frameData, setFrameData] = useState({ frame: "", time: "" });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(
          "http://192.168.18.132:8080/get_latest_processed_frame/2"
        );

        if (!response.ok) {
          throw new Error("Network response was not ok");
        }

        const jsonData = await response.json();

        // Extract frame and time from the response
        const { frame, time } = jsonData;

        // Set the frame data in state
        setFrameData({ frame, time });
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    // Fetch data initially
    fetchData();

    // Set up a timer to fetch data every 5 seconds (5000 milliseconds)
    const interval = setInterval(fetchData, 5000);

    // Clean up the timer when the component unmounts
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="cctv-video" >
      <div className="video-container" >
      <img src={`data:image/jpeg;base64, ${frameData.frame}`} alt="Frame" height={height} />
      </div>
    </div>
  );
};

export default CCTVVideo;
