import React, { useState, useEffect } from "react";
import { useTheme } from "@mui/material";
import { tokens } from "../theme";
import { useApi } from "../scenes/global/ApiContext"; // Import the useApi hook
import Slider from "@mui/material/Slider";


const CCTVVideo = ({ isDashboard = false, height }) => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

  const [apiData, setApiData] = useState({
    frame: null,
    time: null,
  });

  const [sliderValue, setSliderValue] = useState(35);

  const fetchDataFromApi = async () => {
    try {
      const response = await fetch(`http://192.168.100.10:8080/get_frame/${sliderValue}`);

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const jsonData = await response.json();

      setApiData({
        frame: jsonData.frame,
        time: jsonData.time,
      });
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  const handleSliderChange = (event, newValue) => {
    setSliderValue(newValue);
  };

  const handleSliderChangeCommitted = (event, newValue) => {
    fetchDataFromApi();
  };

  useEffect(() => {
    fetchDataFromApi(); // Fetch data initially

    // Set up a timer to fetch data every 5 seconds (5000 milliseconds)
    const interval = setInterval(fetchDataFromApi, 500);

    // Clean up the timer when the component unmounts
    return () => clearInterval(interval);
  }, [sliderValue]);

  if (!apiData.frame) {
    return <div>Loading...</div>;
  }
  


  return (
    <div className="cctv-video" style={{ padding: '10px' }}>
      <div className="video-container">
        {/* Use apiData.frame instead of frameData.frame */}
        <img
          src={`data:image/jpeg;base64, ${apiData.frame}`}
          alt="Frame"
          height={height}
        />
      </div>
      <div className="slider-container" style={{ padding: '10px' }}>
        <Slider
          value={sliderValue}
          onChange={handleSliderChange}
          onChangeCommitted={handleSliderChangeCommitted}
          min={0}
          max={250}
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
