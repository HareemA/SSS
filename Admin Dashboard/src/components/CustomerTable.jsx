import { useEffect } from "react";
import { useTheme } from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import { tokens } from "../theme";
import { BorderClear } from "@mui/icons-material";

const CustomerTable = ({isDashboard = false, users, height}) => {
    const columns = [
        {field:'id',headerName:'ID',flex:1,sortable: true, sortComparator: (a, b) => a - b},
        {field: 'name', headerName:'Name',width:'150'},
        {field: 'visits', headerName:'No. of Visits',flex:1},
        {field: 'gender', headerName:'Gender',flex:1},
        {field: 'age', headerName:'Age',flex:1},
        {field: 'group', headerName:'Group',flex:1},
        {field: 'timeIn', headerName:'Time In',flex:1},
        {field: 'timeOut', headerName:'Time Out',flex:1}
    ];
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);

    return (
        <div style={{ height: height, width: '100%' }}>
            <DataGrid 
                rows={users} 
                columns={columns} 
                // pageSize={5} 
                checkboxSelection 
                pagination={false}
                rowHeight={38}
                sortingMode="client"
                headerClassName="custom-header"
                cellClassName="custom-cell"
                
                />
        </div>
    );
};

export default CustomerTable;


