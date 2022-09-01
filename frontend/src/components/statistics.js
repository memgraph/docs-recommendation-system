import { Box } from "@mui/material";
import React, {useState, useEffect} from "react";
import { ListSubheader, List } from '@mui/material';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';


export const Statistics = ({ data }) => {

    const [recs, setRecs] = useState([])
    const [names, setNames] = useState({})
    const [keywords, setKeywords] = useState({})
    const [similarities, setSimilarities] = useState([])

    useEffect(() => {
        setRecs(data["tf-idf"])
        setNames(data["names"])
        setKeywords(data["top_keywords"])
        setSimilarities(data["similarities"])
      }, [data])

    const getPageName = (link) => { return names[link] }
      
    return ( 
        <Box sx={{ width: "60%", justifyContent: 'center' }}>
            <List sx={{paddingLeft: "4%"}} subheader={
                <ListSubheader sx={{ display: 'inline-flex', fontSize: "19px" }} disableSticky={true}>
                    Statistics of the TF-IDF algorithm
                </ListSubheader>}>
                <TableContainer component={Paper}>
                    <Table size="small" aria-label="a dense table">
                        <TableHead>
                            <TableRow style={{background: "#F0F0F0" }}>
                                <TableCell sx={{ fontWeight: 'bold' }}>Most important word</TableCell>
                                <TableCell align="center" sx={{ fontWeight: 'bold' }}># of documents</TableCell>
                                <TableCell align="right" sx={{ fontWeight: 'bold' }}>% of documents</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {Object.keys(keywords).map((key, value) => (
                                <TableRow key={value} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
                                    <TableCell component="th" scope="row">{key}</TableCell>
                                    <TableCell align="center">{keywords[key][0]}</TableCell>
                                    <TableCell align="right">
                                        { keywords[key][1] }
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </TableContainer>
                <TableContainer sx={{ marginTop: "10px" }} component={Paper}>
                    <Table size="small" aria-label="a dense table">
                        <TableHead>
                            <TableRow style={{background: "#F0F0F0" }}>
                                <TableCell sx={{ fontWeight: 'bold' }}>Document</TableCell>
                                <TableCell align="right" sx={{ fontWeight: 'bold' }}>Similarity score (cos)</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            { recs.map((item, index) => (
                                <TableRow key={index} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
                                    <TableCell component="th" scope="row">{getPageName(item)}</TableCell>
                                    <TableCell align="right">{similarities[index]}</TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </TableContainer>
            </List>
        </Box> 
    );
}

export default Statistics;