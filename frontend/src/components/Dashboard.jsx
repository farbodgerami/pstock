import styles from "./Dashboard.module.css";
import { useEffect, useState } from "react";
import { ROOT_BASE_URL } from "../constants";
import { fetchProtectedData, stocksDataSend } from "../axioses";
import Form from "../components/form";
const Dashboard = () => {
  const [ticker, setTicker] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [plot,setPlot]=useState()
  const [ma100,setMa100]=useState( )
  const [ma200,setMa200]=useState( )
  const [prediction,setPrediction]=useState()
  const[mse,setMse]=useState()
  const [rmse,setRmse]=useState()
  const [r2,setR2]=useState()

  const getData = async () => {
    const response = await fetchProtectedData();
    
  };

  const submithandeler = async (e) => {
    e.preventDefault();
    const respose = await stocksDataSend(ticker,setLoading);
      setLoading(false);
    
    if (respose.status === 200) {
      const plotUrl=ROOT_BASE_URL+respose.data.plot_img
      const plotUrl100=ROOT_BASE_URL+respose.data.plot_100_img
      const plotUrl200=ROOT_BASE_URL+respose.data.plot_200_img   
      const final_predition_img=ROOT_BASE_URL+respose.data.plot_final_predition_img
      setPlot(plotUrl)
      setMa100(plotUrl100)
      setMa200(plotUrl200)
      setPrediction(final_predition_img)
      setMse(respose.data.mse)
      setR2(respose.data.r2)
      setRmse(respose.data.rmse)
   
    } else {
 
      setError(respose.data)
         setTimeout(() => {
        setError("");
      }, 3000);
    }
  };

  useEffect(() => {
    getData();
  }, []);
  return (
    <div className={styles.container}>
      <Form onSubmit={submithandeler}>
        {/* <label>User Name</label> */}
        <input
          type="text"
          onChange={(e) => setTicker(e.target.value)}
          required
          placeholder="Enter Stock Ticker"
          value={ticker}
        />
        {error && <p className={styles.error}>{error}</p>}
        {loading && <p>please wait...</p>}
        <button type="submit">See Prediction</button>
      </Form>
      <div className={styles.image}>
      {plot && <img src={plot} style={{maxWidth:'100%'}}/>}
      {ma100 && <img src={ma100} style={{maxWidth:'100%'}}/>}
      {ma200 && <img src={ma200} style={{maxWidth:'100%'}}/>}
      {prediction && <img src={prediction} style={{maxWidth:'100%'}}/>}

      </div>
      {mse &&<>
      <h4>Model Evaluation</h4>
      <p>Mean Squared Error (MSE): {mse}</p>
      <p>Root Mean Squared Error (RMSE):{rmse}</p>
      <p>R-squaed: {r2}</p>
      </>
      }
    </div>
  );
};

export default Dashboard;
