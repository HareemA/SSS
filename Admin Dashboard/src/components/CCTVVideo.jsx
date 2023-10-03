import React from "react";
import { useTheme } from "@mui/material";
import { tokens } from "../theme";
import { useApi } from "../scenes/global/ApiContext"; // Import the useApi hook
import Slider from "@mui/material/Slider";


const CCTVVideo = ({ isDashboard = false, height }) => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

  const { apiData, sliderValue, updateSliderValue } = useApi();

  const handleSliderChange = (event, newValue) => {
    //updateSliderValue(newValue);
  };

  const handleSliderChangeCommitted = (event, newValue) => {
    updateSliderValue(newValue);
  };

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
      <div className="slider-container">
        <Slider
          value={sliderValue}
          onChange={handleSliderChange}
          onChangeCommitted={handleSliderChangeCommitted}
          min={0}
          max={100}
          step={1}
          valueLabelDisplay="auto"
          valueLabelFormat={(value) => `${value}%`}
          defaultValue={35}
        />
      </div>

    </div>
  );
};

export default CCTVVideo;
