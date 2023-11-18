import React, { createContext, useContext, useState, useEffect } from 'react';

const ApiContext = createContext();

export function useApi() {
  return useContext(ApiContext);
}


export function ApiProvider({ children }) {
  const [apiData, setApiData] = useState({
    entered:0,
    left:0,
    instore:0,
    returning:0,
    new:0,
    groups:0
  });

  const [sliderValue, setSliderValue] = useState(35);

  const fetchDataFromApi = async () => {
    try {
      const response = await fetch("http://192.168.100.10:8080/get_card_data");

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const jsonData = await response.json();

      setApiData({
        entered:jsonData.entered,
        left:jsonData.left,
        instore:jsonData.instore,
        returning:jsonData.returning,
        new:jsonData.new,
        groups:jsonData.groups
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
  },[]); 

  const apiContextValue = {
    apiData,
  };

  return (
    <ApiContext.Provider value={apiContextValue}>
      {children}
    </ApiContext.Provider>
  );
}
