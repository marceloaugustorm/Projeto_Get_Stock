import "./verificar_cod.css";
import { useState } from "react";
import { useNavigate } from "react-router-dom";


function Verificar(){
  const navigate = useNavigate();
  const [codigo, setCodigo] = useState("");

  const handleChange = (e) => {
    setCodigo(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const cnpj = localStorage.getItem("cnpj");


    if (!codigo) {
      alert("Por favor, insira o código recebido por SMS.");
      return;
    }

    try {
    const response = await fetch("http://localhost:5000/verifica/code", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        cnpj: cnpj, // use o mesmo CNPJ cadastrado
        codigo_digitado: codigo, // o valor que o usuário digitou
      }),
    });

      if (response.ok) {
        const data = await response.json();
        console.log("Código verificado:", data);
        alert("Código verificado com sucesso!");
        navigate("/login"); // redireciona para login
      } else {
        const errorData = await response.json();
        console.error("Erro:", errorData);
        alert("Código inválido ou expirado!");
      }
    } catch (error) {
      console.error("Erro na requisição:", error);
      alert("Falha ao verificar o código. Tente novamente.");
    }
  };

    return(
        <div className="container">
            <form id="cadastro_form" onSubmit={handleSubmit}>
            <h2>Confirme sua conta:</h2>
            <div className="grupo">
                <input name="codigo_validacao" placeholder="Código" value={codigo} onChange={handleChange}/>
            </div>
            <button type="submit">Cadastrar</button>

            </form> 


        </div>
    )
}

export default Verificar;