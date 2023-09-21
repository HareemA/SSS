import React, { useState, useEffect } from 'react';
import './App.css';
import { FrameDisplay, RealTimeLineChart } from './Components';

function App() {
  // Initial state with default data
  const [data, setData] = useState([
    { count: 0, groupCount: 0, time: '' } // Default data
  ]);

  // State for frame data
  const [frameData, setFrameData] = useState({ frame: '', time: '' });

  const [groupThreshold, setGroupThreshold] = useState(35);

  const handleGroupThresholdChange = (event) => {
    const newValue = event.target.value;
    setGroupThreshold(newValue);
  }

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`http://192.168.100.10:8080/get_latest_processed_frame/${groupThreshold}`);

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const jsonData = await response.json();

        // Extract count and groupCount from the response
        const { count, groupCount, time, frame } = jsonData;

        // Create a new data object with count, groupCount, and time
        const newData = { count, groupCount, time };

        // Add the new data to the state
        setData((prevData) => [...prevData, newData]);

        // Set the frame data in state
        setFrameData({ frame, time });
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    // Fetch data initially
    fetchData();

    // Set up a timer to fetch data every 5 seconds (5000 milliseconds)
    const interval = setInterval(fetchData, 100);

    // Clean up the timer when the component unmounts
    return () => clearInterval(interval);
  }, [groupThreshold]);

  return (
    <div className="App">
      <h1>Real-Time Line Chart</h1>
      <div className='container'>
        <FrameDisplay frameData={frameData} />
        <RealTimeLineChart data={data} />
        <div className="threshold-control">
          <label>Group Threshold:</label>
          <input
            type="range"
            min="0"
            max="100"
            value={groupThreshold}
            onChange={handleGroupThresholdChange}
          />
          <span>{groupThreshold}</span>
      </div>
    </div>
  </div>
  
  );
}

export default App;

