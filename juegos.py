import hangman
import reversegam
import tictactoeModificado
import csv
import PySimpleGUI as sg


def contar_agrupar(datos):
    jugadores = {}
    next(datos)
    for dato in datos:
        stats = list(dato[1:])
        stats = [int(a) for a in stats]
        jugadores[dato[0]] = stats
    return jugadores


def leer_csv(ruta):
    archivo = open(ruta, 'r')
    info = contar_agrupar(csv.reader(archivo))
    archivo.close()
    return info

def guardar(ruta, datos):
    header = ('Nombre', 'Ahorcado', 'Ahorcado ganadas', 'Ahorcado perdidas', 'Tateti', 'Tateti ganadas', 'Tateti perdidas', 'Otello', 'Otello ganadas', 'Otello perdidas')
    with open(ruta, 'w', newline = '') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for dato in datos.items():
            writer.writerow([dato[0]] + [a for a in dato[1]])


def actualizar_stats(window, jugador):
    for i in range(len(jugador[1])):
        window['-STATS' + str(i) + '-'].update(jugador[1][i])


def seleccion_juegos(jj, jugador):
    if jj == juegos[0]:
        gano = hangman.main()

        jugador[1][0] += 1
        if gano: jugador[1][1] += 1
        else: jugador[1][2] += 1

    elif jj == juegos[1]:
        gano = tictactoeModificado.main()

        jugador[1][3] += 1
        if gano == 1: jugador[1][4] += 1
        else: jugador[1][5] += 1

    elif jj == juegos[2]:
        gano = reversegam.main()

        jugador[1][6] += 1
        if gano: jugador[1][7] += 1
        else: jugador[1][8] += 1
    return jugador


def seleccion_jugador(window, jugador, datos):
    if jugador[0] in datos:
        jugador[1] = datos[jugador[0]]
    else:
        jugador[1] = [0 for i in range(len(jugador[1]))]
        datos[jugador[0]] = jugador[1]
        window['-LISTA_JUGADORES-'].update(list(datos.keys()))

    window['-STATS_NOM-'].update(jugador[0])


def set_win():
    sg.theme_border_width(0)
    sg.theme_background_color(color='#ffffff')
    sg.theme_text_element_background_color(color='#ffffff')
    sg.theme_text_color(color='#3b3b3b')
    sg.theme_input_background_color(color='#dbdbdb')
    sg.theme_button_color(color=('#3b3b3b', '#c9c9c9'))

    ancho_col1 = 30
    tam_listbox_jugs = (ancho_col1, 12)
    tam_in1 = (ancho_col1, 1)

    ancho_col2 = 30
    tam_listbox_juegos = (ancho_col2, 22)

    ancho_col3 = 40
    tam_in2 = (30, 1)
    graph_size = (500, 500)

    col1 = [
        [sg.T('SELECCIONAR JUGADOR')],
		[sg.In(key = '-J_ID-', size = tam_in1)],
        [sg.T('Lista de jugadores')],
        [sg.Listbox((), size = tam_listbox_jugs, key = '-LISTA_JUGADORES-', enable_events = True)],
        [sg.B('Aceptar'), sg.T('', key = '-AVISO_CONFIR_JUGADOR-', size = (25, 2), text_color = 'Red')],

        [sg.T(' ')],

        [sg.T('ESTADISTICAS DEL JUGADOR', relief = 'groove')],
        [sg.T('Nombre:'), sg.T('Nombre:', key = '-STATS_NOM-')],
        [sg.T('Ahorcado:'), sg.T('Total ', key = '-STATS0-'), sg.T('Ganadas ', key = '-STATS1-', text_color = 'Green'), sg.T('Perdidas ', key = '-STATS2-', text_color = 'Red')],
        [sg.T('Tateti:'), sg.T('Total ', key = '-STATS3-'), sg.T('Ganadas ', key = '-STATS4-', text_color = 'Green'), sg.T('Perdidas ', key = '-STATS5-', text_color = 'Red')],
        [sg.T('Otello:'), sg.T('Total ', key = '-STATS6-'), sg.T('Ganadas ', key = '-STATS7-', text_color = 'Green'), sg.T('Perdidas ', key = '-STATS8-', text_color = 'Red')]
    ]

    col2 = [
        [sg.T('ELIJA EL JUEGO')],
        [sg.Listbox((), size = tam_listbox_juegos, key = '-LISTA_JUEGOS-', enable_events = True)],
        [sg.B('Jugar'), sg.T('', key = '-AVISO_CONFIR_JUEGO-', size = (25, 2), text_color = 'Red')],
    ]

    layout = [
        [sg.Column(col1), sg.Column(col2)]
    ]

    window = sg.Window('Juegos', layout, font = ('OpenType', 12))
    window.Finalize()
    return window


def ejecutar_win(window, datos, ruta):
    jugador = ['', [0 for i in range(9)]]
    window['-LISTA_JUGADORES-'].update([j for j in datos.keys()])
    window['-LISTA_JUEGOS-'].update([j for j in juegos])

    while True:
        event, values = window.read()
        if event is None:
            guardar(ruta, datos)
            break

        if event == 'Aceptar':
            aviso = window['-AVISO_CONFIR_JUGADOR-']
            jugador[0] = values['-J_ID-']
            if values['-J_ID-'] == '':
                aviso.update('Nombre no valido')
            elif jugador[0] == '':
                aviso.update('Para confirmar su jugador debe tocar "Aceptar"')
            else:
                aviso.update('')
                seleccion_jugador(window, jugador, datos)
                actualizar_stats(window, jugador)

        if values['-LISTA_JUGADORES-'] != [] and event == '-LISTA_JUGADORES-':
            window['-J_ID-'].update(values['-LISTA_JUGADORES-'][0])

        if event == 'Jugar':
            aviso = window['-AVISO_CONFIR_JUEGO-']
            if jugador[0] == '':
                aviso.update('Para confirmar su jugador debe tocar "Aceptar"')
            elif values['-LISTA_JUEGOS-'] == []:
                aviso.update('Debe seleccionar un juego de la lista para poder jugar')
            else:
                aviso.update('')
                jj = values['-LISTA_JUEGOS-'][0]
                jugador = seleccion_juegos(jj, jugador)
                actualizar_stats(window, jugador)
                datos[jugador[0]] = jugador[1]
    window.close()


juegos = ['Ahorcado', 'Tateti', 'Otello']
ruta = 'Jugadores.csv'
datos = leer_csv(ruta)
print(datos)
window = set_win()
ejecutar_win(window, datos, ruta)
