import PySimpleGUI as sg
import Node


class Plot:
    def __init__(self, seq1, seq2, choice):
        super().__init__()
        self.sequence1 = seq1
        self.sequence2 = seq2
        self.no_of_cols = len(seq1) + 1
        sizeX = 499 / self.no_of_cols
        self.no_of_rows = len(seq2) + 1
        sizeY = 499 / self.no_of_rows
        self.choice = choice
        self.graph = sg.Graph((500, 500), (0, 500), (500, 0), key="-GRAPH-")
        self.highlightX = 0
        self.added_elements = []

        self.layout = [
            [
                sg.T("Window size", size=(13, 1)),
                sg.In(size=(35, 1), key="-SIZEW-"),
            ],
            [
                sg.T("Step", size=(13, 1)),
                sg.In(size=(35, 1), key="-STEP-"),
            ],
            [
                sg.T("Threshold", size=(13, 1)),
                sg.In(size=(35, 1), key="-THRESH-"),
            ],
            [
                sg.Button(
                    button_text="Start",
                    size=(10, 1),
                    key="-START-",
                ),
                sg.T("", size=(25, 1), key="-NOTICE-", text_color="red"),
            ],
            [self.graph],
            [sg.T("")],
        ]
        self.window = sg.Window(
            self.choice,
            self.layout,
            finalize=True,
            size=(600, 650),
        )
        self.graph_elements = []
        for j in range(self.no_of_rows):
            col = []
            for i in range(self.no_of_cols):
                startX = i * sizeX
                endX = (i + 1) * sizeX

                startY = j * sizeY
                endY = (j + 1) * sizeY

                self.graph.draw_rectangle(
                    (startX, startY),
                    (endX, endY),
                    line_color="Black",
                    fill_color="White",
                )
                col.append(
                    Node.Node((i, j), (sizeX, sizeY), (startX, startY), (endX, endY))
                )
            self.graph_elements.append(col)

        for index, item in enumerate(seq1):
            self.draw_txt(self.graph_elements[0][index + 1], item)
        for index, item in enumerate(seq2):
            self.draw_txt(self.graph_elements[index + 1][0], item)

    def open_window(self):
        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED:
                break
            elif event == "-START-":
                self.window.Element("-NOTICE-").update("")
                if (
                    values["-SIZEW-"].isnumeric()
                    and values["-STEP-"].isnumeric()
                    and values["-THRESH-"].isnumeric()
                    or not values["-THRESH-"]
                ):
                    window_size = max(int(values["-SIZEW-"]), 1)
                    step_size = max(int(values["-STEP-"]), 1)
                    thresh = (
                        0 if not values["-THRESH-"] else max(int(values["-THRESH-"]), 0)
                    )
                    min_size = min(self.no_of_cols - 1, self.no_of_rows - 1)
                    if (
                        window_size <= min_size
                        and (min_size - window_size) % step_size == 0
                        and window_size % 2 == 1
                        and thresh <= window_size
                    ):
                        self.refresh_graph()
                        self.get_alignment(window_size, step_size, thresh)
                    else:
                        self.window.Element("-NOTICE-").update("invalid numbers")
                else:
                    self.window.Element("-NOTICE-").update("only numbers allowed")

        self.window.close()

    def delay(self, timeMS):
        self.window.read(timeout=timeMS)

    def refresh_graph(self):
        for item in self.added_elements:
            self.graph.DeleteFigure(item)

    def draw_dot(self, node):
        point = self.graph.draw_point(node.centre, size=4)
        self.added_elements.append(point)

    def draw_txt(self, node, txt):
        txt = self.graph.draw_text(txt, node.centre)

    def draw_line(self, node1, node2):
        line = self.graph.draw_line(node1.centre, node2.centre)
        self.added_elements.append(line)

    def draw_highlight(self, node1, node2, color="Green"):
        rect = self.graph.draw_rectangle(
            node1.top_left, node2.bottom_right, line_color=color, line_width=6
        )
        self.added_elements.append(rect)
        return rect

    def get_alignment(self, window_size, step, thresh=0):
        highlight1 = self.draw_highlight(
            self.graph_elements[0][1],
            self.graph_elements[0][window_size],
        )
        highlight2 = self.draw_highlight(
            self.graph_elements[1][0],
            self.graph_elements[window_size][0],
        )
        sizeX = 499 / self.no_of_cols
        sizeY = 499 / self.no_of_rows
        for i in range(0, self.no_of_rows - window_size, step):
            self.highlightX = step * sizeX
            if i != 0:
                self.graph.MoveFigure(highlight2, 0, step * sizeY)
                self.delay(100)
            for j in range(0, self.no_of_cols - window_size, step):
                score = 0
                self.highlightX -= step * sizeX
                if j != 0:
                    self.graph.MoveFigure(highlight1, step * sizeX, 0)
                    self.delay(100)
                if window_size == 1 and self.sequence1[j] == self.sequence2[i]:
                    score += 1
                else:
                    for count in range(0, window_size, 1):
                        if self.sequence1[j + count] == self.sequence2[i + count]:
                            score += 1
                self.graph_elements[i + 1 + window_size // 2][
                    j + 1 + window_size // 2
                ].score = score
                if score >= thresh:
                    self.draw_dot(
                        self.graph_elements[i + 1 + window_size // 2][
                            j + 1 + window_size // 2
                        ]
                    )
                    self.delay(100)
                    if (
                        (i + 1 - step + window_size // 2) >= 1
                        and (j + 1 - step + window_size // 2) >= 1
                        and self.graph_elements[i + 1 - step + window_size // 2][
                            (j + 1 - step + window_size // 2)
                        ].score
                        >= thresh
                    ):
                        self.draw_line(
                            self.graph_elements[i + 1 + window_size // 2][
                                j + 1 + window_size // 2
                            ],
                            self.graph_elements[i + 1 - step + window_size // 2][
                                j + 1 - step + window_size // 2
                            ],
                        )
                        self.delay(100)
            self.graph.MoveFigure(highlight1, self.highlightX, 0)
            self.delay(100)
            self.highlightX = sizeX * step
