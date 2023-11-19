import { useEffect, useState } from 'react';
import { useTheme } from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import { tokens } from "../theme";
import { BorderClear } from "@mui/icons-material";

const CustomerTable = ({isDashboard = false, users, height}) => {
    const columns = [
        {field:'C_No',headerName:'C No.',flex:1,sortable: true, sortComparator: (a, b) => a - b},
        {field: 'name', headerName:'Name',width:'150'},
        {field: 'visits', headerName:'No. of Visits',flex:1},
        {field: 'gender', headerName:'Gender',flex:1},
        {field: 'age', headerName:'Age',flex:1},
        {field: 'group', headerName:'Group',flex:1},
        {field: 'timeIn', headerName:'Time In',flex:1},
        {field: 'timeOut', headerName:'Time Out',flex:1},
        {field:'id',headerName:'ID',flex:1,sortable: true, sortComparator: (a, b) => a - b}
    ];
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);

    const [chartData, setChartData] = useState([]);

      useEffect(() => {
        const fetchTableData = async () => {
          try {
            const response = await fetch('http://192.168.18.132:8080/customers_table');
      
            if (!response.ok) {
              throw new Error('Network response was not ok');
            }
      
            const jsonData = await response.json();
            console.log("Fetched Table Data:", jsonData);

            // Clear the table data before updating with the latest values from the API
            setChartData([]);
      
            const TableData = jsonData;
            console.log("Table Data: ", TableData);
      
            // Update the table data with the latest values from the API
            setChartData(TableData);
            console.log("Updated TABLE Data:", TableData);
          } catch (error) {
            console.error('Error fetching repeat ratio pie chart data:', error);
          }
        };
      
        // Fetch gender Table data initially and then every x minutes
        fetchTableData();
        const intervalId = setInterval( fetchTableData, 600);
      
        return () => clearInterval(intervalId);
      }, []);

    return (
        <div style={{ height: height, width: '100%' }}>
            <DataGrid 
                rows={chartData}
                columns={columns}
                keyProp="id"
                checkboxSelection
                pagination={false}
                rowHeight={38}
                sortingMode="client"
                sortModel={[
                {
                    field: 'C_No',
                    sort: 'desc',
                },
                ]}
                headerClassName="custom-header"
                cellClassName="custom-cell"
                
                />
        </div>
    );
};

export default CustomerTable;


