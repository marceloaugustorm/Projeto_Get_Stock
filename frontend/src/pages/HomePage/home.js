import { Link } from "react-router-dom";
import "./home.css";

function Home() {
  return (
    <div className="home-container">
      <h1>Bem-vindo ao Mercado X</h1>
      <p>Escolha uma opção:</p>
      <div className="home-buttons">
        <Link to="./Login/login">
          <button>Entrar</button>
        </Link>
        <Link to="./Cadastrar/cadastrar">
          <button>Cadastrar</button>
        </Link>
      </div>
    </div>
  );
}

export default Home;
