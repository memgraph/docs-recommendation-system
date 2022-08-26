import React from "react";
import Graph from "./graph";
import { Box, ListSubheader } from '@mui/material';

export const GraphWrapper = ({ nodes, links, url}) => {

    const nodesData = nodes
    const linksData = links
    const base_url = url

    return (
        <Box sx={{ width: "60%", justifyContent: 'center' }}>
            <ListSubheader sx={{ display: 'inline-flex', fontSize: "17px" }} disableSticky="true">
                Graph visualization
            </ListSubheader>
            <Graph nodesData={nodesData} linksData={linksData} base_url={base_url} />
        </Box>
    );
}

export default GraphWrapper;