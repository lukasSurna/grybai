import PySimpleGUI as sg
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import Grybai, Vietoves, Regionai


db_engine = create_engine("sqlite:///grybai.db")
Session = sessionmaker(db_engine)
session = Session()


def main_window():  # Einaras
    pass


def add_region(session):  # Deivida
    layout = [
        [
            sg.Text("Įveskite regiono pavadinimą: ", size=20),
            sg.InputText(key="-REGIONO-PAVADINIMAS-"),
        ],
        [sg.Button("Pridėti", key="-PRIDETI-")],
    ]
    window = sg.Window("Naujo regiono įvedimas", layout, finalize=True)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if event == "-PRIDETI-":
            regiono_pavadinimas = values["-REGIONO-PAVADINIMAS-"]
            if regiono_pavadinimas:
                naujas_regionas = Regionai(regionas=regiono_pavadinimas)
                session.add(naujas_regionas)
                session.commit()
                sg.popup(f"Regionas: {regiono_pavadinimas} sėkmingai pridėtas")
                break
            else:
                sg.popup("Regiono pavadinimas negali būti tuščias")
    window.close()


# Lukas
def add_location(session):
    # pasiimti regionus is db
    regions = session.query(Regionai).all()
    # regionu dropDown
    regionu_pavadinimai = [regionas.regionas for regionas in regions]

    layout = [
        [
            sg.Text("Iveskite vietoves pavadinima: ", size=20),
            sg.InputText(key="-PAVADINIMAS-"),
        ],
        [
            sg.Text("Pasirinkite regiona: ", size=20),
            sg.Combo(regionu_pavadinimai, key="-REGIONAI-"),
        ],
        [sg.Button("Prideti", key="-PRIDETI-")],
    ]
    window = sg.Window("Naujos Vietoves Ivedimas", layout, finalize=True)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if event == "-PRIDETI-":
            vietoves_pavadinimas = values["-PAVADINIMAS-"]
            pasirinktas_regionas = values["-REGIONAI-"]

            # pasiimti pasirinkta regiona (dropdown)
            pasirinktas_regionas = next(
                (
                    regionas
                    for regionas in regions
                    if regionas.regionas == pasirinktas_regionas
                ),
                None,
            )

        if vietoves_pavadinimas:
            nauja_vietove = Vietoves(vietoves_pavadinimas=vietoves_pavadinimas)
            session.add(nauja_vietove)
            session.commit()
            sg.popup(f"Vietove: {vietoves_pavadinimas} Sekmingai prideta")
            break
        else:
            sg.popup("Visi laukai turi buti uzpildyti")


def remove_location(session):
    vietoves = session.query(Vietoves).all()
    # vietoves dropDown
    vietove = [vietove.vietoves for vietove in vietoves]

    layout = [
        [
            sg.Text("Pasirinkite vietove: ", size=20),
            sg.Combo(vietove, key="-VIETOVES-", size=(10, 10)),
        ],
        [
            sg.Listbox(
                values=vietoves,
                size=(15, 8),
                key="-VISOS-VIETOVES-",
                enable_events=True,
            )
        ],
        [sg.Button("Istrinti", key="-ISTRINTI-")],
    ]
    window = sg.Window("Vietoves pasalinimas", layout, finalize=True)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if event == "-ISTRINTI-":
            pasirinkta_vietove = values["-VIETOVES-"]
            if pasirinkta_vietove:
                pasirinkta_vietove_pavadinimas = pasirinkta_vietove[0]
                trinti_vietove = next(
                    (
                        vietove
                        for vietove in vietoves
                        if vietove.vietoves == pasirinkta_vietove_pavadinimas
                    ),
                    None,
                )
                session.delete(trinti_vietove)
                session.comit()
                sg.popup(f"Vietove {pasirinkta_vietove_pavadinimas} sekmingai istrinta")
        else:
            sg.popup("Pasirinkite vietove, kuria norite istrinti")


def add_mushroom():  # Vytautas
    pass


if __name__ == "__main__":
    session = Session()
    add_location(session)
    add_region(session)
    remove_location(session)
