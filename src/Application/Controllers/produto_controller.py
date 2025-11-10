from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from src.Infrastructure.Model.produto import Produto
from src.Application.Service.produto_service import ProdutoService
from src.Infrastructure.Model.venda import Venda
from supabase import create_client
import matplotlib
matplotlib.use('Agg')  
import os
import uuid
import pandas as pd
import io
import base64
import matplotlib.pyplot as plt

class ProdutoController:
    @staticmethod
    def register_produto():
        try:
            # Pega o ID do usuário do token
            user_id = get_jwt_identity()  # ← ADICIONE ESTA LINHA
            
            # Obtém os campos do formulário
            nome = request.form.get("nome")
            preco = request.form.get("preco")
            quantidade = request.form.get("quantidade")
            status_str = request.form.get("status", "True")
            status = True if status_str.lower() == "true" else False
            imagem = request.files.get("imagem")

            # Validação básica
            if not all([nome, preco, quantidade]):
                return jsonify({"erro": "Campos obrigatórios faltando."}), 400

            imagem_url = None

            # Upload da imagem, se houver
            if imagem:
                try:
                    # Inicializa o cliente Supabase
                    supabase = create_client(
                        os.getenv("SUPABASE_URL"),
                        os.getenv("SUPABASE_KEY")
                    )

                    # Cria nome único para a imagem
                    file_extension = imagem.filename.split('.')[-1]
                    unique_filename = f"{uuid.uuid4()}.{file_extension}"

                    # Faz upload para o bucket 'uploads'
                    supabase.storage.from_("uploads").upload(unique_filename, imagem.read())

                    # Gera URL pública correta
                    imagem_url = f"{os.getenv('SUPABASE_URL')}/storage/v1/object/public/uploads/{unique_filename}"

                except Exception as e:
                    return jsonify({"erro": f"Falha no upload da imagem: {str(e)}"}), 500

            # Cria o produto no banco, enviando a URL da imagem E o user_id
            produto = ProdutoService.criar_produto(
                nome, preco, quantidade, status, imagem_url, user_id  # ← ADICIONE user_id
            )

            
            return jsonify({
                "id": produto.id,
                "nome": produto.nome,
                "preco": produto.preco,
                "quantidade": produto.quantidade,
                "status": produto.status,
                "imagem": produto.imagem,
                "user_id": produto.user_id  # ← Opcional, para debug
            }), 201
        except Exception as e:
            return jsonify({"erro": f"Erro ao cadastrar produto: {str(e)}"}), 500
    

    @staticmethod
    def ativar_produto(id):
        """Ativar produto"""
        produto = ProdutoService.ativar_produto(id)
        
        if produto:
            return jsonify({
                "message": "Produto ativado com sucesso!",
                "produto": produto.to_dict_product()
            }), 200
        
        return jsonify({"erro": "Produto não encontrado"}), 404
    
    @staticmethod
    def inativar_produto(id):
        """
        Inativa um produto pelo ID (soft delete).
        """
        try:
            produto = ProdutoService.inativar_produto(id)

            if not produto:
                return jsonify({"erro": "Produto não encontrado"}), 404

            return jsonify({
                "id": produto.id,
                "nome": produto.nome,
                "preco": produto.preco,
                "quantidade": produto.quantidade,
                "status": produto.status,
                "imagem": produto.imagem
            }), 200

        except Exception as e:
            import traceback
            traceback.print_exc()
            return jsonify({"erro": f"Erro ao inativar produto: {str(e)}"}), 500
    

    @staticmethod
    def deletar_produto(id):
        produto = ProdutoService.excluir_produto(id)

        if produto:
            return jsonify({"message": "Produto excluído com sucesso"}), 200
        
        return jsonify({"message": "Erro ao excluir produto"}), 404
    
    @staticmethod 
    def list_product():
        """
        Retorna todos os produtos do usuário logado.
        """
        try:
            user_id = get_jwt_identity()
            
            
            produtos = ProdutoService.listar_produtos(user_id=user_id)
            
            if not produtos:
                return jsonify([]), 200  

            result = []
            for p in produtos:
                result.append({
                    "id": p.id,
                    "nome": p.nome,
                    "preco": float(p.preco),
                    "quantidade": int(p.quantidade),
                    "status": p.status,
                    "imagem": p.imagem if p.imagem else None
                })

            return jsonify(result), 200

        except Exception as e:
            import traceback
            traceback.print_exc()
            return jsonify({"erro": f"Erro ao listar produtos: {str(e)}"}), 500

    

    @staticmethod
    def att_produto(id):
        """
        Atualiza os dados de um produto pelo ID.
        """
        try:
            user_id = get_jwt_identity()
            if isinstance(user_id, str):
                user_id = int(user_id)

            produto = Produto.query.get(id)
            if not produto:
                return jsonify({"erro": "Produto não encontrado"}), 404

            if produto.user_id is not None and produto.user_id != user_id:
                return jsonify({"erro": "Você não tem permissão para editar este produto"}), 403

            data = request.get_json()  # pega os dados JSON
            nome = data.get("nome")
            preco = data.get("preco")
            quantidade = data.get("quantidade")
            # imagem continua vindo de form-files se houver upload
            imagem = request.files.get("imagem")

            imagem_url = produto.imagem
            if imagem:
                try:
                    supabase = create_client(
                        os.getenv("SUPABASE_URL"),
                        os.getenv("SUPABASE_KEY")
                    )
                    file_extension = imagem.filename.split('.')[-1]
                    unique_filename = f"{uuid.uuid4()}.{file_extension}"
                    supabase.storage.from_("uploads").upload(unique_filename, imagem.read())
                    imagem_url = f"{os.getenv('SUPABASE_URL')}/storage/v1/object/public/uploads/{unique_filename}"
                except Exception as e:
                    return jsonify({"erro": f"Falha no upload da imagem: {str(e)}"}), 500

            produto_atualizado = ProdutoService.atualizar_produtos(
                id=id,
                nome=nome if nome else None,
                preco=float(preco) if preco is not None else None,
                quantidade=int(quantidade) if quantidade is not None else None,
                imagem=imagem_url if imagem_url else None
            )

            if not produto_atualizado:
                return jsonify({"erro": "Produto não encontrado"}), 404

            return jsonify({
                "id": produto_atualizado.id,
                "nome": produto_atualizado.nome,
                "preco": float(produto_atualizado.preco),
                "quantidade": produto_atualizado.quantidade,
                "status": produto_atualizado.status,
                "imagem": produto_atualizado.imagem
            }), 200

        except ValueError:
            return jsonify({"erro": "Valores de preço ou quantidade inválidos"}), 400
        except Exception as e:
            import traceback
            traceback.print_exc()
            return jsonify({"erro": f"Erro ao atualizar produto: {str(e)}"}), 500
        
    @staticmethod
    def vender_produto(id):
        try:
            user_id = get_jwt_identity()  # pega o usuário logado

            if request.is_json:
                data = request.get_json()
                quantidade_venda = data.get("quantidade_venda")
            else:
                quantidade_venda = request.form.get("quantidade_venda")

            if quantidade_venda is None:
                return jsonify({"erro": "Campo 'quantidade_venda' obrigatório"}), 400

            quantidade_venda = int(quantidade_venda)

            # PASSAR user_id para o service
            nova_venda, erro = ProdutoService.vender_produto(id, quantidade_venda, user_id)

            if erro:
                return jsonify({"erro": erro}), 400

            # usar método do model para converter para dict
            venda_dict = nova_venda.to_dict_venda()

            return jsonify({"sucesso": "Produto vendido com sucesso!", "nova_venda": venda_dict})

        except ValueError:
            return jsonify({"erro": "Quantidade inválida"}), 400
        except Exception as e:
            return jsonify({"erro": str(e)}), 500

 

    @staticmethod
    def dashboard():

        """Dashboard completo com estatísticas de produtos e vendas do usuário logado"""
        try:
            
            user_id = get_jwt_identity()
            print(f"👤 Dashboard do User ID: {user_id}")
            
            # Busca produtos filtrados por usuário
            produtos = ProdutoService.listar_produtos(user_id=user_id)  # ← Passa o user_id
            
            if not produtos:
                return jsonify({
                    "total_produtos": 0,
                    "valor_total_estoque": 0.0,
                    "total_vendas": 0,
                    "faturamento_total": 0.0,
                    "produto_mais_vendido": None,
                    "grafico_status": None,
                    "grafico_vendas": None
                }), 200

            
            df_prod = pd.DataFrame([p.to_dict_product() for p in produtos])
            df_prod['preco'] = df_prod['preco'].astype(float)
            df_prod['quantidade'] = df_prod['quantidade'].astype(int)

            total_produtos = int(len(df_prod))
            total_ativos = int(len(df_prod[df_prod['status'] == 'ativo']))
            total_inativos = int(len(df_prod[df_prod['status'] == 'inativo']))
            valor_total_estoque = float(round((df_prod['preco'] * df_prod['quantidade']).sum(), 2))

            
            # Filtra vendas por usuário também
            vendas = Venda.query.filter_by(user_id=user_id).all()  # ← Adicione o filtro
            
            if vendas:
                df_vendas = pd.DataFrame([v.to_dict_venda() for v in vendas])
                df_vendas['preco_total'] = df_vendas['preco_total'].astype(float)
                df_vendas['quantidade_vendida'] = df_vendas['quantidade_vendida'].astype(int)

                total_vendas = int(df_vendas['quantidade_vendida'].sum())
                faturamento_total = float(round(df_vendas['preco_total'].sum(), 2))

                
                ranking_vendas = (
                    df_vendas.groupby('produto_nome')
                    .agg({'quantidade_vendida': 'sum', 'preco_total': 'sum'})
                    .sort_values(by='quantidade_vendida', ascending=False)
                    .reset_index()
                )
                produto_mais_vendido = ranking_vendas.iloc[0]['produto_nome'] if not ranking_vendas.empty else None

                
                plt.figure(figsize=(4, 3))
                df_prod['status'].value_counts().plot(kind='bar', color=['green', 'red'])
                plt.title('Produtos Ativos x Inativos')
                plt.xlabel('Status')
                plt.ylabel('Quantidade')
                buf1 = io.BytesIO()
                plt.tight_layout()
                plt.savefig(buf1, format='png')
                buf1.seek(0)
                grafico_status = base64.b64encode(buf1.getvalue()).decode('utf-8')
                plt.close()

                
                plt.figure(figsize=(5, 4))
                plt.barh(ranking_vendas['produto_nome'], ranking_vendas['quantidade_vendida'], color='skyblue')
                plt.title('Ranking de Produtos Mais Vendidos')
                plt.xlabel('Quantidade Vendida')
                plt.ylabel('Produto')
                plt.gca().invert_yaxis()
                buf2 = io.BytesIO()
                plt.tight_layout()
                plt.savefig(buf2, format='png')
                buf2.seek(0)
                grafico_vendas = base64.b64encode(buf2.getvalue()).decode('utf-8')
                plt.close()

            else:
                total_vendas = 0
                faturamento_total = 0.0
                produto_mais_vendido = None
                grafico_vendas = None

                
                plt.figure(figsize=(4, 3))
                df_prod['status'].value_counts().plot(kind='bar', color=['green', 'red'])
                plt.title('Produtos Ativos x Inativos')
                plt.xlabel('Status')
                plt.ylabel('Quantidade')
                buf1 = io.BytesIO()
                plt.tight_layout()
                plt.savefig(buf1, format='png')
                buf1.seek(0)
                grafico_status = base64.b64encode(buf1.getvalue()).decode('utf-8')
                plt.close()

            
            return jsonify({
                "total_produtos": total_produtos,
                "valor_total_estoque": valor_total_estoque,
                "total_vendas": total_vendas,
                "faturamento_total": faturamento_total,
                "produto_mais_vendido": produto_mais_vendido,
                "grafico_status": f"data:image/png;base64,{grafico_status}",
                "grafico_vendas": f"data:image/png;base64,{grafico_vendas}" if grafico_vendas else None
            })
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return jsonify({"erro": f"Erro ao gerar dashboard: {str(e)}"}), 500