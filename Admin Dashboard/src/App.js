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
              {/* <Route path="/video" element={<Line />} /> */}
              <Route path="/video" element={<CCTV />} />
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
