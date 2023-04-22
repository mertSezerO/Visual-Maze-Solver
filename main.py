from graphics import Window
from maze import Maze

window = Window(600,600)
maze = Maze(10,10,5,5,50,50,window)
window.wait_for_close()