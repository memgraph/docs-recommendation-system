import React, { useState } from 'react';
import axios from 'axios';
import { FormControl, Input, Button, TextField, Box} from '@mui/material';
import ExpandLessIcon from '@mui/icons-material/ExpandLess';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';

export const Form = ({updateRecs, updateLoader, updateDisplay}) => {

    const [show, setShow] = useState(true)
    const [url, setUrl] = useState("")
    const [text, setText] = useState("")

    const handleUrlChange = (event) => { setUrl(event.target.value) }

    const handleTextChange = (event) => { setText(event.target.value) }

    const handleSubmit = async(event) => {
        event.preventDefault()

        if(!isValidHttpUrl(url))  {
            alert("URL is not valid.")
            return
        }
        updateLoader(true)
        updateDisplay(false)

        var bodyFormData = new FormData()
        bodyFormData.append("url", url)
        bodyFormData.append("text", text)
        
        const response = await axios({
            method: "post",
            url: "http://localhost:5000/recommendations",
            data: bodyFormData,
        });
        console.log("response:", response)
        let res = response.data
        if(res === 404){
            alert("Page not found.")
            updateLoader(false)
            updateDisplay(false)
            return
        }
        if(res === -1) {
            alert("Nothing to recommend.")
            updateLoader(false)
            updateDisplay(false)
            updateRecs({})
            return
        }
        updateLoader(false)
        updateDisplay(true)
        //console.log("form.js:", res)
        updateRecs(res)
    }

    const isValidHttpUrl = (string) => {
        let url
        
        try {
          url = new URL(string)
        } catch (_) {
          return false
        }
      
        return url.protocol === "http:" || url.protocol === "https:"
      }

    return (
        <>
            <Box>
            {show && 
                <FormControl style={{ width: "35%"}} >
                    <Input sx={{ marginBottom: "20px" }} placeholder="documentation link" onChange={handleUrlChange}/>
                    <TextField sx={{ marginBottom: "10px" }} 
                            id="standard-multiline-static" 
                            label="Recommend by text:" 
                            multiline rows={8} defaultValue="" variant="standard"
                            onChange={handleTextChange}/>
                    <Button onClick={handleSubmit}>Recommend</Button>
                </FormControl>
            }
            </Box>
            <Button onClick={() => setShow(prev => !prev)}>
                {show && <ExpandLessIcon sx={{color: "#fb6e00"}}></ExpandLessIcon>}
                {!show && <ExpandMoreIcon sx={{color: "#fb6e00"}}></ExpandMoreIcon>}
            </Button>
        </>
    );
}

export default Form;