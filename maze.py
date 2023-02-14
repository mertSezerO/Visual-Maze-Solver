from graphics import Line, Point, Window
import time

class Cell:
    def __init__(self, window:Window):
        self.has_right = True
        self.has_left = True
        self.has_bottom = True
        self.has_top = True
        self._x1 = None
        self._x2 = None
        self._y1 = None
        self._y2 = None
        self._on = window
    
    def draw(self, i:int, j:int, cell_size_x:int, cell_size_y:int, maze_x: int, maze_y:int) -> None:
        self._x1 = i*cell_size_x+maze_x
        self._x2 = (i+1)*cell_size_x+maze_x
        self._y1 = j*cell_size_y+maze_y
        self._y2 = (j+1)*cell_size_y+maze_y

        if self.has_top :
            self._on.draw_line(Line(Point(self._x1, self._y1),Point(self._x1, self._y2)), "black")
        else:
            self._on.draw_line(Line(Point(self._x1, self._y1),Point(self._x1, self._y2)), "white")
        if self.has_bottom :
            self._on.draw_line(Line(Point(self._x2, self._y1),Point(self._x2, self._y2)), "black")
        else:
            self._on.draw_line(Line(Point(self._x2, self._y1),Point(self._x2, self._y2)), "white")
        if self.has_left :
            self._on.draw_line(Line(Point(self._x1, self._y1),Point(self._x2, self._y1)), "black")
        else:
            self._on.draw_line(Line(Point(self._x1, self._y1),Point(self._x2, self._y1)), "white")
        if self.has_right :
            self._on.draw_line(Line(Point(self._x1, self._y2),Point(self._x2, self._y2)), "black")
        else:
            self._on.draw_line(Line(Point(self._x1, self._y2),Point(self._x2, self._y2)), "white")
    

class Maze:

    def __init__(self, start_x:int, start_y:int, num_rows:int, num_columns:int,
                cell_size_x:int, cell_size_y:int, window:Window):
        self.maze_x = start_x
        self.maze_y = start_y
        self.num_rows = num_rows
        self.num_columns = num_columns
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.window = window
        self.create_cells()
    
    def create_cells(self) -> None:
        self.cells = [[Cell(self.window)]*self.num_rows]*self.num_columns
    
    def draw_cells(self) -> None:
        for i in range(0,self.num_rows):
            for j in range(0, self.num_columns):
                self.cells[i][j].draw(i,j,self.cell_size_x,self.cell_size_y,self.maze_x,self.maze_y)
    
    def play(self) -> None:
        if self.window is None:
            return
        self.window.redraw()
        time.sleep(0.1)

    def create_path(self, from_cell:Cell, to_cell:Cell, correct=True) -> None:
        from_x = (from_cell._x1 + from_cell._x2)/2
        from_y = (from_cell._y1 + from_cell._y2)/2

        to_x = (to_cell._x1 + to_cell._x2)/2
        to_y = (to_cell._y1 + to_cell._y2)/2

        if correct:
            fill_colour = "red"
        else:
            fill_colour = "gray"

        line = Line(Point(from_x, from_y),Point(to_x,to_y))
        self.window.draw_line(line,fill_colour)
            
