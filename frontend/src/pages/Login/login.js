import "./login.css"
import { useState } from "react";
import { useNavigate } from "react-router-dom";
function Login() {
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const response = await fetch('http://localhost:5000/verifica', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: email,
          password: senha
        })
      });

      const data = await response.json();

      if (response.ok) {
        alert("Login realizado com sucesso!");
        navigate("/");
      } else {
        alert(data.message || "Email ou senha incorretos!");
      }
    } catch (error) {
      console.error("Erro ao fazer login:", error);
      alert("Erro ao conectar com o servidor!");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container2">
      <form id="quadrado_login" onSubmit={handleSubmit}>
      <h1>Login</h1>
      <div className="grupo">
        <input name="email" type="email" placeholder="E-mail" value={email} onChange={(e) => setEmail(e.target.value)} required disabled={loading}/>
        <input name="password" type="password" placeholder="Senha" value={senha} onChange={(e) => setSenha(e.target.value)} required disabled={loading}/>
      </div>
      <button type="submit" disabled={loading}>{loading ? "Carregando..." : "Logar"}</button>
      </form>

    </div>

    
      
  
  );
}

export default Login;
