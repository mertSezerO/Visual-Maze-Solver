from graphics import Window, Line, Point

window = Window(600,800)
line = Line(Point(25,60), Point(125,500))
window.draw_line(line,"red")
window.wait_for_close()