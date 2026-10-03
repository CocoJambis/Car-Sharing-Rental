from pydantic import BaseModel, EmailStr, ConfigDict


class CreateUser(BaseModel):
    first_name:str
    last_name:str
    email:EmailStr

class UserResponse(BaseModel):
    id:int
    first_name:str
    last_name:str
    email:EmailStr

    model_config = ConfigDict(from_attributes= True)

class UserPrenotazione(BaseModel):
    email:EmailStr


class CreateVeicolo(BaseModel):
    name:str
    targa:str
    desc:str
    cost_per_day:float

class VeicoloResponse(BaseModel):
    id:int
    name:str
    targa:str
    desc:str
    status:str
    cost_per_day:float

    model_config = ConfigDict(from_attributes= True)



class VeicoloPrenotazione(BaseModel):
    targa:str


class VeicoloEdit(BaseModel):
    name:str
    targa:str
    desc:str
    cost_per_day:float


class AggiungiPrenotazione(BaseModel):
    user:UserPrenotazione
    veicolo:VeicoloPrenotazione
    days:int

    model_config = ConfigDict(from_attributes= True)


class PrenotazioneResponse(BaseModel):
    id:int
    user: UserResponse
    veicolo: VeicoloResponse
    prezzo_finale:float

    model_config = ConfigDict(from_attributes= True)
