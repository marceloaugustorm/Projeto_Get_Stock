import { Link } from "react-router-dom";
import "./header.css";

function Header() {
  return (
    <header className="header">
      <div className="logo">GetStock</div>

      <nav className="nav">
        <ul>
          <li><Link to="/">Home</Link></li>
          <li><Link to="/login">Login</Link></li>
          <li><Link to="/cadastro">Cadastrar</Link></li>
        </ul>
      </nav>
    </header>
  );
}

export default Header;
