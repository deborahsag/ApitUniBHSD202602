from fastapi import FastAPI, HTTPException

from database import conectar_banco, criar_tabelas, inserir_novo_registro, consultar_registros, \
    consultar_registro_por_id, atualizar_registro_existente, remover_registro
from models import RegistroBase, RegistroResponse

app = FastAPI(
    title="API de Gerenciamento - Projeto A3",
    description="Template inicial integrando FastAPI, SQLite e validações Pydantic.",
    version="1.0.0"
)


# Cria e conecta ao banco de dados
conectar_banco()

# Cria a tabela automaticamente ao iniciar a API
@app.on_event("startup")
def startup_event():
    criar_tabelas()


# ==========================================
# 3. CAMADA DE ROTAS (Endpoints HTTP)
# ==========================================

@app.post("/registros", response_model=RegistroResponse, status_code=201)
def criar_registro(registro: RegistroBase):
    # Requisito 5: Código 400 (Bad Request) para regra de negócio inválida
    if not registro.titulo.strip():
        raise HTTPException(status_code=400, detail="O título não pode estar em branco.")

    try:
        novo_id = inserir_novo_registro(registro)
        return {**registro.model_dump(), "id": novo_id}
    except Exception as e:
        # Requisito 5: Código 500 (Internal Server Error)
        raise HTTPException(status_code=500, detail=f"Erro interno no banco de dados: {str(e)}")


@app.get("/registros", response_model=list[RegistroResponse], status_code=200)
def listar_registros():
    registros = consultar_registros()
    return [dict(reg) for reg in registros]


@app.get("/registros/{registro_id}", response_model=RegistroResponse, status_code=200)
def buscar_registro(registro_id: int):
    registro = consultar_registro_por_id(registro_id)

    if registro is None:
        # Requisito 5: Código 404 (Not Found)
        raise HTTPException(status_code=404, detail="Registro não encontrado.")

    return dict(registro)


@app.put("/registros/{registro_id}", response_model=RegistroResponse, status_code=200)
def atualizar_registro(registro_id: int, registro: RegistroBase):
    existente = consultar_registro_por_id(registro_id)

    if existente is None:
        raise HTTPException(status_code=404, detail="Registro não encontrado para atualização.")

    try:
        atualizar_registro_existente(registro_id, registro)
        return {**registro.model_dump(), "id": registro_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@app.delete("/registros/{registro_id}", status_code=200)
def deletar_registro(registro_id: int):
    existente = consultar_registro_por_id(registro_id)

    if existente is None:
        raise HTTPException(status_code=404, detail="Registro não encontrado para exclusão.")

    remover_registro(registro_id)

    return {"mensagem": "Registro removido com sucesso."}