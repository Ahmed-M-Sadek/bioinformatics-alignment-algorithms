import PySimpleGUI as sg


class Node:
    def __init__(self, size, key):
        super().__init__()
        self.score = 0
        self.children = []
        self.size = size
        self.image = sg.Image(filename="white.png", size=self.size, k=key)

    def paths(self):
        if not self.children:
            return [[self.score]]
        paths = []
        for child in self.children:
            for path in child.paths():
                paths.append([self.score] + path)
        return paths


class Plot:
    def __init__(self, seq1, seq2, choice):
        super().__init__()
        self.no_of_cols = len(seq1)
        self.no_of_rows = len(seq2)
        self.choice = choice
        grid = [
            [
                Node((500 / self.no_of_cols, 500 / self.no_of_rows), (i, j)).image
                for j in range(self.no_of_cols)
            ]
            for i in range(self.no_of_rows)
        ]
        self.layout = [
            [
                sg.Button(
                    "Start",
                    "center",
                    size=(10, 1),
                ),
            ],
            [sg.Frame("", grid)],
        ]
        self.window = sg.Window(self.choice, self.layout, modal=True)

    def open_window(self):
        while True:
            event, values = self.window.read()
            if event == "Exit" or event == sg.WIN_CLOSED:
                break
        self.window.close()
