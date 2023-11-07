import React from 'react';
import { ApiProvider } from './scenes/global/ApiContext'; // Import ApiProvider from your ApiContext
import { ColorModeContext, useMode } from "./theme";
import { CssBaseline, ThemeProvider } from "@mui/material";
import { Routes, Route } from "react-router-dom";
import Topbar from "./scenes/global/Topbar";
import Sidebar from "./scenes/global/Sidebar";
import Dashboard from "./scenes/dashboard";
import Bar from "./scenes/bar";
// import Form from "./scenes/form";
import Line from "./scenes/CountLine";
import GLine from "./scenes/GCountLine";
import Pie from "./scenes/pie";
import CCTV from "./scenes/Video";
import CurrentCountsLine from "./scenes/liveCount";
import CountLiveMinute from "./scenes/lineMinutes";
import DailyLineChart from './scenes/DailyLine';
import WeeklyLineChart from './scenes/WeeklyLine';
import MonthlyLineChart from './scenes/MonthlyLine';
import FiveMinuteLineChart from './scenes/FiveMinuteLine';

function App() {
  const [theme, colorMode] = useMode();

  return (
    <ColorModeContext.Provider value={colorMode}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <div className="app">
          <Sidebar />
          <main className="content">
            <Topbar />
            <Routes>
              <Route path="/" element={<Dashboard />} />
              {/* <Route path="/form" element={<Form />} /> */}
              <Route path="/bar" element={<Bar />} />
              <Route path="/pie" element={<Pie />} />
              <Route path="/line_count" element={<Line />} />
              <Route path="/line_gCount" element={<GLine />} />
              <Route path="/liveCount" element={<CurrentCountsLine />} />
              <Route path="/video" element={<CCTV />} />
              <Route path="/liveCountMinute" element={<CountLiveMinute />} />
              <Route path="/DailyLineChart" element={<DailyLineChart />} />
              <Route path="/WeeklyLineChart" element={<WeeklyLineChart />} />
              <Route path="/MonthlyLineChart" element={<MonthlyLineChart />} />
              <Route path="/FiveMinuteLineChart" element={<FiveMinuteLineChart />} />
            </Routes>
          </main>
        </div>
      </ThemeProvider>
    </ColorModeContext.Provider>
  );
}

// Wrap your App component with ApiProvider
export default function WrappedApp() {
  return (
    <ApiProvider>
      <App />
    </ApiProvider>
  );
}
