import React from "react";
import { Box, ListSubheader } from '@mui/material';
import Pagerank from "./pagerank";

export const PagerankWrapper = ({ pagerankData }) => {

    const data = pagerankData.page_rank

    return ( 
        <Box sx={{ width: "60%", display: "flex", flexDirection: "column", justifyContent: "flex-start", alignItems: "center" }}>
            <ListSubheader sx={{ display: 'inline-flex', fontSize: "19px" }} disableSticky={true}>
                Pagerank visualization
            </ListSubheader>
            <Pagerank nodes={data} />
        </Box>
    );
}

export default PagerankWrapper;