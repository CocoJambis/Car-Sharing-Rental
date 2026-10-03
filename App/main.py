import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from App.schemas import *
import App.crud as crud
from App.db import get_db
from App.models import *
from sqlalchemy.orm import Session


app = FastAPI()


@app.get('/')
def home():
    return 'Welcome!'

#Aggiungi utente al database
@app.post('/user/', response_model=UserResponse)
def create_user(user:CreateUser, db: Session = Depends(get_db)):

    return crud.create_user(db, user_data=user)

#Aggiungi veicolo
@app.post('/veicolo/', response_model=VeicoloResponse)
def create_veicolo(veicolo:CreateVeicolo, db:Session = Depends(get_db)):

    return crud.create_veicolo(db, veicolo = veicolo)


#Elimina veicolo
@app.delete('/veicolo/{targa}')
def delete_veicolo(targa, db:Session = Depends(get_db)):

  return crud.elimina_veicolo(db, targa = targa)


#Aggiungi Prenotazione
@app.post('/prenotazione/', response_model=PrenotazioneResponse)
def aggiungi_prenotazione(payload:AggiungiPrenotazione, db:Session = Depends(get_db)):

    return crud.add_prenotazione(db, payload)


#Elimina prenotazione
@app.delete('/prenotazione/{id}')
def delete_prenotazione(id:int, db:Session = Depends(get_db)):

   return crud.delete_prenotazione(db, id = id)

#Lista tutti i veicoli
@app.get('/veicoli/', response_model=list[VeicoloResponse])
def all_veicoli(db:Session = Depends(get_db)):

    return crud.all_veicoli(db)

#Lista tutti gli utenti
@app.get('/users/', response_model=list[UserResponse])
def all_users(db:Session = Depends(get_db)):
    return crud.all_users(db)


#Lista tutte le prenotazioni
@app.get('/prenotazioni/', response_model=list[PrenotazioneResponse])
def all_prenotazioni(db:Session = Depends(get_db)):

    return crud.all_prenotazioni(db)

#Tutti i veicoli disponibili
@app.get('/veicoli/disp', response_model=list[VeicoloResponse])
def all_veicoli_disp(db:Session = Depends(get_db)):

    return crud.all_veicoli_disponibili(db)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=5000)


