class Node:
    def __init__(self, indices, size, start, end):
        self.score = 0
        self.children = []
        self.size = size
        self.centre = (((start[0] + end[0]) / 2), (start[1] + end[1]) / 2)
        self.top_left = start
        self.bottom_right = end
        self.col_index = indices[0]
        self.row_index = indices[1]

    def paths(self):
        if not self.children:
            return [[self]]
        paths = []
        for child in self.children:
            for path in child.paths():
                paths.append([self] + path)
        return paths