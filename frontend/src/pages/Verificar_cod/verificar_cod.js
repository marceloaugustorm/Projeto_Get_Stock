import "./verificar_cod.css";




function Verificar(){
    return(
        <div className="container">
            <form id="cadastro_form">
            <h2>Confirme sua conta:</h2>
            <div className="grupo">
                <input name="codigo_validacao" placeholder="Código"/>
            </div>
            <button type="submit">Cadastrar</button>

            </form> 


        </div>
    )
}

export default Verificar;