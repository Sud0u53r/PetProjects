import math, time, sys, os, copy
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'This is to hide the support message at start!'
import pygame

BOARD_HISTORY = []
BLACK = (0,  0,  0)
WHITE = (255, 255, 255)
LIGHTGRAY = (200, 200, 200)
WINDOWMULTIPLIER = 5
WINDOWSIZE = 100
WINDOWWIDTH = WINDOWSIZE * WINDOWMULTIPLIER
WINDOWHEIGHT = WINDOWSIZE * WINDOWMULTIPLIER
SQUARESIZE = (WINDOWSIZE * WINDOWMULTIPLIER) // 3
CELLSIZE = SQUARESIZE // 3

def CheckBox(board, pos, num):
	row, col = pos
	box = [board[x][y] for x in [row-(row % 3)+i for i in range(3)] for y in [col-(col % 3)+i for i in range(3)]]
	return box.count(num) == 0

def CheckRow(board, pos, num):
	row = pos[0]
	return board[row].count(num) == 0

def CheckCol(board, pos, num):
	col = pos[1]
	return [row[col] for row in board].count(num) == 0

CONDITIONS = [
	CheckBox,
	CheckRow,
	CheckCol
]

def draw(screen, board, font):
	screen.fill(WHITE)
	for x in range(0, WINDOWWIDTH, CELLSIZE):
		pygame.draw.line(screen, LIGHTGRAY, (x, 0), (x, WINDOWHEIGHT))
	for y in range (0, WINDOWHEIGHT, CELLSIZE):
		pygame.draw.line(screen, LIGHTGRAY, (0,y), (WINDOWWIDTH, y))

	for x in range(0, WINDOWWIDTH, SQUARESIZE):
		pygame.draw.line(screen, BLACK, (x,0),(x,WINDOWHEIGHT))
	for y in range (0, WINDOWHEIGHT, SQUARESIZE):
		pygame.draw.line(screen, BLACK, (0,y), (WINDOWWIDTH, y))
	
	for index, row in enumerate(board):
		textSurface = font.render('   '.join(map(str, row)).replace('0', ' '), True, BLACK)
		screen.blit(textSurface, (CELLSIZE//3, (index*CELLSIZE)+(CELLSIZE//5)))

def solve(board):
	BOARD_HISTORY.append(board)
	for x in range(9):
		for y in range(9):
			if board[x][y] == 0:
				ss = [all([cond(board, (x,y), num) for cond in CONDITIONS]) for num in range(1,10)]
				if ss.count(True) == 0:
					return False
				elif ss.count(True) == 1:
					valid_num = ss.index(True) + 1
					board[x][y] = valid_num
					return solve(board)
				else:
					valid_nums = [i+1 for i in range(9) if ss[i] == True]
					for num in valid_nums:
						tmp = copy.deepcopy(board)
						tmp[x][y] = num
						nn = solve(tmp)
						if nn is not False: return nn
					else:
						return False
	return board

puzzle1 = [
	[6, 0, 9, 1, 0, 2, 0, 8, 0],
	[0, 0, 0, 0, 0, 0, 4, 0, 0],
	[5, 0, 2, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 2, 0, 3, 0, 4],
	[1, 0, 0, 0, 0, 5, 0, 0, 0],
	[0, 2, 0, 0, 0, 0, 5, 0, 6],
	[0, 0, 0, 8, 0, 1, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 9],
	[8, 0, 5, 9, 0, 7, 0, 4, 0]
]

if __name__ == '__main__':
	xxx = solve(puzzle1)
	pygame.init()
	screen = pygame.display.set_mode([500, 500])
	font = pygame.font.Font('/usr/share/fonts/truetype/ubuntu/UbuntuMono-R.ttf', 28)
	running = True
	i = 0
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
		time.sleep(1/60)
		i += 1
		draw(screen, BOARD_HISTORY[i], font)
		pygame.display.update()
