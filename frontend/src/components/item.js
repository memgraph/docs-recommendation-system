import React from "react";
import axios from 'axios';
import { ListItem, Link, Button } from '@mui/material';
import InsightsIcon from '@mui/icons-material/Insights';


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
        <ListItem sx={{ display: 'flex', alignItems: "left", justifyContent: "space-between" }} 
                        key={link}><Link href={link} underline="hover" target="_blank" 
                        rel="noopener noreferrer">
                        { short_name }
                        </Link>
            <Button sx={{ marginLeft: "5px" }} onClick={getGraphData}>
                <InsightsIcon sx={{color: "#fb6e00"}}></InsightsIcon>
            </Button>
        </ListItem >
    );
}

export default RecsItem;