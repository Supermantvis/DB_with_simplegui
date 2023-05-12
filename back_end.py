# -- https://github.com/DonatasNoreika/python1lygis/wiki/Duomen%C5%B3-baz%C4%97s-2
# -- https://github.com/DonatasNoreika/Python-pamokos/wiki/ORM-(sqlalchemy)-II-dalis

# -- 1 užduotis
# -- Sukurti programą, kuri:

# -- Leistų įvesti darbuotojus: vardą, pavardę, gimimo datą, pareigas, atlyginimą, nuo kada dirba (data būtų nustatoma automatiškai, pagal dabartinę datą).
# -- Duomenys būtų saugomi duomenų bazėję, panaudojant SQLAlchemy ORM (be SQL užklausų)
# -- Vartotojas galėtų peržiūrėti, įrašyti, atnaujinti ir ištrinti darbuotojus.


# -- 2 užduotis
# -- Perdaryti programą 1 užduotyje, kad ji:

# -- Turėtų grafinę sąsają (su ikona ir pavadinimu). Sukurti per Tkinter
# -- Leistų įvesti asmenis į duomenų bazę (jų vardą, pavardę, amžių, ...)
# -- Parodytų visų į duomenų bazę įvestų asmenų sąrašą
# -- Leistų ištrinti pasirinktą asmenį iš duomenų bazės
# -- Leistų paredaguoti įvesto asmens duomenis ir įrašyti atnaujinimus į duomenų bazę Sukurti paleidžiamąjį programos failą (exe, su ikona)

from typing import Any
from sqlalchemy import create_engine, Integer, String, Float, DateTime, Date
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column
from datetime import datetime
import os
import PySimpleGUI as sg

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

class Base(DeclarativeBase):
    pass

class Darbuotojas(Base):
    __tablename__ = "darbuotojai"
    id = mapped_column(Integer, primary_key=True)
    vardas = mapped_column(String(50), nullable=False)
    pavarde = mapped_column(String(50), nullable=False)
    gimimo_data = mapped_column(Date, nullable=False)
    pareigos = mapped_column(String(50), nullable=False)
    atlyginimas = mapped_column(Float(2), nullable=False)
    dirba_nuo = mapped_column(DateTime, default=datetime.now().date())

    def __init__(self, **kw: Any):
        # super().__init__(**kw)
        for key, value in kw.items():
            setattr(self, key, value)

    def __repr__(self) -> str:
        return f"({self.id}, {self.vardas}, {self.pavarde}, {self.gimimo_data}, {self.pareigos}, {self.atlyginimas}, {self.dirba_nuo})"


def spausdinti(session):
    clear()
    darbuotojai = session.query(Darbuotojas).all()
    print("-------------------")
    for darbuotojas in darbuotojai:
        print(darbuotojas)
    print("-------------------")
    return darbuotojai

if __name__ == "__main__":
    engine = create_engine('sqlite:///darbuotojai_uzd.db', echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    Base.metadata.create_all(engine)  # CREATE TABLE

    while True:
        pasirinkimas = input("""Pasirinkite veiksmą: 
    1 - Atvaizduoti darbuotojus
    2 - Itraukti darbuotoja i DB
    3 - Pakeisti darbuotojo info
    4 - Ištrinti darbuotoja
    0 - Išeiti
    >:""")

        try:
            pasirinkimas = int(pasirinkimas)
        except:
            pass

        if pasirinkimas == 1:
            spausdinti(session)

        elif pasirinkimas == 2:
            vardas = input("Įveskite darbuotojo varda: ")
            pavarde = input("Įveskite darbuotojo pavarde: ")
            gimimo_data = datetime.strptime(input("Įveskite darbuotojo gimimo data: "), '%Y-%m-%d')
            gimimo_data = gimimo_data.date()
            pareigos = input("Įveskite darbuotojo pareigas: ")
            atlyginimas = float(input("Įveskite darbuotojo atlyginima: "))
            darbuotojas = Darbuotojas(vardas=vardas, pavarde=pavarde, gimimo_data=gimimo_data, pareigos=pareigos, atlyginimas=atlyginimas)
            session.add(darbuotojas)
            session.commit()

        elif pasirinkimas == 3:
            projektai = spausdinti(session)
            try:
                keiciamas_id = int(input("Pasirinkite norimo pakeisti darbuotojo ID: "))
                keiciamas_darbuotojas = session.get(Darbuotojas, keiciamas_id)
            except Exception as e:
                print(f"Klaida: {e}")
            else:
                pakeitimas = int(input("""
            ===[ Darbuotoju info keitimas ]===
            1 - Vardas
            2 - Pavarde
            3 - Gimimo data
            4 - Pareigos
            5 - Atlyginimas
            ===================================
            Pasirinkite: """))
                if pakeitimas == 1:
                    keiciamas_darbuotojas.vardas = input("Įveskite darbuotojo varda: ")
                if pakeitimas == 2:
                    keiciamas_darbuotojas.pavarde = input("Įveskite darbuotojo pavarde: ")
                if pakeitimas == 3:
                    keiciamas_darbuotojas.gimimo_data = datetime.strptime(input("Įveskite darbuotojo gimimo data: "), '%Y-%m-%d')
                if pakeitimas == 4:
                    keiciamas_darbuotojas.pareigos = input("Įveskite darbuotojo pareigas: ")
                if pakeitimas == 5:
                    keiciamas_darbuotojas.atlyginimas = input("Įveskite darbuotojo atlyginima: ")
                session.commit()

        elif pasirinkimas == 4:
            darbuotojai = spausdinti(session)
            trinamas_id = int(input("Pasirinkite norimo ištrinti darbuotojo ID: "))
            try:
                trinamas_darbuotojas = session.get(Darbuotojas, trinamas_id)
                session.delete(trinamas_darbuotojas)
                session.commit()
            except Exception as e:
                print(f"Klaida: {e}")

        elif pasirinkimas == 0:
            print("Ačiū už tvarkingą uždarymą")
            break

        else:
            print("Klaida: Neteisingas pasirinkimas")
