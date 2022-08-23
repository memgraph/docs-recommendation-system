import React from 'react';
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";

export const Header = () => {

    return (
        <AppBar position="static" style={{ background: "#fb6e00", marginBottom: "30px", paddingRight: "50px" }}>
        <Toolbar>
          <img src="/logo_memgraph.png" alt="" width="50" height="50"></img>
          <Typography variant="h6" 
            component="div" sx={{ flexGrow: 1 }}>
            Docs recommendation system
          </Typography>
        </Toolbar>
      </AppBar>
    );
}

export default Header;