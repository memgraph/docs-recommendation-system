import React from 'react';
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";

export const Header = () => {

    return (
        <AppBar position="static" style={{ background: "#fb6e00", marginBottom: "30px", paddingRight: "50px" }}>
        <Toolbar>
          <a href="https://memgraph.com/" target="_blank" rel="noopener noreferrer">
            <img src="/logo_memgraph.png" alt="" width="50" height="50"></img>
          </a>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1, fontSize: "24px" }}>
            Docs Recommendation System
          </Typography>
        </Toolbar>
      </AppBar>
    );
}

export default Header;