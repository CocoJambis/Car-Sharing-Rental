import pytest
from fastapi import HTTPException
from App.crud import *
from App.schemas import CreateUser, CreateVeicolo, AggiungiPrenotazione



def test_create_user(db_session):
    user_data = CreateUser(first_name="Mario", last_name="Rossi", email="mario.rossi@gmail.com")

    nuovo_utente = create_user(db=db_session, user_data=user_data)

    assert nuovo_utente.id is not None
    assert nuovo_utente.email == "mario.rossi@gmail.com"

    utente_db = get_user_by_email(db=db_session, email='mario.rossi@gmail.com')

    assert utente_db is not None


def test_create_user_già_esistente(db_session):

    user_data = CreateUser(first_name="Mario", last_name = "Rossi", email = "mario.rossi@gmail.com")

    create_user(db = db_session, user_data = user_data)


    with pytest.raises(HTTPException) as exc_info:
        create_user(db = db_session, user_data = user_data)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == 'User già esistente'



def test_add_prenotazione(db_session):
    user_data = CreateUser(first_name="Mario", last_name = "Rossi", email = "mario.rossi@gmail.com")
    utente = create_user(db = db_session, user_data = user_data)

    veicolo_data = CreateVeicolo(name = 'Scirocco', targa = 'DT293RG', desc = '160cv benzina', cost_per_day= 50.0)
    veicolo = create_veicolo(db = db_session, veicolo=veicolo_data)

    prenotazione_in = AggiungiPrenotazione(user = UserPrenotazione(email="mario.rossi@gmail.com"), 
                                           veicolo = VeicoloPrenotazione(targa = "DT293RG"), days = 5)

    prenotazione = add_prenotazione(db = db_session, prenotazione = prenotazione_in)


    assert prenotazione.id is not None
    assert prenotazione.targa_veicolo == "DT293RG"
    assert prenotazione.user_first_name == "Mario"
    assert prenotazione.user_last_name == "Rossi"
    assert veicolo.status == "Prenotato"


def test_prenotazione_utente_inesistente(db_session):
    veicolo_payload = CreateVeicolo(name= "Scirocco", targa = "DT293RG", desc = "160cv benzina", cost_per_day = 50.0)
    veicolo = create_veicolo(db_session, veicolo_payload)
    veicolo.status = "Disponibile"

    db_session.commit()

    prenotazione_in = AggiungiPrenotazione(user = UserPrenotazione(email= "non.esiste@gmail.com"), veicolo = VeicoloPrenotazione(targa = "DT293RG"), days = 5)

    with pytest.raises(HTTPException) as exc_info:
        add_prenotazione(db_session, prenotazione_in)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "non.esiste@gmail.com non esistente!"


def test_prenotazione_veicolo_inesistente(db_session):
    user_in = CreateUser(first_name="Mario", last_name="Rossi", email = "mario.rossi@gmail.com")
    user = create_user(db_session, user_in)

    prenotazione_in = AggiungiPrenotazione(user = UserPrenotazione(email = "mario.rossi@gmail.com"), veicolo = VeicoloPrenotazione(targa = "asv123cv"), days = 3)


    with pytest.raises(HTTPException) as exc_info:
        add_prenotazione(db_session, prenotazione_in)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "asv123cv non esistente!"


def test_prenotazione_veicolo_già_prenotato(db_session):
    user_in = CreateUser(first_name="Mario", last_name="Rossi", email = "mario.rossi@gmail.com")
    user = create_user(db_session, user_in)

    veicolo_in = CreateVeicolo(name = "Scirocco", targa = "DT293RG", desc = "160cv benzina", cost_per_day = 50.0)
    veicolo = create_veicolo(db_session, veicolo_in)
    veicolo.status = "Prenotato"
    db_session.commit()

    prenotatione_in = AggiungiPrenotazione(user = UserPrenotazione(email = "mario.rossi@gmail.com"), veicolo= VeicoloPrenotazione(targa = "DT293RG"), days = 3)

    with pytest.raises(HTTPException) as exc_info:
        add_prenotazione(db_session, prenotatione_in)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Il veicolo targato : DT293RG è già prenotato!"


def test_elimina_veicolo(db_session):
    veicolo_in = CreateVeicolo(name = "Scirocco", targa = "DT293RG", desc = "asd", cost_per_day = 50.0)
    veicolo = create_veicolo(db_session, veicolo_in)

    messaggio_ritorno = elimina_veicolo(db_session, veicolo.targa)
    db_session.commit()

    assert messaggio_ritorno == "Veicolo con targa :DT293RG eliminato con successo!"

    veicolo_cancellato = get_veicolo_by_targa(db_session, targa = veicolo.targa)

    assert veicolo_cancellato is None

def test_elimina_veicolo_inesistente(db_session):


    with pytest.raises(HTTPException) as exc_info:
        elimina_veicolo(db_session, "DT293RG")

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Veicolo con targa :DT293RG non esistente"


def test_aggiungi_veicolo(db_session):
    veicolo_in = CreateVeicolo(name = "Scirocco", targa = "DT293RG", desc = "160cv benzina", cost_per_day = 50.0)
    veicolo = create_veicolo(db_session, veicolo_in)

    assert veicolo.name == "Scirocco"
    assert veicolo is not None
    assert veicolo.targa == "DT293RG"


def test_aggiungi_veicolo_già_esistente(db_session):
    veicolo_in = CreateVeicolo(name = "Scirocco", targa = "DT293RG", desc = "160cv benzina", cost_per_day = 50.0)
    veicolo = create_veicolo(db_session, veicolo_in)

    with pytest.raises(HTTPException) as exc_info:
        create_veicolo(db_session, veicolo_in)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == f"Veicolo con targa : {veicolo.targa} già presente nel database"


def test_elimina_prenotazione(db_session):
    user_in = CreateUser(first_name = "Mario", last_name = "Rossi", email = "mario.rossi@gmail.com")
    user = create_user(db_session, user_in)

    veicolo_in = CreateVeicolo(name = "Scirocco", targa = "DT293RG", desc = "160cv benzina", cost_per_day = 50.0)
    veicolo = create_veicolo(db_session, veicolo_in)


    prenotazione_in = AggiungiPrenotazione(user = UserPrenotazione(email = "mario.rossi@gmail.com"), veicolo = VeicoloPrenotazione(targa = "DT293RG"), days = 3)
    prenotazione = add_prenotazione(db_session, prenotazione_in)

    assert prenotazione is not None
    assert prenotazione.id == 1

    messaggio = delete_prenotazione(db_session, prenotazione.id)

    assert messaggio == f"Prenotazione con id: {prenotazione.id} eliminata con successo!"


def test_elimina_prenotazione_inesistente(db_session):

    with pytest.raises(HTTPException) as exc_info:
        delete_prenotazione(db_session, 1)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Prenotazione inesistente"
    
def test_elimina_user(db_session):

    user_in = CreateUser(first_name = "Mario", last_name = "Rossi", email= "mario.rossi@gmail.com")
    user = create_user(db_session, user_in)

    assert user.id is not None
    assert user.first_name == "Mario"
    assert user.email == "mario.rossi@gmail.com"

    messaggio = delete_utente_by_email(db_session, user.email)

    assert messaggio == f'User con email : {user.email} eliminato con successo!'

    user_eliminato = get_user_by_email(db_session, user.email)

    assert user_eliminato is None


def test_elimina_utente_inesistente(db_session):

    with pytest.raises(HTTPException) as exc_info:
        delete_utente_by_email(db_session, "mario.rossi@gmail.com")

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "email : mario.rossi@gmail.com non esistente!"


def test_edit_veicolo(db_session):
    veicolo_in = CreateVeicolo(name = "Scirocco", targa = "DT293RG", desc = "160cv benzina", cost_per_day = 50.0)
    veicolo = create_veicolo(db_session, veicolo_in)

    edit_veicolo = VeicoloEdit(name= "Edit", targa = "ciao", desc = "150cv benzina", cost_per_day=20.0)

    edit_veicolo_by_targa(db_session, targa= "DT293RG", veicolo_edit = edit_veicolo)

    assert veicolo.name == "Edit"
    assert veicolo.targa == "ciao"
    assert veicolo.desc == "150cv benzina"


def test_edit_veicolo_inesistente(db_session):


    with pytest.raises(HTTPException) as exc_info:
        edit_veicolo_by_targa(db_session, targa = "DT293RA", veicolo_edit= None)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == f"Veicolo con targa : DT293RA inesistente"

