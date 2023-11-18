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
import LoginIcon from "@mui/icons-material/Login";
import LogoutIcon from "@mui/icons-material/Logout";
import StorefrontIcon from "@mui/icons-material/Storefront";
import GroupsIcon from "@mui/icons-material/Groups";
import PersonAddIcon from "@mui/icons-material/PersonAdd";
import ReplayIcon from "@mui/icons-material/Replay";
import Header from "../../components/Header";
import CountLineChart from "../../components/CountLineChart";
import GCountLineChart from "../../components/GCountLineChart";
import DailyLineChart from "../../components/DailyLine";
import WeeklyLineChart from "../../components/WeeklyLine";
import MonthlyLineChart from "../../components/MonthlyLine";
import FiveMinuteLineChart from "../../components/FiveMinuteLine";
import CurrentCountsLine from "../../components/CurrentCountsLine";
import BarChart from "../../components/BarChart";
import PieChart from "../../components/PieChart";
import StatBox from "../../components/StatBox";
import ProgressCircle from "../../components/ProgressCircle";
import CCTVVideo from "../../components/CCTVVideo";
import React, { useState, useEffect } from "react";
import { useApi } from "../../scenes/global/ApiContext";
import CountLiveMinute from "../../components/CountLiveMinute";
import CustomerTable from "../../components/CustomerTable";
import PieChartGroup from "../../components/PieChartGroup";
import EngagementBarGraph from "../../components/EngagementBarGraph";
import { mockUserData as userData } from "../../data/mockData";
import RepeatRatioPie from "../../components/RepeatRatioPie";

const Dashboard = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  const { apiData } = useApi();

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
    //else if (chartType === "MinutesLive") {
      //return <FiveMinuteLineChart isDashboard={true} />;
   // }
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
          border={`1px solid ${colors.primary[900]}`}
          borderRadius="20px"
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
                color={
                  theme.palette.mode === "dark"
                    ? colors.greenAccent[500]
                    : colors.blueAccent[150]
                }
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
                <MenuItem value="Monthly">Last Month</MenuItem>
                {/* <MenuItem value="MinutesLive">5 Minute</MenuItem> */}
              </Select>
            </Box>
          </Box>
          <Box height="250px" m="-20px 0 0 0">
            {renderChart()}
          </Box>
        </Box>

        {/* Row 2: CCTV Video + card */}

        <Box
          gridColumn="span 9"
          gridRow="span 3"
          backgroundColor={colors.primary[400]}
          border={`1px solid ${colors.primary[900]}`}
          borderRadius="20px"
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
                color={
                  theme.palette.mode === "dark"
                    ? colors.greenAccent[500]
                    : colors.blueAccent[150]
                }
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

        {/* CARD */}
        <Box
          gridColumn="span 3"
          gridRow="span 3"
          backgroundColor={colors.primary[400]}
          border={`1px solid ${colors.primary[900]}`}
          borderRadius="20px"
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
                fontWeight="700"
                margin="15px 0 15px 35px"
                alignItems="center"
                color={colors.grey[200]}
              >
                CUSTOMERS TODAY
              </Typography>
            </Box>
          </Box>

          <Box
            display="flex"
            flexDirection="column" // Set the container to display items vertically
            alignItems="center"
          >
            {[
              {
                icon: (
                  <LoginIcon
                    sx={{
                      fontSize: "26px",
                      color:
                        theme.palette.mode === "dark"
                          ? colors.redAccent[500]
                          : colors.blueAccent[150],
                    }}
                  />
                ),
                label: "Entered",
                value: apiData.entered,
              },
              {
                icon: (
                  <LogoutIcon
                    sx={{
                      fontSize: "26px",
                      color:
                        theme.palette.mode === "dark"
                          ? colors.redAccent[500]
                          : colors.blueAccent[150],
                    }}
                  />
                ),
                label: "Left",
                value: apiData.left,
              },
              {
                icon: (
                  <StorefrontIcon
                    sx={{
                      fontSize: "26px",
                      color:
                        theme.palette.mode === "dark"
                          ? colors.redAccent[500]
                          : colors.blueAccent[150],
                    }}
                  />
                ),
                label: "In-Store",
                value: apiData.instore,
              },
              {
                icon: (
                  <PersonAddIcon
                    sx={{
                      fontSize: "26px",
                      color:
                        theme.palette.mode === "dark"
                          ? colors.redAccent[500]
                          : colors.blueAccent[150],
                    }}
                  />
                ),
                label: "New",
                value: apiData.new,
              },
              {
                icon: (
                  <ReplayIcon
                    sx={{
                      fontSize: "26px",
                      color:
                        theme.palette.mode === "dark"
                          ? colors.redAccent[500]
                          : colors.blueAccent[150],
                    }}
                  />
                ),
                label: "Returning",
                value: apiData.returning,
              },
              {
                icon: (
                  <GroupsIcon
                    sx={{
                      fontSize: "26px",
                      color:
                        theme.palette.mode === "dark"
                          ? colors.redAccent[500]
                          : colors.blueAccent[150],
                    }}
                  />
                ),
                label: "Groups",
                value: apiData.groups,
              },
            ].map((item, index) => (
              <Box
                key={index}
                p="15px 15px"
                m="0px 25px"
                display="flex"
                justifyContent="space-between"
                width="100%" // Make each row equally spaced and centered
              >
                <Box display="flex" alignItems="center">
                  {item.icon}
                  <Typography
                    variant="h5"
                    fontWeight="600"
                    color={colors.grey[100]}
                    paddingLeft="10px"
                  >
                    {item.label}
                  </Typography>
                </Box>
                <Typography
                  variant="h5"
                  fontWeight="600"
                  color={colors.grey[100]}
                  paddingRight="8px"
                >
                  {item.value}
                </Typography>
              </Box>
            ))}
          </Box>
        </Box>

        {/* ROW 3: Gender, Repeat Ratio Pie Chart, Group Trend, Engagement, BAR Graph */}
        {/* Gender Ratio Pie */}
        <Box
          gridColumn="span 4"
          gridRow="span 2"
          backgroundColor={colors.primary[400]}
          border={`1px solid ${colors.primary[900]}`}
          borderRadius="20px"
        >
          <Box mt="25px" ml="20px">
            <Typography variant="h5" fontWeight="600" color={colors.grey[100]}>
              GENDER RATIO
            </Typography>
          </Box>

          <Box height="220px">
            <PieChart isDashboard={true} />
          </Box>
        </Box>

        <Box
          gridColumn="span 4"
          gridRow="span 2"
          backgroundColor={colors.primary[400]}
          border={`1px solid ${colors.primary[900]}`}
          borderRadius="20px"
        >
          <Box mt="25px" ml="20px">
            <Typography variant="h5" fontWeight="600" color={colors.grey[100]}>
              REPEAT RATIO
            </Typography>
          </Box>

          <Box height="220px">
            <RepeatRatioPie isDashboard={true} />
          </Box>
        </Box>

        <Box
          gridColumn="span 4"
          gridRow="span 2"
          backgroundColor={colors.primary[400]}
          border={`1px solid ${colors.primary[900]}`}
          borderRadius="20px"
        >
          <Box mt="25px" ml="20px">
            <Typography variant="h5" fontWeight="600" color={colors.grey[100]}>
              GROUP RATIO
            </Typography>
          </Box>

          <Box height="220px">
            <PieChartGroup isDashboard={true} />
          </Box>
        </Box>

        {/* ROW: ENgagement ad Gender BARS */}

        <Box
          gridColumn="span 6"
          gridRow="span 2"
          backgroundColor={colors.primary[400]}
          border={`1px solid ${colors.primary[900]}`}
          borderRadius="20px"
        >
          <Typography
            variant="h5"
            fontWeight="600"
            sx={{ padding: "30px 30px 0 30px" }}
          >
            DAILY GENDER DISTRIBUTION
          </Typography>
          <Box height="250px" mt="-20px">
            <BarChart isDashboard={true} height="30vh" />
          </Box>
        </Box>

        <Box
          gridColumn="span 6"
          gridRow="span 2"
          backgroundColor={colors.primary[400]}
          p="30px"
          border={`1px solid ${colors.primary[900]}`}
          borderRadius="20px"
        >
          <Typography variant="h5" fontWeight="600">
            ENGAGEMENT
          </Typography>
          <Box height="250px" mt="-20px">
            <EngagementBarGraph isDashboard={true} height="30vh" />
          </Box>
        </Box>

        {/* USERS DATA TABLE */}
        <Box
          gridColumn="span 12"
          height={300}
          backgroundColor={colors.primary[400]}
        >
          <Box height={350} sx={{ marginBottom: "35px" }}>
            <CustomerTable isDashboard={true} users={userData} height="300px" />
          </Box>
        </Box>

        {/* XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX */}

        {/*  four stat boxes 

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
        </Box> */}

        {/* ROW 3: CCTV Video and Min/Max Count per minute Line Graph */}
        {/* <Box
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
        </Box> */}

        {/* <Box
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
        </Box> */}

        {/* LINE live */}

        {/* <Box
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
        </Box> */}

        {/* LINE GCOUNT */}
        {/* <Box
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
          </Box>
          <Box height="250px" m="-20px 0 0 0">
            <GCountLineChart isDashboard={true} />
          </Box>
        </Box> */}

        {/* ROW 4 */}

        {/* LINE */}
        {/* <Box
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
                HOURLY FOOTFALL
              </Typography>
              <Typography
                variant="h3"
                fontWeight="bold"
                color={colors.greenAccent[500]}
              >
                XXX individuals today
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
            <CountLineChart isDashboard={true} />
          </Box>
        </Box> */}
      </Box>
    </Box>
  );
};

export default Dashboard;
