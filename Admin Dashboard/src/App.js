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


function App() {

  const [theme, colorMode] = useMode();


  return  ( 
    <ColorModeContext.Provider value = {colorMode}>
      <ThemeProvider theme={theme}>
        <CssBaseline/>
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
                
            </Routes>
            </main>
          
          </div>;
        </ThemeProvider>
    </ColorModeContext.Provider>
  )
      
    
  
}

export default App;
