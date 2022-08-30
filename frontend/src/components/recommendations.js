import React from "react";
import axios from 'axios';
import { RecsItem } from './item';
import { Box, List, ListItem, ListSubheader, Divider, Link, Button } from '@mui/material';
import KeyboardArrowRightIcon from '@mui/icons-material/KeyboardArrowRight';
import BubbleChartIcon from '@mui/icons-material/BubbleChart';
import QueryStatsIcon from '@mui/icons-material/QueryStats';

export const Recommendations = ({ data, updateStats, updateGraph, updatePagerankData, updateGraphData, updatePagerank }) => {

    const tf_idfItems = data["tf-idf"] ? data["tf-idf"] : []
    const node2vecItems = data["node2vec"] ? data["node2vec"] : []
    const link_predictionsItems = data["link_prediction"] ? data["link_prediction"] : []
    const names = data["names"] ? data["names"] : []

    const getPageName = (link) => { return names[link] }

    const showStats = () => { 
        updateStats(true)
        updateGraph(false)
        updatePagerank(false) 
    }

    const showPagerank = () => { 
        updatePagerank(true) 
        updateStats(false)
        updateGraph(false)
    }

    const showGraph = () => {
        updateGraph(true)
        updateStats(false)
        updatePagerank(false) 
    }
    
    const updateGraphData_ = (data) => {
        updateGraphData(data)
    }

    const getPagerankData = async(event) => {
        event.preventDefault()
        let okRequest = true
        
        const response = await axios({
            method: "get",
            url: "http://localhost:5000/pagerank",
        }).catch(error => {
            okRequest = false
            if(error.response.status === 500){
                alert("Something went wrong.")
                return
            }
        })
        if(okRequest){
            showPagerank()     
            updatePagerankData(response.data)
        }
    }

    return (
        <Box sx={{ width: '40%' }}>
            <Box sx={{ display: 'flex', alignItems: "left", justifyContent: "space-between", 
                       marginLeft: "15px", marginRight: "15px" }}>
                <Box>
                    <List subheader={
                            <ListSubheader sx={{ textAlign: "left", fontSize: "17px" }} disableSticky="true">
                                TF-IDF recommendations
                            </ListSubheader>}>
                        { tf_idfItems.map((item, index) => <ListItem  key={index}><Link href={item} underline="hover" target="_blank" rel="noopener noreferrer">
                            {getPageName(item)}
                            </Link></ListItem >)}
                    </List>
                </Box>
                <Box sx={{display: 'flex', alignItems: "center", justifyContent: "center" }}>
                    <Button sx={{ paddingLeft: "10px", paddingRight: "0px" }} variant="outlined" onClick={showStats}>
                        <QueryStatsIcon sx={{ color: "#fb6e00" }}></QueryStatsIcon>
                        <KeyboardArrowRightIcon sx={{ color: "#fb6e00", paddingLeft: "20px" }} />
                    </Button>
                </Box>
            </Box>
            <Divider variant="middle" />
            <Box sx={{display: 'flex', flexDirection: "column", alignItems: "left", justifyContent: "left", marginLeft: "15px" }}>
                <List subheader={
                        <ListSubheader sx={{ textAlign: "left", fontSize: "17px" }} disableSticky="true">
                            node2vec recommendations
                        </ListSubheader>}>
                    { node2vecItems.map((item, index) => <RecsItem key={index} url={item} name={getPageName(item)} showGraph={showGraph} updateGraph={updateGraphData_}/>) }
                </List>
            </Box>
            <Divider variant="middle" />
            <Box sx={{display: 'flex', flexDirection: "column", alignItems: "left", justifyContent: "left", marginLeft: "15px" }}>
                <List subheader={
                        <ListSubheader sx={{ textAlign: "left", fontSize: "17px" }} disableSticky="true">
                            Link prediction recommendations
                        </ListSubheader>}>
                    { link_predictionsItems.map((item, index) => <RecsItem key={index} url={item} name={getPageName(item)} showGraph={showGraph} updateGraph={updateGraphData_}/>) }
                </List>
            </Box>
            <Divider variant="middle" />
            <Box sx={{ marginTop: "20px", marginBottom: "20px" }}>
                <Button variant="outlined" onClick={getPagerankData}>
                    Pagerank
                    <BubbleChartIcon sx={{ color: "#fb6e00", paddingLeft: "10px" }}></BubbleChartIcon>
                </Button>
            </Box>
        </Box>
    )
}

export default Recommendations;