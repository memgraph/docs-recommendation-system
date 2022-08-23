import React, {useState, useEffect}  from "react";
import { Statistics } from './statistics';
import { Pagerank } from './pagerank'
import { Box } from '@mui/material';
import Typography from '@mui/material/Typography';

export const Visualisation = ({ data, displayStats, displayPagerank} ) => {

    const [showStats, setShowStats] = useState(false)
    const [showPagerank, setShowPagerank] = useState(false)
    const recs = data
    
    useEffect(() => {
        setShowStats(displayStats)
        setShowPagerank(displayPagerank)
      }, [displayStats, displayPagerank]);

    return (
        <>
            { showStats ? <Statistics data={recs} /> :
              ( showPagerank ? <Pagerank /> :
            (<Box sx={{ width: "60%", alignItems: "center", justifyContent: 'center' }}>
                    <img style={{ paddingTop: "15%" }} src="https://playground.memgraph.com/assets/img/GraphView.svg" alt="" width="320" height="160"></img>
                    <Typography sx={{ paddingTop: "10px" }} variant="subtitle1">
                        To visualize data or show statistics, click on one of the buttons on the left. 
                    </Typography>
            </Box>))
            }
        </>
    );
}

export default Visualisation;