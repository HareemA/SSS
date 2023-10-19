import React, { createContext, useContext, useState, useEffect } from 'react';

const ApiContext = createContext();

export function useApi() {
  return useContext(ApiContext);
}

export function ApiProvider({ children }) {
  const [apiData, setApiData] = useState({
    frame: null,
    count: null,
    groupCount: null,
    time: null,
  });

  const [sliderValue, setSliderValue] = useState(35);

  const updateSliderValue = (value) => {
    setSliderValue(value);
  };

  // Function to fetch data from the API
  const fetchDataFromApi = async () => {
    try {
      const response = await fetch(`http://172.23.17.3:8080/get_latest_processed_frame/${sliderValue}`);  //http://172.23.17.3:8080/get_latest_processed_frame/${sliderValue}

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const jsonData = await response.json();

      setApiData({
        frame: jsonData.frame,
        count: jsonData.count,
        groupCount: jsonData.groupCount,
        time: jsonData.time,
      });
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  useEffect(() => {
    fetchDataFromApi(); // Fetch data initially

    // Set up a timer to fetch data every 5 seconds (5000 milliseconds)
    const interval = setInterval(fetchDataFromApi, 500);

    // Clean up the timer when the component unmounts
    return () => clearInterval(interval);
  }, [sliderValue]);

  const apiContextValue = {
    apiData,
    updateSliderValue,
  };

  return (
    <ApiContext.Provider value={apiContextValue}>
      {children}
    </ApiContext.Provider>
  );
}
