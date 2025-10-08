import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Header from "./components/header";
import Home from "./pages/HomePage/home";
import Login from "./pages/Login/login";
import Cadastro from "./pages/Cadastrar/cadastrar";
import Verificar_cod from "./pages/Verificar_cod/verificar_cod";

function App() {
  return (
    <Router>
      <Header /> {/* aparece em todas as páginas */}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/cadastro" element={<Cadastro />} />
        <Route path="/verificar_cod" element={<Verificar_cod />} />
      </Routes>
    </Router>
  );
}

export default App;