import "./assets/css/style.css";

import { BrowserRouter, Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import Register from "./pages/Register";
import Login from "./pages/Login";
import Footer from './components/Footer'
import Header from './components/Header'
import Dashboard from './components/Dashboard'
import AuthProvider from "./AuthProvider";
import PriveteRoute from "./PriveteRoute";
function App() {
  return (
    <div className="app">
      <AuthProvider>

      <BrowserRouter>
      <Header />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/register" element={<Register />} />
          <Route path="/Login" element={<Login />} />
          <Route path="/dashboard" element={<PriveteRoute><Dashboard /></PriveteRoute>} />
     
        </Routes>
      <Footer />
      </BrowserRouter>
      </AuthProvider>
    </div>
  );
}

export default App;
