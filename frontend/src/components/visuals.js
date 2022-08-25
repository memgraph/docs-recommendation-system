import React, {useState, useEffect}  from "react";
import { Statistics } from './statistics';
import { Pagerank } from './pagerank'
import { Box } from '@mui/material';
import Typography from '@mui/material/Typography';
import GraphWrapper from "./graphWrapper";

export const Visualisation = ({ data, graphData, displayStats, displayGraph, displayPagerank} ) => {

    const recs = data
    const graph = graphData
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
              ( showPagerank ? <Pagerank /> : 
                ( showGraph ? <GraphWrapper nodes={graph.nodes} links={graph.links} url={graph.base_url}/> :
                    (<Box sx={{ width: "60%", alignItems: "center", justifyContent: 'center' }}>
                        <img style={{ paddingTop: "15%" }} src="https://playground.memgraph.com/assets/img/GraphView.svg" alt="" width="320" height="160"></img>
                        <Typography sx={{ paddingTop: "10px" }} variant="subtitle1">
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