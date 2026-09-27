from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import User, Veicolo, Prenotazione
from schemas import *


#Lista tutti i veicoli disponibili
def all_veicoli_disponibili(db:Session) -> list[object]:
    veicoli = db.query(Veicolo).all()

    return [v for v in veicoli if v.status == 'Disponibile']


#Lista tutte le prenotazioni
def all_prenotazioni(db:Session) -> list[object]:
    return db.query(Prenotazione).all()

#Lista tutti gli utenti
def all_users(db:Session) -> list[object]:
    return db.query(User).all()

#Lista tutti i veicoli
def all_veicoli(db:Session) -> list[object]:
    return db.query(Veicolo).all()


#Elimina prenotazione
def delete_prenotazione(db:Session, id:int) -> None:
    prenotazione = db.query(Prenotazione).filter(Prenotazione.id == id).one_or_none()

    if prenotazione:

        prenotazione.veicolo.status = 'Disponibile'
        db.delete(prenotazione)
        db.commit()
        return f'Prenotazione con id: {id} eliminata con successo!'

    else:
        raise HTTPException(status_code=404, detail=f'Prenotazione inesistente')

#Aggiungi prenotazione
def add_prenotazione(db:Session, prenotazione:AggiungiPrenotazione) -> object:

    utente = db.query(User).filter(User.email == prenotazione.user.email).one_or_none()

    if not utente:
        raise HTTPException(status_code=404, detail=f'{prenotazione.user.email} non esistente!')

    veicolo = db.query(Veicolo).filter(Veicolo.targa == prenotazione.veicolo.targa).one_or_none()

    if not veicolo:
        raise HTTPException(status_code=404, detail=f'{prenotazione.veicolo.targa} non esistente!')

    if veicolo.status != 'Prenotato':

        nuova_prenotazione = Prenotazione(user=utente, veicolo=veicolo, 
                                            days=prenotazione.days ,user_first_name=utente.first_name, 
                                            user_last_name=utente.last_name, targa_veicolo=veicolo.targa)

        nuova_prenotazione._total_payment()

        veicolo.status = 'Prenotato'
        db.add(nuova_prenotazione)
        db.commit()
        db.refresh(nuova_prenotazione)
        return nuova_prenotazione

    else:
        raise HTTPException(status_code=404, detail=f'Il veicolo targato : {veicolo.targa} è già prenotato!')



#Elimina veicolo
def elimina_veicolo(db:Session, targa:str) -> None:

    veicolo = get_veicolo_by_targa(db, targa)
    if veicolo:
        db.delete(veicolo)
        db.commit()
        return f'Veicolo con targa :{targa} eliminato con successo!'
    else:
        HTTPException(status_code=404, detail=f'Veicolo con targa :{targa} non esistente')    
 
#Trova veicolo dalla targa
def get_veicolo_by_targa(db:Session, targa) -> object:
    return db.query(Veicolo).filter(Veicolo.targa == targa).one_or_none()

#Aggiunge veicolo
def create_veicolo(db:Session, veicolo:CreateVeicolo) -> object:
    if get_veicolo_by_targa(db, targa= veicolo.targa):
        raise HTTPException(status_code=404, detail=f'Veicolo con targa : {veicolo.targa} già presente nel database')

    new_veicolo = Veicolo(name = veicolo.name, targa = veicolo.targa, 
                          desc= veicolo.desc, cost_per_day = veicolo.cost_per_day)
    db.add(new_veicolo)
    db.commit()
    db.refresh(new_veicolo)
    return new_veicolo

#Crea User
def create_user(db:Session, user_data:CreateUser) -> object:

    if get_user_by_email(db, user_data.email):
        raise HTTPException(status_code=404, detail='User già esistente')

    new_user = User(first_name = user_data.first_name,
                    last_name = user_data.last_name,
                    email = user_data.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


#Trova user by email
def get_user_by_email(db:Session, email:str) -> object:
    return db.query(User).filter(User.email == email).one_or_none()


