import React, { useState } from 'react';
import axios from 'axios';
import { FormControl, Button, TextField, Box, Tooltip, Typography } from '@mui/material';
import ExpandLessIcon from '@mui/icons-material/ExpandLess';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';

export const Form = ({updateRecs, updateLoader, updateDisplay}) => {

    const [show, setShow] = useState(true)
    const [url, setUrl] = useState("")
    const [validUrl, setValidUrl] = useState(true)
    const [text, setText] = useState("")

    const handleUrlChange = (event) => { setUrl(event.target.value) }

    const handleTextChange = (event) => { setText(event.target.value) }

    const handleSubmit = async(event) => {
        event.preventDefault()

        let okRequest = true

        if(!isValidHttpUrl(url)) {
            setValidUrl(false)
            return
        }
        else setValidUrl(true)

        updateLoader(true)
        updateDisplay(false)

        var bodyFormData = new FormData()
        bodyFormData.append("url", url)
        bodyFormData.append("text", text)
        
        const response = await axios({
            method: "post",
            url: "http://localhost:5000/recommendations",
            data: bodyFormData,
        }).catch(error => {
            okRequest = false
            updateLoader(false)
            updateDisplay(false)
            if(error.response.status === 404){
                alert("Page not found.")
                return
            }
            else if(response.status === -1) {
                alert("Nothing to recommend.")
                updateRecs({})
                return
            }
            else{
                alert("Something went wrong.")
                return
            }
        })
        if(okRequest){        
            updateLoader(false)
            updateDisplay(true)
            updateRecs(response.data, url)
        }
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
                <> 
                    <Typography sx={{ paddingBottom: "20px", fontSize: "18px"}} variant="subtitle1">
                        Welcome to Docs Recommendation System! Fill form below and get the best documentation recommendations.
                    </Typography>
                    <FormControl style={{ width: "35%"}} >
                        <Tooltip title={<span style={{ fontSize: "14px" }}>Add any URL of certain documentation</span>} placement="left" arrow>
                            <TextField sx={{ marginBottom: "20px" }} label="URL" variant="standard"
                                    required onChange={handleUrlChange} 
                                    error={!validUrl} helperText={!validUrl ? "URL is not valid" : ""}/>
                        </Tooltip>
                        <Tooltip title={<span style={{ fontSize: "14px" }}>Optionally, recommend pages within the documentation based on this text</span>} placement="right" arrow>
                            <TextField sx={{ marginBottom: "10px" }} 
                                    id="standard-multiline-static" 
                                    label="Text" 
                                    multiline rows={8} defaultValue="" variant="standard"
                                    onChange={handleTextChange}/>
                        </Tooltip>
                        <Button onClick={handleSubmit} disabled={url === ""}>Recommend</Button>
                    </FormControl>
                </>
            }
            </Box>
            <Button onClick={() => setShow(prev => !prev)}>
                {show && <><ExpandLessIcon sx={{color: "#fb6e00"}} /></>}
                {!show && <>Show form<ExpandMoreIcon sx={{color: "#fb6e00"}} /></>}
            </Button>
        </>
    );
}

export default Form;