import React, { createContext, useContext, useState, useEffect } from 'react';

const ApiContext = createContext();

export function useApi() {
  return useContext(ApiContext);
}


export function ApiProvider({ children }) {
  const [apiData, setApiData] = useState({
    frame: null,
    inStore: 0,
    groupCount: 0,
    time: null,
    male:0,
    female:0,
    enter:0,
    exit:0,
    unknown:0

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
      const response = await fetch(`http://192.168.146.125:8080/get_data/${sliderValue}`);

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const jsonData = await response.json();

      // Update maximum and minimum values within a minute
      if (jsonData.inStore !== null) {
        setMaxCountWithinMinute((prevMax) => Math.max(prevMax, jsonData.inStore));
        setMinCountWithinMinute((prevMin) => (prevMin === 0 ? jsonData.inStore : Math.min(prevMin, jsonData.inStore)));
      }

      setApiData({
        frame: jsonData.frame,
        inStore: jsonData.inStore,
        groupCount: jsonData.group_count,
        time: jsonData.time,
        male: jsonData.male,
        female: jsonData.female,
        unknown: jsonData.unknown,
        enter: jsonData.enter,
        exit: jsonData.exit
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
