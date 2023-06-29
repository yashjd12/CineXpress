import { ThemeProvider } from '@mui/material';
import { createTheme } from '@mui/material/styles';
import {
  BrowserRouter,
  Routes,
  Route,
} from "react-router-dom"; import { Footer } from './Components/Footer';
import { Navbar } from './Components/Navbar';
import { HomePage } from './pages/HomePage';
import { MovieDetail } from './pages/MovieDetail';
import { MyBookings } from './pages/MyBookings';
import { Profile } from './pages/Profile';
import { decodeToken, useJwt } from "react-jwt";
import { useEffect } from 'react';

const theme = createTheme({
  typography: {
    fontFamily: "gilroy",
    button: {
      fontWeight: "bold",
      // background: "rgba(0,0,0,0)",
    },
    p: {
      fontWeight: "bold",
    },
    h2: {
      fontWeight: "bold",
    },
    h3: {
      fontWeight: "bold",
    },
    h4: {
      fontWeight: "bold",
    },
    h5: {
      fontWeight: "bold",
    },
    h6: {
      fontWeight: "bold"
    },
    body1:{
      fontWeight: "bold", 
    },
    body2:{
      fontWeight: "bold",
    }
  },
  palette: {
    type: "dark",
    primary: {
      main: '#000000',
    },
  }
})

function App() {

    const { decodedToken, isExpired } = useJwt(sessionStorage.getItem('token'));
    let currTime = Math.floor(Date.now()/1000)

  return (
    <ThemeProvider theme={theme}>
      <BrowserRouter>
        <Navbar />
        <Routes>
          {decodedToken?
            decodedToken.exp+6000
            <currTime?sessionStorage.removeItem('token'):null
          :null}
          <Route path='/' element={<HomePage />}/>
          <Route path='/movie-detail/:id' element={<MovieDetail />}/>
          <Route path='/my-bookings' element={<MyBookings />}/>
          <Route path='/profile' element={<Profile />}/>
        </Routes>
        <Footer />
      </BrowserRouter>
    </ThemeProvider>
  );
}

export default App;
