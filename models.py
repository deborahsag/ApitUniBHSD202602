from pydantic import BaseModel


# ==========================================
# 2. CAMADA DE MODELOS (Pydantic)
# ==========================================
class RegistroBase(BaseModel):
    titulo: str
    descricao: str | None = None
    ativo: bool = True


class RegistroResponse(RegistroBase):
    id: int
