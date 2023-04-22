import random
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
        self.visited = False

    @property
    def center(self) -> Point:
        return Point((self.upper_left.y + self.lower_left.y)/2,(self.upper_left.x + self.upper_right.x)/2)
    
    def draw(self, point1: Point, point2: Point) -> None:
        self.upper_left = point1
        self.lower_right = point2
        if self.has_left_wall:
            line = Line(self.upper_left, Point(self.upper_left.x, self.lower_right.y))
            self.win.draw_line(line,"black")
        else:
            line = Line(self.upper_left, Point(self.upper_left.x, self.lower_right.y))
            self.win.draw_line(line,"white")
        if self.has_right_wall:
            line = Line(Point(self.lower_right.x, self.upper_left.y), self.lower_right)
            self.win.draw_line(line,"black")
        else:
            line = Line(Point(self.lower_right.x, self.upper_left.y), self.lower_right)
            self.win.draw_line(line,"white")
        if self.has_top_wall:
            line = Line(self.upper_left, Point(self.lower_right.x, self.upper_left.y))
            self.win.draw_line(line,"black")
        else:
            line = Line(self.upper_left, Point(self.lower_right.x, self.upper_left.y))
            self.win.draw_line(line,"white")
        if self.has_bottom_wall:
            line = Line(Point(self.upper_left.x, self.lower_right.y), self.lower_right)
            self.win.draw_line(line,"black")
        else:
            line = Line(Point(self.upper_left.x, self.lower_right.y), self.lower_right)
            self.win.draw_line(line,"white")

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
        self._create_maze()

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

    def _create_maze(self) -> None:
        self._create_entrance_and_exit()
        self._break_walls(0,0)

    #entrance is at the top of first cell, exit at the bottom of last cell
    def _create_entrance_and_exit(self) -> None:
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[self.num_cols-1][self.num_rows-1].has_bottom_wall = False
        self._draw_cell(self.num_cols - 1, self.num_rows - 1)

    def _break_walls(self, i, j) -> None:
        self._cells[i][j].visited = True
        while True:
            next_cells = []

            options = 0

            # determine which cell(s) to visit next
            # left
            if i > 0 and not self._cells[i - 1][j].visited:
                next_cells.append((i - 1, j))
                options += 1
            # right
            if i < self.num_cols - 1 and not self._cells[i + 1][j].visited:
                next_cells.append((i + 1, j))
                options += 1
            # up
            if j > 0 and not self._cells[i][j - 1].visited:
                next_cells.append((i, j - 1))
                options += 1
            # down
            if j < self.num_rows - 1 and not self._cells[i][j + 1].visited:
                next_cells.append((i, j + 1))
                options += 1

            # if there is nowhere to go from here
            # just break out
            if options == 0:
                self._draw_cell(i, j)
                return

            # randomly choose the next direction to go
            index = random.randrange(options)
            next_cell = next_cells[index]

            # knock out walls between this cell and the next cell(s)
            # right
            if next_cell[0] == i + 1:
                self._cells[i][j].has_right_wall = False
                self._cells[i + 1][j].has_left_wall = False
            # left
            if next_cell[0] == i - 1:
                self._cells[i][j].has_left_wall = False
                self._cells[i - 1][j].has_right_wall = False
            # down
            if next_cell[1] == j + 1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j + 1].has_top_wall = False
            # up
            if next_cell[1] == j - 1:
                self._cells[i][j].has_top_wall = False
                self._cells[i][j - 1].has_bottom_wall = False

            # recursively visit the next cell
            self._break_walls(next_cell[0], next_cell[1])

