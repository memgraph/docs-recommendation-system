import React, { useState, useEffect } from 'react';
import './App.css';

const Header = () => {
    return (
        <h1> Docs recommendation system </h1>
    );
}

async function fetchRecommendations() {
const res = await fetch("/languages");
res
  .json()
  .then((res) => setLanguages(res.languages))
  .catch((err) => setErrors(err));
}



const Form = () => {
   const [data, setData] = useState([])

    useEffect(() => {
       fetch("/recommendations").then(res => res.json()).then(
          data => {
              setData(data)
              console.log(data)
          }
       )
       }, []
    )

    return (
        <>
            <div className="form-div">
                <div>
                    <label for="url">URL:</label>
                    <input type="text" name="input-url" />
                </div>
                <br />
                <button>Go!</button>
            </div>
        </>
    );
}

const Visualisation = () => {
    return (
        <h1>Here goes D3.</h1>
    );
}

const App = () => {
  return (
    <div className="App">
      <Header />
      <div className="flexbox-container">
          <Form />
          <Visualisation />
      </div>
    </div>
  );
}

export default App;
