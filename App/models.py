from typing import List
from sqlalchemy import Integer, String, ForeignKey, Float
from sqlalchemy.orm import declarative_base, relationship, mapped_column, Mapped
from App.db import engine


Base = declarative_base()

class User(Base):

    __tablename__ = 'users'

    id : Mapped[int] = mapped_column(primary_key=True)
    first_name : Mapped[str] = mapped_column(String, nullable=False)
    last_name : Mapped[str] = mapped_column(String, nullable=False)
    email : Mapped[str] = mapped_column(String, unique=True, nullable=False)


    prenotazioni : Mapped[List["Prenotazione"]] = relationship('Prenotazione', back_populates='user')


class Veicolo(Base):

    __tablename__ = 'veicoli'

    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(String, nullable=False)
    targa : Mapped[str] = mapped_column(String, nullable=False, unique=True)
    desc : Mapped[str] = mapped_column(String, nullable=False)
    status : Mapped[str] = mapped_column(String, default='Disponibile', server_default='Disponibile')
    cost_per_day : Mapped[float] = mapped_column(Float, nullable=False)

    prenotazioni : Mapped[List['Prenotazione']] = relationship('Prenotazione', back_populates='veicolo')


class Prenotazione(Base):

    __tablename__ = 'prenotazioni'

    id : Mapped[int] = mapped_column(primary_key=True)
    user_id : Mapped[int] = mapped_column(ForeignKey('users.id'))
    veicolo_id : Mapped[int] = mapped_column(ForeignKey('veicoli.id'))
    days : Mapped[int] = mapped_column(Integer, nullable=False)

    user_first_name : Mapped[str] = mapped_column(String, nullable=False)
    user_last_name : Mapped[str] = mapped_column(String, nullable=False)
    targa_veicolo: Mapped[str] = mapped_column(String, nullable=False)
    prezzo_finale : Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

    user : Mapped['User'] = relationship('User', back_populates='prenotazioni')
    veicolo : Mapped['Veicolo'] = relationship('Veicolo', back_populates='prenotazioni')


    def _total_payment(self) -> float:
        cost = self.veicolo.cost_per_day
        self.prezzo_finale = self.days * cost
        return self.prezzo_finale


if __name__ == "__main__":
    Base.metadata.create_all(engine)