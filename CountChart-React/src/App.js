import React, { useState, useEffect } from 'react';
import './App.css';
import { LineChart, Line, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts';

function App() {
  // Initial state with default data
  const [data, setData] = useState([
    { count: 0, groupCount: 0, time: '' } // Default data
  ]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://192.168.18.132:8080/get_latest_processed_frame');

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const jsonData = await response.json();

        // Extract count and groupCount from the response
        const { count, groupCount, time } = jsonData;

        // Create a new data object with count, groupCount, and time
        const newData = { count, groupCount, time };

        // Add the new data to the state
        setData((prevData) => [...prevData, newData]);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    // Fetch data initially
    fetchData();

    // Set up a timer to fetch data every 5 seconds (5000 milliseconds)
    const interval = setInterval(fetchData, 1000);

    // Clean up the timer when the component unmounts
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="App">
      <h1>Real-Time Line Chart</h1>
      <ResponsiveContainer width="70%" height={400}>
        <LineChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 10 }}>
          <XAxis dataKey="time" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="groupCount" name="Group Count" stroke="#82ca9d" />
          <Line type="monotone" dataKey="count" name="Count" stroke="#8884d8" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export default App;