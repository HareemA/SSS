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
    male:null,
    female:null,
    unknown:null
  });

  const [sliderValue, setSliderValue] = useState(35);

  // State variables to track maximum and minimum values within a minute
  const [maxCountWithinMinute, setMaxCountWithinMinute] = useState(0);
  const [minCountWithinMinute, setMinCountWithinMinute] = useState(0);

  const updateSliderValue = (value) => {
    setSliderValue(value);
  };

  // Function to fetch data from the API
  const fetchDataFromApi = async () => {
    try {
      const response = await fetch(`http://192.168.100.10:8080/get_data/${sliderValue}`);

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const jsonData = await response.json();

      // Update maximum and minimum values within a minute
      if (jsonData.count !== null) {
        setMaxCountWithinMinute((prevMax) => Math.max(prevMax, jsonData.count));
        setMinCountWithinMinute((prevMin) => (prevMin === 0 ? jsonData.count : Math.min(prevMin, jsonData.count)));
      }

      setApiData({
        frame: jsonData.frame,
        count: jsonData.count,
        groupCount: jsonData.groupCount,
        time: jsonData.time,
        male: jsonData.male,
        female: jsonData.female,
        unknown: jsonData.unknown
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
    maxCountWithinMinute,
    minCountWithinMinute,
    updateSliderValue,
  };

  return (
    <ApiContext.Provider value={apiContextValue}>
      {children}
    </ApiContext.Provider>
  );
}
