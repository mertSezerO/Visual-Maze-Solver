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
        return Point((self.upper_left.x+self.lower_right.x)/2,(self.upper_left.y + self.lower_right.y)/2)
    
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
        if self.win is None:
            return
        fill_color = "red"
        if false_path:
            fill_color = "gray"

        # moving left
        if self.upper_left.x > to_cell.upper_left.x:
            line = Line(Point(self.upper_left.x, self.center.y), Point(self.center.x, self.center.y))
            self.win.draw_line(line, fill_color)
            line = Line(Point(to_cell.center.x, to_cell.center.y), Point(to_cell.lower_right.y, to_cell.center.y))
            self.win.draw_line(line, fill_color)

        # moving right
        elif self.upper_left.x < to_cell.upper_left.x:
            line = Line(Point(self.center.x, self.center.y), Point(self.lower_right.x, self.center.y))
            self.win.draw_line(line, fill_color)
            line = Line(Point(to_cell.upper_left.x, to_cell.center.y), Point(to_cell.center.x, to_cell.center.y))
            self.win.draw_line(line, fill_color)

        # moving up
        elif self.upper_left.y > to_cell.upper_left.y:
            line = Line(Point(self.center.x, self.center.y), Point(self.center.x, self.upper_left.y))
            self.win.draw_line(line, fill_color)
            line = Line(Point(to_cell.center.x, to_cell.lower_right.y), Point(to_cell.center.x, to_cell.center.y))
            self.win.draw_line(line, fill_color)

        # moving down
        elif self.upper_left.y < to_cell.upper_left.y:
            line = Line(Point(self.center.x, self.center.y), Point(self.center.x, self.lower_right.y))
            self.win.draw_line(line, fill_color)
            line = Line(Point(to_cell.center.x, to_cell.center.y), Point(to_cell.center.x, to_cell.upper_left.y))
            self.win.draw_line(line, fill_color)

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
        self.normalize_cells()

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

    def normalize_cells(self) -> None:
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                self._cells[i][j].visited = False

    #break walls using BFS algorithm
    def _break_walls(self, i, j) -> None:
        self._cells[i][j].visited = True
        while True:
            next_cells = []

            options = 0

            # determine which cell to visit next
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

            #if all options handled, break the process
            if options == 0:
                self._draw_cell(i, j)
                return

            # randomly choose next cell
            index = random.randrange(options)
            next_cell = next_cells[index]

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

            self._break_walls(next_cell[0], next_cell[1])

    def solve(self, i=0, j=0):
        self._animate()

        # vist the current cell
        self._cells[i][j].visited = True

        # if we are at the end cell, we are done!
        if i == self.num_cols - 1 and j == self.num_rows - 1:
            return True

        # move left if there is no wall and it hasn't been visited
        if (
            i > 0
            and not self._cells[i][j].has_left_wall
            and not self._cells[i - 1][j].visited
        ):
            self._cells[i][j]._draw_path(self._cells[i - 1][j])
            if self.solve(i - 1, j):
                return True
            else:
                self._cells[i][j]._draw_path(self._cells[i - 1][j], True)

        # move right if there is no wall and it hasn't been visited
        if (
            i < self.num_cols - 1
            and not self._cells[i][j].has_right_wall
            and not self._cells[i + 1][j].visited
        ):
            self._cells[i][j]._draw_path(self._cells[i + 1][j])
            if self.solve(i + 1, j):
                return True
            else:
                self._cells[i][j]._draw_path(self._cells[i + 1][j], True)

        # move up if there is no wall and it hasn't been visited
        if (
            j > 0
            and not self._cells[i][j].has_top_wall
            and not self._cells[i][j - 1].visited
        ):
            self._cells[i][j]._draw_path(self._cells[i][j - 1])
            if self.solve(i, j - 1):
                return True
            else:
                self._cells[i][j]._draw_path(self._cells[i][j - 1], True)

        # move down if there is no wall and it hasn't been visited
        if (
            j < self.num_rows - 1
            and not self._cells[i][j].has_bottom_wall
            and not self._cells[i][j + 1].visited
        ):
            self._cells[i][j]._draw_path(self._cells[i][j + 1])
            if self.solve(i, j + 1):
                return True
            else:
                self._cells[i][j]._draw_path(self._cells[i][j + 1], True)

        # we went the wrong way let the previous cell know by returning False
        return False