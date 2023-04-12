import unittest
from maze import Maze

class Tests(unittest.TestCase):
    def test_maze_rows_cols(self):
        num_rows = 8
        num_cols = 10
        maze = Maze(0,0,num_rows,num_cols,10,10,None)
        self.assertEqual(
            num_rows,
            len(maze._cells[0])
        )

        self.assertEqual(
            num_cols,
            len(maze._cells)
        )

    def test_maze_cells(self):
        num_cells = 25
        maze = Maze(0,0,5,5,10,10,None)
        self.assertEqual(
            num_cells,
            len(maze._cells[0])*len(maze._cells)
        )

    def test_has_walls(self) :
        num_of_walls = 36
        maze = Maze(0,0,3,3,10,10,None)
        walls=0
        for i in range(3):
            for j in range(3):
                if maze._cells[i][j].has_right_wall:
                    walls += 1
                if maze._cells[i][j].has_left_wall:
                    walls += 1
                if maze._cells[i][j].has_top_wall:
                    walls += 1
                if maze._cells[i][j].has_bottom_wall:
                    walls += 1
        self.assertEqual(
            num_of_walls,
            walls
        )

if __name__ == "__main__":
    unittest.main()