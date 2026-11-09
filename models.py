from pydantic import BaseModel


class RegistroBase(BaseModel):
    titulo: str
    descricao: str | None = None
    ativo: bool = True


class RegistroResponse(RegistroBase):
    id: int
