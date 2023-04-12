import time
from graphics import Point, Line, Window
class Cell:

    def __init__(self, win: Window) -> None:
        self.upper_left = None
        self.lower_right = None
        self.win = win
        self.has_right_wall = True
        self.has_left_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True

    def getCenter(self) -> Point:
        return Point((self.upper_left.y + self.lower_left.y)/2,(self.upper_left.x + self.upper_right.x)/2)
    
    def draw(self, point1: Point, point2: Point) -> None:
        self.upper_left = point1
        self.lower_right = point2
        if self.has_left_wall:
            line = Line(self.upper_left, Point(self.upper_left.x, self.lower_right.y))
            self.win.draw_line(line,"black")
        if self.has_right_wall:
            line = Line(Point(self.lower_right.x, self.upper_left.y), self.lower_right)
            self.win.draw_line(line,"black")
        if self.has_top_wall:
            line = Line(self.upper_left, Point(self.lower_right.x, self.upper_left.y))
            self.win.draw_line(line,"black")
        if self.has_bottom_wall:
            line = Line(Point(self.upper_left.x, self.lower_right.y), self.lower_right)
            self.win.draw_line(line,"black")

    def _draw_path(self, to_cell, false_path=False) -> None:
        pass

class Maze:

    def __init__(self, x:int, y:int, num_rows:int, num_cols:int, cell_size_x:int, cell_size_y:int, win:Window) -> None:
        self.x = x
        self.y = y
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self._cells = []
        self._create_cells()

    def _create_cells(self) -> None:
        for i in range(self.num_cols):
            col_cells = []
            for j in range(self.num_rows):
                col_cells.append(Cell(self.win))
            self._cells.append(col_cells)
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._draw_cell(i,j)
    
    def _draw_cell(self, i, j) -> None:
        if self.win is None:
            return
        x1 = self.x + i * self.cell_size_x
        y1 = self.y + j * self.cell_size_y
        x2 = x1 + self.cell_size_x
        y2 = y1 + self.cell_size_y
        self._cells[i][j].draw(Point(x1, y1), Point(x2, y2))
        self._animate()
    
    def _animate(self):
        if self.win is None:
            return
        self.win.redraw()
        time.sleep(0.05)