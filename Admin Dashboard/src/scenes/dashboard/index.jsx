import {
  Box,
  Button,
  IconButton,
  Typography,
  useTheme,
  Select,
  MenuItem,
} from "@mui/material";
import { tokens } from "../../theme";
import DownloadOutlinedIcon from "@mui/icons-material/DownloadOutlined";
import PeopleIcon from "@mui/icons-material/People";
import ManIcon from "@mui/icons-material/Man";
import Woman2Icon from "@mui/icons-material/Woman2";
import GroupsIcon from "@mui/icons-material/Groups";
import Header from "../../components/Header";
import CountLineChart from "../../components/CountLineChart";
import GCountLineChart from "../../components/GCountLineChart";
import DailyLineChart from "../../components/DailyLine";
import WeeklyLineChart from "../../components/WeeklyLine";
import MonthlyLineChart from "../../components/MonthlyLine";
import CurrentCountsLine from "../../components/CurrentCountsLine";
import BarChart from "../../components/BarChart";
import PieChart from "../../components/PieChart";
import StatBox from "../../components/StatBox";
import ProgressCircle from "../../components/ProgressCircle";
import CCTVVideo from "../../components/CCTVVideo";
import React, { useState, useEffect } from "react";
import { useApi } from "../../scenes/global/ApiContext";
import CountLiveMinute from "../../components/CountLiveMinute";

const Dashboard = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  const { apiData } = useApi();
  const { count, groupCount, time, male, female, unknown } = apiData;

  const [chartType, setChartType] = useState("Today");
  const [currentTime, setCurrentTime] = useState("");
  const [currentDate, setCurrentDate] = useState("");

  useEffect(() => {
    const interval = setInterval(() => {
      const now = new Date();
      const hours = now.getHours().toString().padStart(2, "0");
      const minutes = now.getMinutes().toString().padStart(2, "0");
      const seconds = now.getSeconds().toString().padStart(2, "0");
      setCurrentTime(`${hours}:${minutes}:${seconds}`);

      const day = now.getDate().toString().padStart(2, "0");
      const monthNames = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
      ];
      const month = monthNames[now.getMonth()];
      const year = now.getFullYear();
      setCurrentDate(`${day} ${month} ${year}`);
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  const renderChart = () => {
    if (chartType === "Today") {
      return <DailyLineChart isDashboard={true} />;
    } else if (chartType === "Weekly") {
      return <WeeklyLineChart isDashboard={true} />;
    } else if (chartType === "Monthly") {
      return <MonthlyLineChart isDashboard={true} />;
    }
  };

  return (
    <Box m="20px">
      {/* HEADER */}
      <Box display="flex" justifyContent="space-between" alignItems="center">
        <Header title="CSE DEPARTMENT" subtitle={"Surveillance Analytics"} />

        <Box>
          <Typography variant="h5" fontWeight="600" color={colors.grey[100]}>
            {currentTime} | {currentDate}
          </Typography>
        </Box>
      </Box>

      {/* GRID & CHARTS */}
      <Box
        display="grid"
        gridTemplateColumns="repeat(12, 1fr)"
        gridAutoRows="140px"
        gap="20px"
      >
        {/* ROW 1 : Footfall Line Graph*/}

        <Box
          gridColumn="span 12"
          gridRow="span 2"
          backgroundColor={colors.primary[400]}
        >
          <Box
            mt="25px"
            p="0 30px"
            display="flex "
            justifyContent="space-between"
            alignItems="center"
          >
            <Box>
              <Typography
                variant="h5"
                fontWeight="600"
                color={colors.grey[100]}
              >
                FOOTFALL
              </Typography>
              <Typography
                variant="h3"
                fontWeight="bold"
                color={colors.greenAccent[500]}
              >
                {chartType}
              </Typography>
            </Box>
            <Box>
              <Select
                value={chartType}
                onChange={(e) => setChartType(e.target.value)}
                sx={{
                  width: 150,
                  height: 35,
                }}
              >
                <MenuItem value="Today">Today</MenuItem>
                <MenuItem value="Weekly">This Week</MenuItem>
                <MenuItem value="Monthly">This Month</MenuItem>
              </Select>
            </Box>
          </Box>
          <Box height="250px" m="-20px 0 0 0">
            {renderChart()}
          </Box>
        </Box>

        {/* Row 2: CCTV Video */}

        <Box
          gridColumn="span 9"
          gridRow="span 3"
          backgroundColor={colors.primary[400]}
        >
          <Box
            mt="10px"
            p="0 0px"
            display="flex "
            justifyContent="space-between"
            alignItems="center"
          >
            <Box>
              <Typography
                variant="h5"
                fontWeight="600"
                margin="15px 0 0 25px"
                color={colors.grey[100]}
              >
                CCTV VIDEO
              </Typography>
              <Typography
                variant="h3"
                fontWeight="bold"
                marginLeft="25px"
                color={colors.greenAccent[500]}
                marginBottom="5px"
              >
                Live
              </Typography>
            </Box>
          </Box>
          <Box
            height="250px"
            m="0px 0 0 0"
            display="flex"
            justifyContent="center"
          >
            <CCTVVideo isDashboard={true} height="315vh" />
          </Box>
        </Box>

        {/* gender ratio Box */}
        <Box
          gridColumn="span 4"
          gridRow="span 2"
          // paddingLeft="20px"
          // paddingRight="20px"
          backgroundColor={colors.primary[400]}
        >
          <Box mt="25px" ml="20px">
            <Typography variant="h5" fontWeight="600" color={colors.grey[100]}>
              GENDER RATIO
            </Typography>
          </Box>

          <Box height="220px" >
            <PieChart isDashboard={true} />
          </Box>
        </Box>

        {/* ROW 2 : four stat boxes  */}

        <Box
          gridColumn="span 3"
          backgroundColor={colors.primary[400]}
          display="flex"
          alignItems="center"
          justifyContent="center"
        >
          <StatBox
            title={count}
            subtitle="PEOPLE COUNT"
            progress="0.75"
            increase={time}
            icon={
              <PeopleIcon
                sx={{ color: colors.greenAccent[600], fontSize: "26px" }}
              />
            }
          />
        </Box>

        <Box
          gridColumn="span 3"
          backgroundColor={colors.primary[400]}
          display="flex"
          alignItems="center"
          justifyContent="center"
        >
          <StatBox
            title={groupCount}
            subtitle="GROUP COUNT"
            progress="0.80"
            increase={time}
            icon={
              <GroupsIcon
                sx={{ color: colors.greenAccent[600], fontSize: "26px" }}
              />
            }
          />
        </Box>

        <Box
          gridColumn="span 3"
          backgroundColor={colors.primary[400]}
          display="flex"
          alignItems="center"
          justifyContent="center"
        >
          <StatBox
            title={unknown}
            subtitle="MEN"
            progress="0.50"
            increase="+21%"
            icon={
              <ManIcon
                sx={{ color: colors.greenAccent[600], fontSize: "26px" }}
              />
            }
          />
        </Box>
        <Box
          gridColumn="span 3"
          backgroundColor={colors.primary[400]}
          display="flex"
          alignItems="center"
          justifyContent="center"
        >
          <StatBox
            title={female}
            subtitle="WOMEN"
            progress="0.30"
            increase="+5%"
            icon={
              <Woman2Icon
                sx={{ color: colors.greenAccent[600], fontSize: "26px" }}
              />
            }
          />
        </Box>

        {/* ROW 3: CCTV Video and Min/Max Count per minute Line Graph */}
        <Box
          gridColumn="span 5"
          gridRow="span 2"
          backgroundColor={colors.primary[400]}
        >
          <Box
            mt="25px"
            p="0 30px"
            display="flex "
            justifyContent="space-between"
            alignItems="center"
          >
            <Box>
              <Typography
                variant="h5"
                fontWeight="600"
                color={colors.grey[100]}
              >
                CCTV VIDEO
              </Typography>
              <Typography
                variant="h3"
                fontWeight="bold"
                color={colors.greenAccent[500]}
                marginBottom="5px"
              >
                Live
              </Typography>
            </Box>
          </Box>
          <Box
            height="250px"
            m="0px 0 0 0"
            display="flex"
            justifyContent="center"
          >
            <CCTVVideo isDashboard={true} height="180vh" />
          </Box>
        </Box>

        <Box
          gridColumn="span 7"
          gridRow="span 2"
          backgroundColor={colors.primary[400]}
        >
          <Box
            mt="25px"
            p="0 30px"
            display="flex "
            justifyContent="space-between"
            alignItems="center"
          >
            <Box>
              <Typography
                variant="h5"
                fontWeight="600"
                color={colors.grey[100]}
              >
                MIN/MAX COUNT PER MINUTE
              </Typography>
              <Typography
                variant="h3"
                fontWeight="bold"
                color={colors.greenAccent[500]}
              >
                Min and Max people in a minute
              </Typography>
            </Box>
            <Box>
              <IconButton>
                <DownloadOutlinedIcon
                  sx={{ fontSize: "26px", color: colors.greenAccent[500] }}
                />
              </IconButton>
            </Box>
          </Box>
          <Box height="250px" m="-20px 0 0 0">
            <CountLiveMinute isDashboard={true} />
          </Box>
        </Box>

        {/* Row 3 */}

        <Box
          gridColumn="span 12"
          gridRow="span 2"
          backgroundColor={colors.primary[400]}
        >
          <Box
            mt="25px"
            p="0 30px"
            display="flex "
            justifyContent="space-between"
            alignItems="center"
          >
            <Box>
              <Typography
                variant="h5"
                fontWeight="600"
                color={colors.grey[100]}
              >
                LIVE COUNTS
              </Typography>
              <Typography
                variant="h3"
                fontWeight="bold"
                color={colors.greenAccent[500]}
              >
                Individual | Group
              </Typography>
            </Box>
          </Box>
          <Box height="250px" m="-20px 0 0 0">
            <CurrentCountsLine isDashboard={true} />
          </Box>
        </Box>

        {/* ROW 3 */}
        <Box
          gridColumn="span 6"
          gridRow="span 2"
          backgroundColor={colors.primary[400]}
        >
          <Box
            mt="25px"
            p="0 30px"
            display="flex "
            justifyContent="space-between"
            alignItems="center"
          >
            <Box>
              <Typography
                variant="h5"
                fontWeight="600"
                color={colors.grey[100]}
              >
                GROUP COUNT HOURLY
              </Typography>
              <Typography
                variant="h3"
                fontWeight="bold"
                color={colors.greenAccent[500]}
              >
                18 groups today
              </Typography>
            </Box>
            <Box>
              <IconButton>
                <DownloadOutlinedIcon
                  sx={{ fontSize: "26px", color: colors.greenAccent[500] }}
                />
              </IconButton>
            </Box>
          </Box>
          <Box height="250px" m="-20px 0 0 0">
            <GCountLineChart isDashboard={true} />
          </Box>
        </Box>

        <Box
          gridColumn="span 6"
          gridRow="span 2"
          backgroundColor={colors.primary[400]}
        >
          <Typography
            variant="h5"
            fontWeight="600"
            sx={{ padding: "30px 30px 0 30px" }}
          >
            WEEKLY GENDER DISTRIBUTION
          </Typography>
          <Box height="250px" mt="-20px">
            <BarChart isDashboard={true} height="30vh" />
          </Box>
        </Box>


        {/* ROW 4 */}

        <Box
          gridColumn="span 4"
          gridRow="span 2"
          backgroundColor={colors.primary[400]}
          p="30px"
        >
          <Typography variant="h5" fontWeight="600">
            FOOTFALL PROGRESS
          </Typography>
          <Box
            display="flex"
            flexDirection="column"
            alignItems="center"
            mt="25px"
          >
            <ProgressCircle size="125" />
            <Typography
              variant="h5"
              color={colors.greenAccent[500]}
              sx={{ mt: "15px" }}
            >
              11%
            </Typography>
            <Typography>MONTHLY GROWTH IN FOOTFALL</Typography>
          </Box>
        </Box>
      </Box>
    </Box>
  );
};

export default Dashboard;
