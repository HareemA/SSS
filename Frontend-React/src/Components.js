import React from 'react';
import './App.css';
import { LineChart, Line, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts';

export function FrameDisplay({ frameData }) {
  const { frame, time } = frameData;

  return (
    <div className="frame-display">
      <img src={`data:image/jpeg;base64, ${frame}`} alt="Frame" />
      <p>Timestamp: {time}</p>
    </div>
  );
}

export function RealTimeLineChart({ data }) {
  return (
    <ResponsiveContainer width="50%" height={400}>
      <LineChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 10 }}>
        <XAxis dataKey="time" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="groupCount" name="Group Count" stroke="#82ca9d" />
        <Line type="monotone" dataKey="count" name="Count" stroke="#8884d8" />
      </LineChart>
    </ResponsiveContainer>
  );
}
