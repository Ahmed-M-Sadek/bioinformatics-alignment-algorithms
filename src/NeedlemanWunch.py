import PySimpleGUI as sg
import Node


class Plot:
    def __init__(self, seq1, seq2, choice):
        super().__init__()
        self.sequence1 = seq1
        self.sequence2 = seq2
        self.no_of_cols = len(seq1) + 2
        sizeX = 499 / self.no_of_cols
        self.no_of_rows = len(seq2) + 2
        sizeY = 499 / self.no_of_rows
        self.choice = choice
        self.graph = sg.Graph((500, 500), (0, 500), (500, 0), key="-GRAPH-")
        self.added_elements = []

        self.layout = [
            [
                sg.T("Match score", size=(13, 1)),
                sg.In(
                    size=(35, 1),
                    key="-MATCH-",
                    tooltip="Usually a positive number",
                    default_text="1",
                ),
            ],
            [
                sg.T("Mismatch penalty", size=(13, 1)),
                sg.In(
                    size=(35, 1),
                    key="-MISMATCH-",
                    tooltip="Usually a negative number",
                    default_text="-1",
                ),
            ],
            [
                sg.T("Gap penalty", size=(13, 1)),
                sg.In(
                    size=(35, 1),
                    key="-GAP-",
                    tooltip="Usually a smaller negative number",
                    default_text="-1",
                ),
            ],
            [
                sg.Button(
                    button_text="Start",
                    size=(10, 1),
                    key="-START-",
                ),
                sg.T("", size=(50, 1), key="-NOTICE-", text_color="red"),
            ],
            [self.graph],
            [sg.T("")],
            [],
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
            self.draw_txt(self.graph_elements[0][index + 2], item, False)
        for index, item in enumerate(seq2):
            self.draw_txt(self.graph_elements[index + 2][0], item, False)

    def open_window(self):
        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED:
                break
            elif event == "-START-":
                self.window.Element("-NOTICE-").update("")
                if (
                    values["-MATCH-"].lstrip("-").isnumeric()
                    and values["-MISMATCH-"].lstrip("-").isnumeric()
                    and values["-GAP-"].lstrip("-").isnumeric()
                ):
                    match_score = int(values["-MATCH-"])
                    mismatch_penalty = int(values["-MISMATCH-"])
                    gap_penalty = int(values["-GAP-"])
                    if match_score > mismatch_penalty and match_score > gap_penalty:
                        self.refresh_graph()
                        self.get_alignment(match_score, mismatch_penalty, gap_penalty)
                    else:
                        self.window.Element("-NOTICE-").update(
                            "invalid numbers: match score must be the highest value"
                        )
                else:
                    self.window.Element("-NOTICE-").update("only numbers allowed")

        self.window.close()

    def delay(self, timeMS):
        self.window.read(timeout=timeMS)

    def refresh_graph(self):
        for item in self.added_elements:
            self.graph.DeleteFigure(item)

    def draw_txt(self, node, txt, isRemovable=True):
        txt = self.graph.draw_text(txt, node.centre)
        if isRemovable:
            self.added_elements.append(txt)

    def draw_line(self, node1, node2):
        line = self.graph.draw_line(node1.centre, node2.centre)
        self.added_elements.append(line)

    def draw_arrow(self, node1, node2, color="Black", size=1):
        lines = []
        delta1 = (0, 0)
        delta2 = (0, 0)
        centre1 = (0, 0)
        centre2 = (0, 0)
        sizeX = (499 / self.no_of_cols) / 3
        sizeY = (499 / self.no_of_rows) / 3
        if node1.centre[0] == node2.centre[0]:
            delta1 = (-10, 10)
            delta2 = (10, 10)
            centre1 = (0, -sizeY)
            centre2 = (0, sizeY)
        elif node1.centre[1] == node2.centre[1]:
            delta1 = (10, -10)
            delta2 = (10, 10)
            centre1 = (-sizeX, 0)
            centre2 = (sizeX, 0)
        else:
            delta1 = (10, 0)
            delta2 = (0, 10)
            centre1 = (-sizeX, -sizeY)
            centre2 = (sizeX, sizeY)
        lines.append(
            self.graph.draw_line(
                (node1.centre[0] + centre1[0], node1.centre[1] + centre1[1]),
                (node2.centre[0] + centre2[0], node2.centre[1] + centre2[1]),
                color=color,
                width=size,
            )
        )
        lines.append(
            self.graph.draw_line(
                (node2.centre[0] + centre2[0], node2.centre[1] + centre2[1]),
                (
                    node2.centre[0] + centre2[0] + delta1[0],
                    node2.centre[1] + centre2[1] + delta1[1],
                ),
                color=color,
                width=size,
            )
        )
        lines.append(
            self.graph.draw_line(
                (node2.centre[0] + centre2[0], node2.centre[1] + centre2[1]),
                (
                    node2.centre[0] + centre2[0] + delta2[0],
                    node2.centre[1] + centre2[1] + delta2[1],
                ),
                color=color,
                width=size,
            )
        )
        self.added_elements.extend(lines)
        return lines

    def draw_highlight(self, node1, node2, color="Green"):
        rect = self.graph.draw_rectangle(
            node1.top_left, node2.bottom_right, line_color=color, line_width=6
        )
        self.added_elements.append(rect)
        return rect

    def get_alignment(self, match, mismatch, gap):
        for i in range(1, self.no_of_rows):
            for j in range(1, self.no_of_cols):
                node = self.graph_elements[i][j]
                node.children = []
                if i == 1 and j == 1:
                    node.score = 0
                elif i == 1:
                    prev = self.graph_elements[i][j - 1]
                    node.score = prev.score + gap
                    self.draw_arrow(node, prev)
                    node.children.append(prev)
                elif j == 1:
                    prev = self.graph_elements[i - 1][j]
                    node.score = prev.score + gap
                    self.draw_arrow(node, prev)
                    node.children.append(prev)
                else:
                    max_score = 0
                    children = []
                    prevX = self.graph_elements[i][j - 1]
                    prevY = self.graph_elements[i - 1][j]
                    prevD = self.graph_elements[i - 1][j - 1]
                    if self.sequence1[j - 2] == self.sequence2[i - 2]:
                        max_score = prevD.score + match
                        children.append(prevD)
                    else:
                        max_score = prevD.score + mismatch
                        children.append(prevD)
                    if prevX.score + gap > max_score:
                        max_score = prevX.score + gap
                        children = []
                        children.append(prevX)
                    elif prevX.score + gap == max_score:
                        max_score = prevX.score + gap
                        children.append(prevX)
                    if prevY.score + gap > max_score:
                        max_score = prevY.score + gap
                        children = []
                        children.append(prevY)
                    elif prevY.score + gap == max_score:
                        max_score = prevY.score + gap
                        children.append(prevY)
                    node.score = max_score
                    for child in children:
                        self.delay(100)
                        self.draw_arrow(node, child)
                    node.children.extend(children)
                self.delay(250)
                self.draw_txt(node, node.score)
        root_node = self.graph_elements[self.no_of_rows - 1][self.no_of_cols - 1]
        paths = root_node.paths()
        prev_node = root_node
        solution = ""
        for path in paths:
            string1 = ""
            string2 = ""
            addstring1 = ""
            addstring2 = ""
            for node in path:
                if (
                    node.row_index == self.no_of_rows - 1
                    and node.col_index == self.no_of_cols - 1
                ):
                    prev_node = node
                    continue
                if node.col_index == prev_node.col_index:
                    addstring1 = "-"
                    addstring2 = self.sequence2[prev_node.row_index - 2]
                elif node.row_index == prev_node.row_index:
                    addstring1 = self.sequence1[prev_node.col_index - 2]
                    addstring2 = "-"
                else:
                    addstring1 = self.sequence1[prev_node.col_index - 2]
                    addstring2 = self.sequence2[prev_node.row_index - 2]
                self.delay(100)
                self.draw_arrow(prev_node, node, "Red", 4)
                prev_node = node
                string1 = addstring1 + string1
                string2 = addstring2 + string2
            solution += "Possible allignment:\n"
            solution += string1 + "\n"
            solution += string2 + "\n"
            solution += "\n"
        sg.Popup(solution)
