import React from "react";
import { Box, List, ListItem, ListSubheader, Divider, Link, Button } from '@mui/material';
import KeyboardArrowRightIcon from '@mui/icons-material/KeyboardArrowRight';


export const Recommendations = ({ data, updateStats, updatePagerank }) => {

    const tf_idfItems = data["tf-idf"] ? data["tf-idf"] : []
    const node2vecItems = data["node2vec"] ? data["node2vec"] : []
    const link_predictionsItems = data["link_prediction"] ? data["link_prediction"] : []

    const getPageName = (link) => {
        const parts = link.split("/")
        let pageName = parts[parts.length - 1]
        if(pageName === "")  pageName = parts[parts.length - 2]
        
        return pageName  
    }

    const showStats = () => { 
        updateStats(true)
        updatePagerank(false) 
    }
    const showPagerank = () => { 
        updatePagerank(true) 
        updateStats(false)
    }

    return (
        <Box sx={{ width: '40%' }}>
            <Box sx={{ display: 'flex', alignItems: "center", justifyContent: "center"}}>
                <List subheader={
                        <ListSubheader sx={{ textAlign: "left", fontSize: "17px" }}>
                            TF-IDF recommendations
                        </ListSubheader>}>
                    { tf_idfItems.map((item) => <ListItem  key={item}><Link href={item} underline="hover" target="_blank" rel="noopener noreferrer">
                        {getPageName(item)}
                        </Link></ListItem >)}
                </List>
                <Box>
                    <Button variant="outlined" onClick={showStats}>
                        Statistics
                        <KeyboardArrowRightIcon sx={{color: "#fb6e00"}} />
                    </Button>
                </Box>
            </Box>
            <Divider variant="middle" />
            <Box sx={{display: 'flex', alignItems: "center", justifyContent: "center"}}>
                <List subheader={
                        <ListSubheader sx={{ textAlign: "left", fontSize: "17px" }}>
                            node2vec recommendations
                        </ListSubheader>}>
                    { node2vecItems.map((item) => <ListItem key={item}><Link href={item} underline="hover" target="_blank" rel="noopener noreferrer">
                        {getPageName(item)}
                        </Link></ListItem >)}
                </List>
                <Box>
                    <Button variant="outlined" onClick={showPagerank}>
                        Pagerank
                        <KeyboardArrowRightIcon sx={{color: "#fb6e00" }} />
                    </Button>
                </Box>
            </Box>
            <Divider variant="middle" />
            <Box sx={{display: 'flex', alignItems: "center", justifyContent: "center"}}>
                <List subheader={
                        <ListSubheader sx={{ textAlign: "left", fontSize: "17px" }}>
                            Link prediction recommendations
                        </ListSubheader>}>
                    { link_predictionsItems.map((item) => <ListItem key={item}><Link href={item} underline="hover" target="_blank" rel="noopener noreferrer">
                        {getPageName(item)}
                        </Link></ListItem >)}
                </List>
                <Box>
                    <Button variant="outlined" onClick={showPagerank}>
                        Pagerank
                        <KeyboardArrowRightIcon sx={{color: "#fb6e00" }} />
                    </Button>
                </Box>
            </Box>
        </Box>
    );
}

export default Recommendations;