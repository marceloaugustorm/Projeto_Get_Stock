import "./cadastrar.css";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

function Cadastro() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    cnpj: "",
    celular: "",
  });

  const handleChange = (e) => {
    setFormData({...formData, [e.target.name]: e.target.value});
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log("Enviando dados:", formData);

    try{
      const response = await fetch('http://localhost:5000/user', {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(formData),
      });

      if(response.ok){
        const data = await response.json();
        localStorage.setItem("cnpj", formData.cnpj);
        alert("Usuário cadastrado com sucesso!");
        navigate("/verificar_cod");
      } else{
        alert("Erro ao cadastrar usuário!");
      }
    } catch (error){
      console.error("Erro na requisição:", error)
      alert("Falha na comunicação com o servidor.")
    }
    
  };

  return (
    <div className="container">
      <form id="cadastro_form" onSubmit={handleSubmit}>
      <h2>Informações Pessoais</h2>
      <div className="grupo">
        <input name="name" placeholder="Nome" value={formData.name} onChange={handleChange}/>
        <input name="email" placeholder="E-mail" value={formData.email} onChange={handleChange}/>
        <input name="password" placeholder="Senha" value={formData.password} onChange={handleChange}/>
        <input name="cnpj" placeholder="CNPJ" value={formData.cnpj} onChange={handleChange}/>
        <input name="celular" placeholder="Celular" value={formData.celular} onChange={handleChange}/>
      </div>
      <button type="submit">Cadastrar</button>

      </form> 


    </div>
    
  );
}

export default Cadastro;
