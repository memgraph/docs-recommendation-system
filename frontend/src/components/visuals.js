import React, {useState, useEffect}  from "react";
import { Statistics } from './statistics';
import { PagerankWrapper } from './pagerankWrapper'
import { Box } from '@mui/material';
import Typography from '@mui/material/Typography';
import GraphWrapper from "./graphWrapper";

export const Visualisation = ({ data, graphData, pageRankData, displayStats, displayGraph, displayPagerank} ) => {

    const recs = data
    const graph = graphData
    const pagerankData = pageRankData
    const [showStats, setShowStats] = useState(false)
    const [showGraph, setShowGraph] = useState(false)
    const [showPagerank, setShowPagerank] = useState(false)
    
    useEffect(() => {
        setShowStats(displayStats)
        setShowGraph(displayGraph)
        setShowPagerank(displayPagerank)
      }, [displayStats, displayGraph, displayPagerank]);

    return (
        <>
            { showStats ? <Statistics data={recs} /> :
              ( showPagerank ? <PagerankWrapper pagerankData={pagerankData}/> : 
                ( showGraph ? <GraphWrapper nodes={graph.nodes} links={graph.links} /> :
                    (<Box sx={{ width: "60%", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "flex-start" }}>
                        <img style={{ paddingTop: "15%" }} src="https://playground.memgraph.com/assets/img/GraphView.svg" alt="" width="320" height="160"></img>
                        <Typography sx={{ paddingTop: "10px", width: 320 }} variant="body1">
                            To visualize data or show statistics, click on one of the buttons on the left. 
                        </Typography>
                    </Box>)
                )
              )
            }
        </>
    );
}

export default Visualisation;