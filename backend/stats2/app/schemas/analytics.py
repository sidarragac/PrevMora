from pydantic import BaseModel


class MesSeleccion(BaseModel):
    Enero: bool = False
    Febrero: bool = False
    Marzo: bool = False
    Abril: bool = False
    Mayo: bool = False
    Junio: bool = False
    Julio: bool = False
    Agosto: bool = False
    Septiembre: bool = False
    Octubre: bool = False
    Noviembre: bool = False
    Diciembre: bool = False


