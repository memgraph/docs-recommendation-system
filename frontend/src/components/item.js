import React from "react";
import axios from 'axios';
import { ListItem, Link, Button, Tooltip } from '@mui/material';
import InsightsIcon from '@mui/icons-material/Insights';
import LaunchIcon from '@mui/icons-material/Launch';


export const RecsItem = ({ url, name, showGraph, updateGraph }) => {

    const link = url
    const short_name = name

    const getGraphData = async(event) => {
        event.preventDefault()
        let okRequest = true
        
        const response = await axios({
            method: "get",
            url: "http://localhost:5000/webpage/?url=" + link,
        }).catch(error => {
            okRequest = false
            if(error.response.status === 500){
                alert("Something went wrong.")
                return
            }
        })
        if(okRequest){        
            updateGraph(response.data)
            showGraph()
        }
    }
    
    return ( 
        <ListItem sx={{ display: 'flex', alignItems: "left", justifyContent: "space-between", marginBottom: "5px", paddingBottom: "0px", paddingTop: "0px" }} key={link}>
            <Link sx={{ fontSize: "17px" }} href={link} underline="hover" target="_blank" rel="noopener noreferrer">
                { short_name }
                <LaunchIcon sx={{ color: "#fb6e00", paddingLeft: "5px", fontSize: "medium" }}/>
            </Link>
            <Tooltip title={<span style={{ fontSize: "14px" }}>Show graph visualization</span>} placement="right">
                <Button sx={{ marginLeft: "5px", padding: "5px" }} variant="outlined" onClick={getGraphData}>
                    Graph
                    <InsightsIcon sx={{ color: "#fb6e00", paddingLeft: "5px", paddingTop: "0px", paddingBottom: "0px" }} />
                </Button>
            </Tooltip>
        </ListItem >
    );
}

export default RecsItem;