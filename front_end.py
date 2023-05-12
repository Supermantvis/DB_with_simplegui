import PySimpleGUI as sg
from back_end import Darbuotojas
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

engine = create_engine('sqlite:///darbuotojai_uzd.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

class Darbuotojai_gui:
    def __init__(self):
        self.layout = [
            [sg.Button("Perziureti darbuotojus"),
             sg.Button("Prideti nauja darbuotoja"),
             sg.Button("Pakeisti darbuotojo info"),
             sg.Button("Istrinti darbuotoja"),
             sg.Button("Uzdaryti programa")]
        ]
        self.window = sg.Window("Darbuotojai", layout=self.layout)

    def run(self):
        while True:
            event, values = self.window.read()
            if event == sg.WINDOW_CLOSED or event == 'Uzdaryti programa':
                break


            elif event == 'Perziureti darbuotojus':
                darbuotoju_sarasas = session.query(Darbuotojas).all()
                data = [
                    [item.id, item.vardas, item.pavarde, item.gimimo_data, item.pareigos, item.atlyginimas, item.dirba_nuo]
                    for item in darbuotoju_sarasas
                ]
                headers = ['ID', 'Vardas', 'Pavarde', 'Gimimo data', 'Pareigos', 'Atlyginimas', 'Nuo kada dirba']
                table = sg.Table(values=data, headings=headers, auto_size_columns=True, key="-TABLE-")
                layout = [[table]]
                window = sg.Window("Perziureti darbuotojus", layout=layout)
                window.read()
                window.close()


            elif event == 'Prideti nauja darbuotoja':
                # Create a new window with input fields
                new_employee_layout = [
                    [sg.Text('Vardas'), sg.Input(key='-VARDAS-')],
                    [sg.Text('Pavarde'), sg.Input(key='-PAVARDE-')],
                    [sg.Text('Gimimo data'), sg.Input(key='-GIMIMO_DATA-')],
                    [sg.Text('Pareigos'), sg.Input(key='-PAREIGOS-')],
                    [sg.Text('Atlyginimas'), sg.Input(key='-ATLYGINIMAS-')],
                    [sg.Button('Prideti', key='-ADD_EMPLOYEE-')]
                ]
                new_employee_window = sg.Window('Prideti nauja darbuotoja', layout=new_employee_layout)

                # Wait for user input
                while True:
                    new_event, new_values = new_employee_window.read()
                    if new_event == sg.WINDOW_CLOSED:
                        break
                    elif new_event == '-ADD_EMPLOYEE-':
                        # Create a new Darbuotojas object and add it to the database
                        new_employee = Darbuotojas(
                            vardas=new_values['-VARDAS-'],
                            pavarde=new_values['-PAVARDE-'],
                            gimimo_data=datetime.strptime(new_values['-GIMIMO_DATA-'], '%Y-%m-%d'),
                            pareigos=new_values['-PAREIGOS-'],
                            atlyginimas=new_values['-ATLYGINIMAS-']
                        )
                        session.add(new_employee)
                        session.commit()
                        sg.popup('Darbuotojas pridetas sėkmingai')
                        break
                new_employee_window.close()


            elif event == 'Pakeisti darbuotojo info':
                # Create a new window with input fields
                update_employee_layout = [
                    [sg.Text('ID'), sg.Input(key='-EMPLOYEE_ID-')],
                    [sg.Text('Keisti Varda'), sg.Input(key='-NEW_F_NAME-')],
                    [sg.Text('Keisti pavarde'), sg.Input(key='-NEW_L_NAME-')],
                    [sg.Text('Keisti gimimo data'), sg.Input(key='-NEW_BIRTHED_DATE-')],
                    [sg.Text('Keisti pareigas'), sg.Input(key='-NEW_POSITION-')],
                    [sg.Text('Keisti atlyginima'), sg.Input(key='-NEW_SALARY-')],

                    [sg.Button('Pakeisti', key='-UPDATE_EMPLOYEE-')]
                ]
                update_employee_window = sg.Window('Pakeisti darbuotojo info', layout=update_employee_layout)

                # Wait for user input
                while True:
                    update_event, update_values = update_employee_window.read()
                    if update_event == sg.WINDOW_CLOSED:
                        break
                    elif update_event == '-UPDATE_EMPLOYEE-':
                        # Get the employee with the given ID and update their salary
                        employee_id = update_values['-EMPLOYEE_ID-']
                        new_f_name = update_values['-NEW_F_NAME-']
                        new_l_name = update_values['-NEW_L_NAME-']
                        new_birth_date=datetime.strptime(update_values['-NEW_BIRTHED_DATE-'], '%Y-%m-%d')
                        new_position = update_values['-NEW_POSITION-']
                        new_salary = update_values['-NEW_SALARY-']
                        employee = session.query(Darbuotojas).get(employee_id)
                        if employee is not None:
                            if update_values['-NEW_F_NAME-'] != '':
                                employee.vardas = update_values['-NEW_F_NAME-']
                            if update_values['-NEW_L_NAME-'] != '':
                                employee.pavarde = update_values['-NEW_L_NAME-']
                            if update_values['-NEW_BIRTHED_DATE-'] != '':
                                employee.gimimo_data = datetime.strptime(update_values['-NEW_BIRTHED_DATE-'], '%Y-%m-%d')
                            if update_values['-NEW_POSITION-'] != '':
                                employee.pareigos = update_values['-NEW_POSITION-']
                            if update_values['-NEW_SALARY-'] != '':
                                employee.atlyginimas = update_values['-NEW_SALARY-']
                            session.commit()
                            sg.popup('Darbuotojo informacija pakeista sėkmingai')
                        else:
                            sg.popup('Darbuotojas su tokiu ID nerastas')
                        break
                update_employee_window.close()

                pass
            else:
                pass

        self.window.close()

darbuotojeliai = Darbuotojai_gui()
darbuotojeliai.run()