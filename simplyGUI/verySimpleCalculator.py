import PySimpleGUI as sg

"""
    A very simple calculator.
    To practise the simpleGUI module and the basic application design for a calculator.
"""

sg.theme('BluePurple')

numeric_keys = {
    '-ONE-': '1', '-TWO-': '2', '-THREE-': '3', '-FOUR-': '4', '-FIVE-': '5',
    '-SIX-': '6', '-SEVEN-': '7', '-EIGHT-': '8', '-NINE-': '9', '-ZERO-': '0',
    '-DOT-': '.'
}

operator_keys = {
    '-PLUS-': '+', '-MINUS-': '-', '-MULTI-': '*', '-DIV-': '/', '-EQ-': '=',
}
layout = [[sg.InputText(size=(15, 2), key='-OUTPUT-')],
          [sg.Button('1', key='-ONE-'), sg.Button('2', key='-TWO-'), sg.Button('3', key='-THREE-'), sg.Button('x', key='-MULTI-')],
          [sg.Button('4', key='-FOUR-'), sg.Button('5', key='-FIVE-'), sg.Button('6', key='-SIX-'), sg.Button('/', key='-DIV-')],
          [sg.Button('7', key='-SEVEN-'), sg.Button('8', key='-EIGHT-'), sg.Button('9', key='-NINE-'), sg.Button('-', key='-MINUS-')],
          [sg.Button('.', key='-DOT-'), sg.Button('0', key='-ZERO-'), sg.Button('+', key='-PLUS-'), sg.Button('=', key='-EQ-')]
          ]

window = sg.Window('Calculator', layout)




def verySimpleCalc(default=None):

    # initiate the input and output string with empty.
    input_str = ''
    result_str = ''

   # starting the main windows and waiting for input events.
    while True:  # Event Loop
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event in numeric_keys.keys():
            # Update the "output" text element to be the value of "input" element
            input_str += numeric_keys[event]
            window['-OUTPUT-'].update(input_str)
        elif event in operator_keys.keys():
            if event != '-EQ-':
                input_str += operator_keys[event]
                window['-OUTPUT-'].update(input_str)
            elif event == '-EQ-':
                try:
                    result = eval(input_str)
                    result_str = str(result)
                except :
                    result_str = 'Error'


                window['-OUTPUT-'].update(result_str)
                input_str = ''
                result_str = ''

    window.close()
