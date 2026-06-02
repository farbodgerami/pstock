import  { useState, } from "react";
import style from "./Form.module.css";
import Form from "../components/form";
import { register } from "../axioses";
import { useNavigate } from "react-router-dom";
const Register = () => {
  const [username, setname] = useState("");
  const [email, setemail] = useState("");
  const [password, setpassword] = useState("");
  const [message, setmessage] = useState("");
  const [error, seterror] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const submithandeler = async (e) => {
    e.preventDefault();
    const data = await register(username, email, password, setLoading);
    setLoading(false);
    if (data.status === 200) {
      // setmessage(data.error.response.data.detail)
      setmessage("user created successfully");
      setTimeout(() => {
        setmessage("");
      }, 1000);
      navigate("/login");
    } else {
      seterror(data.data.detail);
      setTimeout(() => {
        seterror("");
      }, 3000);
    }
  };

  return (
    <div className={style.body}>
      <Form onSubmit={submithandeler}>
        <h1>Create an account</h1>

        <label>User Name</label>
        <input
          type="text"
          onChange={(e) => setname(e.target.value)}
          required
          placeholder="enter your name"
          value={username}
        />
        <label>Email:</label>
        <input
          type="email"
          onChange={(e) => setemail(e.target.value)}
          placeholder="enter your email"
          value={email}
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
        <button type="submit">Register</button>
      </Form>
    </div>
  );
};

export default Register;
