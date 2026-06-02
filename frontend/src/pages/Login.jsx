import { useContext, useState } from "react";
import style from "./Form.module.css";
import Form from "../components/form";
import { login } from "../axioses";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../AuthProvider";

const Login = () => {
  const [username, setname] = useState("");
  const [password, setpassword] = useState("");
  const [message, setmessage] = useState("");
  const [error, seterror] = useState("");
  const [loading, setLoading] = useState(false);
  const { setIsLoggedIn,   } = useContext(AuthContext);
  const navigate = useNavigate();
  const submithandeler = async (e) => {
    e.preventDefault();
    const respose = await login(username, password, setLoading);
    setLoading(false);
    if (respose.status === 200) {
 
      localStorage.setItem("accessToken", respose.data.access);
      localStorage.setItem("refreshToken", respose.data.refresh);
      setIsLoggedIn(true);
      setmessage("logged in successfully");
      setTimeout(() => {
        setmessage("");
      }, 1000);
      navigate("/");
    } else {
      seterror("username or password is wrong");
      setTimeout(() => {
        seterror("");
      }, 3000);
    }
  };

  return (
    <div className={style.body}>
      <Form onSubmit={submithandeler}>
        <h1>Logn youe account</h1>

        <label>User Name</label>
        <input
          type="text"
          onChange={(e) => setname(e.target.value)}
          required
          placeholder="enter your name"
          value={username}
        />

        <label>Password:</label>
        <input
          type="password"
          placeholder="enter Password"
          onChange={(e) => setpassword(e.target.value)}
          value={password}
        />

        {message && <p className={style.message}>{message}</p>}
        {error && <p className={style.error}>{error}</p>}
        {loading && <p>please wait...</p>}
        <button type="submit">Login</button>
      </Form>
    </div>
  );
};
export default Login;
