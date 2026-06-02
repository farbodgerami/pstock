import { STE_BASE_URL } from "./constants";
import axios from "axios";

export const register = async (username, email, password, setLoading) => {
  try {
    setLoading(true);
    const config = { headers: { "Content-type": "application/json" } };
    const response = await axios.post(
      STE_BASE_URL + "/register/",
      { username: username, email: email, password: password },
      config,
    );

    return response;
  } catch (error) {
    return error.response;
  }
};

export const login = async (username, password, setLoading) => {
  try {
    setLoading(true);
    const config = { headers: { "Content-type": "application/json" } };
    const response = await axios.post(
      STE_BASE_URL + "/token/",
      { username: username, password: password },
      config,
    );

    return response;
  } catch (error) {
    return error.response;
  }
};

export const fetchProtectedData = async () => {
  const accessToken = localStorage.getItem("accessToken");
  
  try {
    const response = await axios.get(STE_BASE_URL + "/protected-view/", {
      headers: {"Content-type": "application/json", Authorization: `Bearer ${accessToken}` },
    });
    return response;
  } catch (error) {
    return error.response;
  }
};


export const stocksDataSend = async (ticker,setLoading) =>{
  const accessToken = localStorage.getItem("accessToken");
   try {
      setLoading(true);
    const config = {
      headers: {"Content-type": "application/json", Authorization: `Bearer ${accessToken}` },
    }
    const response = await axios.post(STE_BASE_URL + "/predict/",{ticker:ticker}, config,);
    return response;

      } catch (error) {
     
    return error.response;
  }
    };
 
