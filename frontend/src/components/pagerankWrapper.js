import React from "react";
import { Box, ListSubheader } from '@mui/material';
import Pagerank from "./pagerank";

export const PagerankWrapper = ({ pagerankData }) => {

    const data = pagerankData.page_rank
    console.log(data)

    return ( 
        <Box sx={{ width: "60%", justifyContent: 'center' }}>
            <ListSubheader sx={{ display: 'inline-flex', fontSize: "17px" }} disableSticky="true">
                Pagerank visualization
            </ListSubheader>
            <Pagerank nodes={data} />
        </Box>
    );
}

export default PagerankWrapper;