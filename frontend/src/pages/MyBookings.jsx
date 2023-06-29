import { Box, Button, Collapse, Dialog, DialogActions, Divider, IconButton, Paper, Typography } from "@mui/material";
import { Stack } from "@mui/system";
import { useEffect } from "react";
import { useState } from "react";
import { HiOutlineTicket } from "react-icons/hi";
import { MdDelete } from "react-icons/md";
import axiosInstance from "../AxiosInstance";


export const MyBookings = () =>{


    const [bookedSeats,setBookedSeats] = useState();
    const [open,setOpen] = useState(false);

    useEffect(()=>{
        const userId = sessionStorage.getItem("userId")
        axiosInstance.get('/get-booked-seats-for-user/'+userId).then(res=>{
            console.log(res.data);
            setBookedSeats(res.data);
        })
    },[]);

    // {userId:sessionStorage.getItem('userId'),movieId,seat}

    const cancelBooking = (movieId,seat) => {
        axiosInstance.delete('cancel-booked-seat',{
            data: {
                userId:sessionStorage.getItem('userId'),
                movieId,
                seat
            }
          })
        console.log(seat)
        console.log(movieId)
        let temp = bookedSeats.filter(function(s){
            return !(s.movieId === movieId && s.seat===seat)
        })
        setBookedSeats(temp)
        setOpen(false)
    }


    return (
        <>
            <Box sx={{width:"100%",height:"100px",background:"rgba(0,0,0,0)"}}/>
            <Paper elevation={7} sx={{width:"600px",borderRadius:"30px",margin:"auto",padding:"15px"}}>
                <Typography variant='h5' textAlign='center' sx={{color:"#ed6c02",textShadow:"1px 1px 1px black"}}>My Bookings</Typography>
                <Divider sx={{background:"black",border:"1px solid black",margin:"10px 0px"}}/>
                    <Stack spacing={3}>
                    {bookedSeats ? 
                    bookedSeats.map((seat)=>(
                        <Paper sx={{padding:"20px",borderRadius:"20px",display:"flex",justifyContent:"space-around",alignItems:'center'}} elevation={4}>
                            <Box sx={{display:"flex",justifyContent:"center",alignItems:"center"}}>
                                <HiOutlineTicket fontSize="40px"/>
                                <Typography sx={{margin:"0px 20px"}}>{seat.name}</Typography>
                            </Box>
                            <Typography  sx={{background:"black",color:"white",width:"40px",borderRadius:"5px",lineHeight:"40px",textAlign:"center",margin:"0px 5px"}}>{seat.seat}</Typography>
                            <IconButton color="warning" onClick={()=>setOpen(true)}><MdDelete/></IconButton>
                            
                            
                            <Dialog open={open}>
                                <Box sx={{padding:"20px"}}>
                                    <Typography>Are you sure you want to cancel booking?</Typography>
                                    <DialogActions>
                                        <Button color='success' variant='contained' onClick={()=>setOpen(false)}>No</Button>
                                        <Button color='warning' variant='contained' onClick={()=>cancelBooking(seat.movieId,seat.seat)} autoFocus>
                                            Yes
                                        </Button>
                                        </DialogActions>
                                </Box>
                            </Dialog>

                        </Paper>
                    )): <>Loading..</>}
                    </Stack>
            </Paper>

            
        </>
    );
}