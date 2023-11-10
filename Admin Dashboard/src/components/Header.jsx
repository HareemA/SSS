import { Typography, Box, useTheme } from "@mui/material";
import { tokens } from "../theme";

const Header = ({ title, subtitle }) => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  return (
    <Box mb="20px">
      <Typography
        variant="h3"
        color={colors.grey[100]}
        fontWeight="bold"
        sx={{ m: "0 0 5px 0" }}
      >
        {title}
      </Typography>
      <Typography
        variant="h6"
        color={
          theme.palette.mode === "dark" ? colors.greenAccent[500] : colors.blueAccent[150]
        }
      >
        {subtitle}
      </Typography>
    </Box>
  );
};

export default Header;
