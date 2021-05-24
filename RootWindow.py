import PySimpleGUI as sg
import re

layout = [
    [
        sg.T("First Sequence", size=(13, 1)),
        sg.In(size=(35, 1), enable_events=True, key="-SEQ1-"),
    ],
    [
        sg.T("Second Sequence", size=(13, 1)),
        sg.In(size=(35, 1), enable_events=True, key="-SEQ2-"),
    ],
    [
        sg.T("", size=(13, 1)),
        sg.T("", key="-sequence_notice-", size=(30, 1), text_color="red"),
    ],
    [
        sg.Radio("Dot Matrix", "Algorithm", key="-algorithm_DM-"),
        sg.T("                         "),
        sg.Button(
            button_text="Plot",
            size=(10, 1),
        ),
    ],
    [
        sg.Radio("Needleman-Wunch", "Algorithm", key="-algorithm_NW-"),
        sg.T("    "),
        sg.T("", key="-algorithm_notice-", size=(25, 1), text_color="red"),
    ],
    [sg.Radio("Smith-Waterman", "Algorithm", key="-algorithm_SW-")],
]


root = sg.Window("Assignment 2", layout)
sequence_pattern = re.compile("^((A|T|G|C)+)$")


def run():
    while True:
        event, values = root.read()
        error = False
        choice = ""
        if event == sg.WIN_CLOSED:
            break
        elif event == "Plot":
            root.Element("-algorithm_notice-").update("")
            root.Element("-sequence_notice-").update("")

            sequence1 = values["-SEQ1-"]
            sequence2 = values["-SEQ2-"]

            if not (
                sequence_pattern.search(sequence1)
                and sequence_pattern.search(sequence2)
            ):
                root.Element("-sequence_notice-").update(
                    "Sequence can only contain A, T, C or G"
                )
                error = True

            if values["-algorithm_DM-"]:
                choice = "Dot Matrix"
            elif values["-algorithm_NW-"]:
                choice = "Needleman-Wunch"
            elif values["-algorithm_SW-"]:
                choice = "Smith-Waterman"
            else:
                root.Element("-algorithm_notice-").update("Please choose one algorithm")
                error = True
            if not error:
                print(choice + "," + sequence1 + "," + sequence2)
    root.close()


def ShowPlotWindow(choice, seq1, seq2):
    print()
