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

  // Function to fetch data from the API
  const fetchDataFromApi = async () => {
    try {
      const response = await fetch("http://192.168.18.132:8080/get_latest_processed_frame/2"); 

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
    const interval = setInterval(fetchDataFromApi, 100);

    // Clean up the timer when the component unmounts
    return () => clearInterval(interval);
  }, []);

  return (
    <ApiContext.Provider value={apiData}>
      {children}
    </ApiContext.Provider>
  );
}
