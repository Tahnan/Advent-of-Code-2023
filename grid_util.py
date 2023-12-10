DIRECTIONS = ((-1, -1), (-1, 0), (-1, 1),
              (0, -1),         (0, 1),
              (1, -1), (1, 0), (1, 1))

class Grid(dict):
    # Order is (row, column)
    def __init__(self, grid):
        super().__init__(grid)
        mr, mc = max(self)
        self.rows = mr + 1
        self.columns = mc + 1

    @classmethod
    def from_text(cls, grid_text, sep=None):
        if sep is None:
            sepfunc = lambda x: x
        else:
            sepfunc = lambda x: x.split(sep)
        dic = {}
        for row, line in enumerate(grid_text.splitlines()):
            for col, entry in enumerate(sepfunc(line)):
                dic[(row, col)] = entry
        return cls(dic)

    @classmethod
    def from_dimensions(cls, x, y, default=''):
        return cls({(a, b): default for b in range(y) for a in range(x)})

    def to_text(self, sep=''):
        return '\n'.join(
            sep.join(self[(r, c)] for c in range(self.columns))
            for r in range(self.rows)
        )

    def get_row(self, rownum):
        return [self[(rownum, c)] for c in range(self.columns)]

    def get_column(self, colnum):
        return [self[(r, colnum)] for r in range(self.rows)]

    def get_neighbors(self, coord, diagonals=False):
        neighbors = []
        for direction in DIRECTIONS:
            if not (diagonals or 0 in direction):
                continue
            nb = (coord[0] + direction[0], coord[1] + direction[1])
            if nb in self:
                neighbors.append(self[nb])
        return neighbors

    def get_line(self, coord, direction, distance, past_edge=None):
        x, y = coord
        dx, dy = direction
        if (past_edge is None
            and (x + dx * (distance - 1), y + dy * (distance - 1)) not in self):
            return
        return ''.join(self.get((x + dx * i, y + dy * i), past_edge)
                       for i in range(distance))
