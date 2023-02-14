from graphics import Window, Line, Point
from maze import Cell,Maze

window = Window(600,600)
window.wait_for_close()
maze = Maze(10,10,5,5,50,50,window)
