import React from "react";
import { Box, List, ListItem, ListSubheader, Divider, Link } from '@mui/material';


export const Recommendations = (data) => {

    const node2vecItems = data.data["node2vec"] ? data.data["node2vec"] : []
    const tf_idfItems = data.data["tf-idf"] ? data.data["tf-idf"] : []

    const getPageName = (link) => {
        const parts = link.split("/")
        let pageName = parts[parts.length - 1]
        if(pageName === "")  pageName = parts[parts.length - 2]
        
        return pageName  
    }

    return (
        <Box sx={{ width: '40%' }}>
            <List sx={{paddingLeft: "4%"}} subheader={
                    <ListSubheader sx={{ textAlign: "left", fontSize: "17px" }}>
                        Top TF-IDF recommendations
                    </ListSubheader>}>
                { tf_idfItems.map((item) => <ListItem  key={item}><Link href={item} underline="hover" target="_blank" rel="noopener noreferrer">
                    {getPageName(item)}
                    </Link></ListItem >)}
            </List>
            <Divider variant="middle" />
            <List sx={{paddingLeft: "4%"}} subheader={
                    <ListSubheader sx={{ textAlign: "left", fontSize: "17px" }}>
                        Top node2vec recommendations
                    </ListSubheader>}>
                { node2vecItems.map((item) => <ListItem  key={item}><Link href={item} underline="hover" target="_blank" rel="noopener noreferrer">
                    {getPageName(item)}
                    </Link></ListItem >)}
            </List>
        </Box>
    );
}

export default Recommendations;