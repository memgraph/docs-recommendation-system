import React, { useEffect, useState } from 'react';
import './App.css';
import { Form } from './components/form';
import { Header } from './components/header';
import { Visualisation } from './components/visuals';
import { Recommendations } from './components/recommendations';
import { Box, LinearProgress, Divider, Typography, Link } from '@mui/material';
import LaunchIcon from '@mui/icons-material/Launch';


const App = () => {

  const [recommendations, setRecommendations] = useState({})
  const [url, setUrl] = useState("")
  const [graphData, setGraphData] = useState({})
  const [pageRankData, setPageRankData] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [displayRecs, setDisplayRecs] = useState(false)
  const [displayStats, setDisplayStats] = useState(false)
  const [displayPagerank, setDisplayPagerank] = useState(false)  
  const [displayGraph, setDisplayGraph] = useState(false)  

  useEffect(() => { setDisplayRecs(false) }, [])

  const updateRecommendations = (data, url) => { 
    setRecommendations(data) 
    setUrl(url)
  }

  const updateGraph = (data) => { setGraphData(data) }

  const updatePagerank = (data) => { setPageRankData(data) }

  const updateLoader = (value) => { setIsLoading(value) }

  const updateDisplay = (value) => { setDisplayRecs(value) }

  const showStats = (value) => { setDisplayStats(value) }

  const showPagerank = (value) => { setDisplayPagerank(value) }

  const showGraph = (value) => { setDisplayGraph(value) }
  
  return (
    <div className="App">
      <Header />
      <Form updateRecs={updateRecommendations} updateLoader={updateLoader} updateDisplay={updateDisplay}/>
      {
        displayRecs ? 
        (
        <>
          <Typography sx={{ padding: "10px", fontSize: "17px"}} variant="body1">
            Showing recommendations for URL:
            <Link sx={{paddingLeft: "5px"}} href={url} underline="hover" target="_blank" rel="noopener noreferrer">
                {url}
                <LaunchIcon sx={{ color: "#fb6e00", paddingLeft: "5px", fontSize: "medium" }}/>
            </Link>
          </Typography>
          <div className="flexbox-container" style={{ width: '90%', paddingLeft: "5%", marginTop: '15px'}}>
            <Recommendations data={recommendations} updateStats={showStats} 
                             updateGraph={showGraph} updatePagerankData={updatePagerank} 
                             updateGraphData={updateGraph} updatePagerank={showPagerank}/>
            <Divider orientation="vertical" variant="middle" flexItem />
            <Visualisation data={recommendations} graphData={graphData} pageRankData={pageRankData}
                           displayStats={displayStats} displayGraph={displayGraph} 
                           displayPagerank={displayPagerank}/>
          </div>
        </>
        ) :
        (
          isLoading ? 
            <Box sx={{ width: "35%", margin: "0 auto;", color: "#fb6e00"}}>
              <LinearProgress color='inherit' />
            </Box> : 
            <></>
        )
      }
    </div>
  );
}

export default App;
