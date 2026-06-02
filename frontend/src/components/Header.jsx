import style from "./Header.module.css";
import LinkButton from "./LinkButton";
import { Link } from "react-router-dom";
import  { useContext,   } from "react";
import { AuthContext } from "../AuthProvider";
import bottunstyle from "./LinkButton.module.css";
const Header = () => {
    const {setIsLoggedIn,isLoggedIn}=useContext(AuthContext)
    const logoutOnclick=()=>{
    localStorage.removeItem("accessToken");
        localStorage.removeItem("refreshToken");
         window.location.replace("/");
    }
  return (
    <div className={style.header}>

    <nav className={style.container}>
      <Link className={style.headerLink} to='/'>Stock Prediction Portal</Link>
      <div className={style.bottonContainer}>
        {isLoggedIn? 
        <>
        <LinkButton buttonName='Dashboard' to='dashboard'  />
        <LinkButton buttonName='Logout' to='#' onClick={logoutOnclick}/>
        </>
     
        :(
<>
          <LinkButton buttonName='Register' to='/register'/>
          <LinkButton buttonName='Login' to='/login'/>
</>
        )
      }
 
      </div>
    </nav>
    </div>
  );
};

export default Header;
