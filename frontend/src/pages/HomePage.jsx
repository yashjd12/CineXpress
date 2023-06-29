import Typography  from "@mui/material/Typography";
import Box  from "@mui/material/Box";
import background from '../images/background.png'
import TextField  from "@mui/material/TextField";
import InputAdornment  from "@mui/material/InputAdornment";
import Button  from "@mui/material/Button";
import { Stack } from "@mui/system";
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';
import { useState } from "react";
import { useEffect } from "react";
import axiosInstance, { mediaUrl } from "../AxiosInstance";
import { useNavigate } from "react-router-dom";
import {SiScrollreveal} from 'react-icons/si'

const popularMovieSx = {width:"214px",height:"290px",background:"green",borderRadius:'5px','&:hover':{
    transform:'scale(1.1)',
    transition:"all 0.3s ease-in-out"
}
};
const upcomingMovieSx = {width:"400px",height:"240px",background:"green",borderRadius:'5px','&:hover':{
    transform:'scale(1.1)',
    transition:"all 0.3s ease-in-out"
}};

export const HomePage = () =>{

    const navigate = useNavigate();
    const [movies,setMovies] = useState();
    const [upcomingMovies,setUpcomingMovies] = useState();
    
    useEffect(()=>{
        axiosInstance.get('/movies/all').then(res=>{
            setMovies(res.data)
        })
        axiosInstance.get('/upcoming-movies').then(res=>{
            setUpcomingMovies(res.data)
        })
    },[])

    const browseMovies = () => {
        document.documentElement.scrollTo({
            top:550,
            behavior:"smooth"
        })
    }


    return(
        <>
        <Box component="img" sx={{width:"100%",backgroundRepeat:'repeat',backgroundSize:'cover',zIndex:"-1",position:"absolute",opacity:"0.1"}} src={background}></Box>
        <Box sx={{zIndex:"1",padding:"150px 100px"}}>
            <Typography variant='h6' sx={{color:"#ed6c02"}} >
                Welcome to BD Screens
            </Typography>
            <Typography variant='h3' sx={{margin:"20px 0px"}}>
                Easily Book tickets <br/>
                for your favourite Movie <br/>
                in just a click 
            </Typography>
           <Button color="warning" variant="contained" endIcon={<SiScrollreveal/>} onClick={browseMovies}>Browse Movies</Button>
        </Box>
        <Box sx={{padding:"30px 30px",display:'flex',justifyContent:"space-between"}}>
            <Typography variant="h5">Most Popular</Typography>
            <Button variant='contained' color="warning" endIcon={<ArrowForwardIcon/>}>See All</Button>
        </Box>
        <Box sx={{padding:"20px 30px 70px 30px"}}>
                    <Stack spacing={4} direction="row" justifyContent='space-between'>
                        {movies?movies.map((movie)=>(
                            <Box sx={popularMovieSx} onClick={()=>navigate('/movie-detail/'+movie.id)}>
                                <Box component="img" src={mediaUrl + movie.image}/>
                                <Typography sx={{background:"black",padding:"5px 10px",borderRadius:"0px 0px 10px 10px",color:"white"}}>{movie.name}</Typography>
                            </Box>
                        )):null}
                    </Stack>
                </Box>
        <Box sx={{padding:"30px 30px",display:'flex',justifyContent:"space-between"}}>
            <Typography variant="h5">Upcoming Movies</Typography>
            <Button variant='contained' color="warning" endIcon={<ArrowForwardIcon/>}>See All</Button>
        </Box>  
        <Box sx={{padding:"50px 30px 70px 30px"}}>
            <Stack spacing={4} direction="row">
                {upcomingMovies?upcomingMovies.map((movie)=>(
                    <Box sx={upcomingMovieSx}>
                        <Box component="img" src={mediaUrl + movie.image}/>
                        <Typography sx={{background:"black",color:"white",padding:"5px 10px",borderRadius:"0px 0px 10px 10px"}}>{movie.name}</Typography>
                    </Box>
                )):null}
            </Stack>
        </Box>
        </>
    );
}