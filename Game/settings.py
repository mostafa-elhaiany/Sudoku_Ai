WIDTH = 600
HEIGHT= 600

#colours
WHITE=(255,255,255)
BLACK=(0,0,0)
BLUE=(0,0,255)
RED=(255,0,0)
GREEN=(0,255,0)
GRAY=(190,190,190)

#boards
ROWS=9
COLS=9
test_board = [[0 for _ in range(ROWS)] for _ in range(COLS)]

#positions and sizes
MARGIN = 150
grid_pos= (75, 100, WIDTH-MARGIN, HEIGHT-MARGIN)
cell_size= ((grid_pos[2]-grid_pos[0])/ ROWS) + ROWS-1
grid_size= cell_size * ROWS 

