import React from "react";
import Graph from "./graph";
import { Box, ListSubheader } from '@mui/material';

export const GraphWrapper = ({ nodes, links }) => {
    
    const nodesData = nodes
    const linksData = links

    return (
        <Box sx={{ width: "60%", display: "flex", flexDirection: "column", justifyContent: "flex-start", alignItems: "center" }} >
            <ListSubheader sx={{ display: 'inline-flex', fontSize: "19px" }} disableSticky="true">
                Graph visualization
            </ListSubheader>
            <Graph nodesData={nodesData} linksData={linksData} />
        </Box>
    );
}

export default GraphWrapper;