import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Header from "./components/header";
import Home from "./pages/HomePage/home";
import Login from "./pages/Login/login";
import Cadastro from "./pages/Cadastrar/cadastrar";

function App() {
  return (
    <Router>
      <Header /> {/* aparece em todas as páginas */}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/cadastro" element={<Cadastro />} />
      </Routes>
    </Router>
  );
}

export default App;