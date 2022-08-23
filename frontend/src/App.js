import React, { useEffect, useState } from 'react';
import './App.css';
import { Form } from './components/form';
import { Header } from './components/header';
import { Visualisation } from './components/D3';
import { Recommendations } from './components/recommendations';
import { Box, LinearProgress, Divider } from '@mui/material';


const App = () => {

  const [recommendations, setRecommendations] = useState({})
  const [isLoading, setIsLoading] = useState(false)
  const [displayRecs, setDisplayRecs] = useState(false)

  useEffect(() => { setDisplayRecs(false) }, [])

  const updateRecommendations = (data) => { setRecommendations(data) }

  const updateLoader = (value) => { setIsLoading(value) }

  const updateDisplay = (value) => { setDisplayRecs(value) }
  
  return (
    <div className="App">
      <Header />
      <Form updateRecs={updateRecommendations} updateLoader={updateLoader} updateDisplay={updateDisplay}/>
      {
        displayRecs ? 
        (
          <div className="flexbox-container" style={{ width: '90%', paddingLeft: "5%", marginTop: '15px'}}>
            <Recommendations data={recommendations}/>
            <Divider orientation="vertical" variant="middle" flexItem />
            <Visualisation />
          </div>
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
