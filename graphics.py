from tkinter import Tk, BOTH, Canvas

class Point:

    def __init__(self, x:int, y:int):
        self.__x = x
        self.__y = y
    
    @property
    def x(self):
        return self.__x
    
    @property
    def y(self):
        return self.__y

class Line:

    def __init__(self, point1:Point, point2:Point):
        self.point1 = point1
        self.point2 = point2

    def draw(self, canvas:Canvas, colour:str):
        canvas.create_line(self.point1.x, self.point1.y, self.point2.x, self.point2.y, fill=colour, width=2)
        canvas.pack()

class Window:

    def __init__(self, width:int, heigth:int):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__canvas = Canvas(self.__root, bg="white", height=heigth, width=width)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW",self.close)
    
    def draw_line(self, line:Line, fill_colour:str):
        line.draw(self.__canvas,fill_colour)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()
        print("Window is closing now...")
    
    def close(self):
        self.__running = False