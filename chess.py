import pygame as pg
import time
import os
import cProfile
import pstats
from pstats import SortKey
from multiprocessing.pool import ThreadPool

ENABLE_ENGINE = True

BOARD_SIZE = 480
SQUARE_SIZE = BOARD_SIZE / 8
MOVE_ANIMATION_STEPS = 10
MOVE_ANIMATION_TIME = 0.25

ASSET_PATH = 'assets'

TEAM_WHITE = 0
TEAM_BLACK = 1
PLAYER_TEAM = TEAM_WHITE

BOARD_COLOR = {
	TEAM_WHITE: (200, 200, 200),
	TEAM_BLACK: (55, 55, 55)
}

PIECE_PAWN = 0
PIECE_ROOK = 1
PIECE_KNIGHT = 2
PIECE_BISHOP = 3
PIECE_QUEEN = 4
PIECE_KING = 5
PIECE_PASSANT_MARKER = 6

PIECE_SCORES = {
	PIECE_PAWN: 1,
	PIECE_ROOK: 5,
	PIECE_KNIGHT: 3,
	PIECE_BISHOP: 3,
	PIECE_QUEEN: 9,
	PIECE_KING: 999
}

PIECE_IMAGES = {
	TEAM_WHITE: {
		PIECE_PAWN: pg.image.load(os.path.join(ASSET_PATH, 'Chess_plt60.png')),
		PIECE_ROOK: pg.image.load(os.path.join(ASSET_PATH, 'Chess_rlt60.png')),
		PIECE_KNIGHT: pg.image.load(os.path.join(ASSET_PATH, 'Chess_nlt60.png')),
		PIECE_BISHOP: pg.image.load(os.path.join(ASSET_PATH, 'Chess_blt60.png')),
		PIECE_QUEEN: pg.image.load(os.path.join(ASSET_PATH, 'Chess_qlt60.png')),
		PIECE_KING: pg.image.load(os.path.join(ASSET_PATH, 'Chess_klt60.png'))
	},
	TEAM_BLACK: {
		PIECE_PAWN: pg.image.load(os.path.join(ASSET_PATH, 'Chess_pdt60.png')),
		PIECE_ROOK: pg.image.load(os.path.join(ASSET_PATH, 'Chess_rdt60.png')),
		PIECE_KNIGHT: pg.image.load(os.path.join(ASSET_PATH, 'Chess_ndt60.png')),
		PIECE_BISHOP: pg.image.load(os.path.join(ASSET_PATH, 'Chess_bdt60.png')),
		PIECE_QUEEN: pg.image.load(os.path.join(ASSET_PATH, 'Chess_qdt60.png')),
		PIECE_KING: pg.image.load(os.path.join(ASSET_PATH, 'Chess_kdt60.png'))
	}
}


CARDINAL_DIRECTION_INCREMENTS = [
	( 0, 1),
	( 0,-1),
	( 1, 0),
	(-1, 0)
]

DIAGONAL_DIRECTION_INCREMENTS = [
	( 1, 1),
	(-1,-1),
	( 1,-1),
	(-1, 1)
]

ALL_DIRECTION_INCREMENTS = \
	CARDINAL_DIRECTION_INCREMENTS + \
	DIAGONAL_DIRECTION_INCREMENTS

pool = ThreadPool()

#class Square():
#	def __init__(self, squareType, pieceType, team):
#		self.squareType = squareType
#		self.pieceType = pieceType
#		self.

class Piece():
	def __init__(self, pieceType, team):
		self.pieceType = pieceType
		self.team = team

class SpecialPiece(Piece):
	def __init__(self, *args):
		super().__init__(*args)
'''
class Board():
	def __init__(self, layout=None):
		self.layout = layout or createBoard()
		self.everySquare = 
		self.everyTeamPiece = {}
		for rank in self.layout:
			f

	def movePiece(self, move):
'''


def asciiBoard(board):
	for rank in board:
		print(''.join([str(piece.pieceType) if type(piece) == Piece else ' ' for piece in rank]))

def drawBoard(surface, board, width):

	for rankIndex, rank in enumerate(board):
		for fileIndex, piece in enumerate(rank):

			pg.draw.rect(
				surface,
				pg.Color(BOARD_COLOR[(fileIndex + rankIndex + 1) % 2]),
				pg.Rect(
					fileIndex * SQUARE_SIZE,
					width - rankIndex * SQUARE_SIZE - SQUARE_SIZE,
					SQUARE_SIZE - 1,
					SQUARE_SIZE - 1
				)
			)

			if type(piece) == Piece:
				surface.blit(
					PIECE_IMAGES[piece.team][piece.pieceType],
					(
						fileIndex * SQUARE_SIZE,
						width - rankIndex * SQUARE_SIZE - SQUARE_SIZE
					)
				)
			'''
			elif type(piece) == SpecialPiece:
				if piece.pieceType == PIECE_PASSANT_MARKER:
					pg.draw.rect(
						surface,
						pg.Color('RED'),
						pg.Rect(
							fileIndex * SQUARE_SIZE,
							width - rankIndex * SQUARE_SIZE - SQUARE_SIZE,
							SQUARE_SIZE - 1,
							SQUARE_SIZE - 1
						),
						int(SQUARE_SIZE / 20)
					)
'''

def animateMove(surface, board, move, width):

	fromPosition, toPosition = move
	fromPosX, fromPosY = fromPosition
	toPosX, toPosY = toPosition

	stepX = (toPosX - fromPosX) / MOVE_ANIMATION_STEPS
	stepY = (toPosY - fromPosY) / MOVE_ANIMATION_STEPS

	delayTime = MOVE_ANIMATION_TIME / MOVE_ANIMATION_STEPS

	movePiece = board[fromPosY][fromPosX]

	for offset in range(MOVE_ANIMATION_STEPS):
		surface.fill(0)
		drawBoard(surface, board, BOARD_SIZE)
		# Blank the square that we are moving from
		pg.draw.rect(
					surface,
					pg.Color('RED'),
					pg.Rect(
						fromPosX * SQUARE_SIZE,
						BOARD_SIZE - fromPosY * SQUARE_SIZE - SQUARE_SIZE,
						SQUARE_SIZE - 1,
						SQUARE_SIZE - 1
					)
				)

		surface.blit(
			PIECE_IMAGES[movePiece.team][movePiece.pieceType],
			(
				(fromPosX + stepX * (offset + 1)) * SQUARE_SIZE,
				width - (fromPosY + stepY * (offset + 1)) * SQUARE_SIZE - SQUARE_SIZE
			)
		)

		pg.display.flip()
		time.sleep(delayTime)

def createBoard():
	return [
		[
			Piece(PIECE_ROOK, TEAM_WHITE),
			Piece(PIECE_KNIGHT, TEAM_WHITE),
			Piece(PIECE_BISHOP, TEAM_WHITE),
			Piece(PIECE_QUEEN, TEAM_WHITE),
			Piece(PIECE_KING, TEAM_WHITE),
			Piece(PIECE_BISHOP, TEAM_WHITE),
			Piece(PIECE_KNIGHT, TEAM_WHITE),
			Piece(PIECE_ROOK, TEAM_WHITE)
		],
		[Piece(PIECE_PAWN, TEAM_WHITE)] * 8,
		[None] * 8,
		[None] * 8,
		[None] * 8,
		[None] * 8,
		[Piece(PIECE_PAWN, TEAM_BLACK)] * 8,
		[
			Piece(PIECE_ROOK, TEAM_BLACK),
			Piece(PIECE_KNIGHT, TEAM_BLACK),
			Piece(PIECE_BISHOP, TEAM_BLACK),
			Piece(PIECE_QUEEN, TEAM_BLACK),
			Piece(PIECE_KING, TEAM_BLACK),
			Piece(PIECE_BISHOP, TEAM_BLACK),
			Piece(PIECE_KNIGHT, TEAM_BLACK),
			Piece(PIECE_ROOK, TEAM_BLACK)
		]
	]

def directionalMoves(board, fromPosition, increments, limit):
	fromPosX, fromPosY = fromPosition
	fromPiece = board[fromPosY][fromPosX]
	validDirectionalMoves = []
	for incrementX, incrementY in increments:
		for offset in range(limit):
			toPosX = fromPosX + incrementX * (offset + 1)
			toPosY = fromPosY + incrementY * (offset + 1)
			if toPosX not in range(8) or toPosY not in range(8):
				break
			toPiece = board[toPosY][toPosX]
			if type(toPiece) != Piece:
				# Empty square, can move here
				validDirectionalMoves.append((toPosX, toPosY))
			else:
				if toPiece.team == fromPiece.team:
					# Same team, can't move here
					break
				else: 
					# Opposite team, can capture
					validDirectionalMoves.append((toPosX, toPosY))
					break
	return validDirectionalMoves

def isEmpty(board, position):
	piece = board[position[1]][position[0]]
	return type(piece) != Piece

def isEnemyPiece(board, position, friendlyTeam):
	piece = board[position[1]][position[0]]
	return type(piece) == Piece and piece.team != friendlyTeam

def isEnemyPassantMarker(board, position, friendlyTeam):
	piece = board[position[1]][position[0]]
	return type(piece) == SpecialPiece and piece.pieceType == PIECE_PASSANT_MARKER and piece.team != friendlyTeam

def isInCheck(board, team):
	pass

def validMoves(board, fromPosition):
	fromPosX, fromPosY = fromPosition
	fromPiece = board[fromPosY][fromPosX]
	
	validMoveList = []
	if fromPiece.pieceType == PIECE_PAWN:
		if fromPiece.team == TEAM_WHITE:
			if fromPosY < 7 and isEmpty(board, (fromPosX, fromPosY + 1)):
				validMoveList.append((fromPosX, fromPosY + 1))
			if fromPosY == 1 and isEmpty(board, (fromPosX, fromPosY + 1)) and isEmpty(board, (fromPosX, fromPosY + 2)):
				validMoveList.append((fromPosX, fromPosY + 2))
			if fromPosX > 0 and fromPosY < 7:
				toPos = (fromPosX - 1, fromPosY + 1)
				if isEnemyPiece(board, toPos, fromPiece.team) or isEnemyPassantMarker(board, toPos, fromPiece.team):
					validMoveList.append(toPos)
			if fromPosX < 7 and fromPosY < 7:
				toPos = (fromPosX + 1, fromPosY + 1)
				if isEnemyPiece(board, toPos, fromPiece.team) or isEnemyPassantMarker(board, toPos, fromPiece.team):
					validMoveList.append(toPos)
		elif fromPiece.team == TEAM_BLACK:
			if fromPosY > 0 and isEmpty(board, (fromPosX, fromPosY - 1)):
				validMoveList.append((fromPosX, fromPosY - 1))
			if fromPosY == 6 and isEmpty(board, (fromPosX, fromPosY - 1)) and isEmpty(board, (fromPosX, fromPosY - 2)):
				validMoveList.append((fromPosX, fromPosY - 2))
			if fromPosX > 0 and fromPosY > 0:
				toPos = (fromPosX - 1, fromPosY - 1)
				if isEnemyPiece(board, toPos, fromPiece.team) or isEnemyPassantMarker(board, toPos, fromPiece.team):
					validMoveList.append(toPos)
			if fromPosX < 7 and fromPosY > 0:
				toPos = (fromPosX + 1, fromPosY - 1)
				if isEnemyPiece(board, toPos, fromPiece.team) or isEnemyPassantMarker(board, toPos, fromPiece.team):
					validMoveList.append(toPos)

	elif fromPiece.pieceType == PIECE_ROOK:
		validMoveList.extend(directionalMoves(
			board,
			fromPosition,
			CARDINAL_DIRECTION_INCREMENTS,
			7
		))

	elif fromPiece.pieceType == PIECE_KNIGHT:
		offsets = [
			( 1, 2),
			( 2, 1),
			( 1,-2),
			( 2,-1),
			(-1,-2),
			(-2,-1),
			(-1, 2),
			(-2, 1)
			]
		for offsetX, offsetY in offsets:
			toPosX = fromPosX + offsetX
			toPosY = fromPosY + offsetY
			if toPosX not in range(8) or toPosY not in range(8):
				continue
			toPiece = board[toPosY][toPosX]
			if isEmpty(board, (toPosX, toPosY)) or isEnemyPiece(board, (toPosX, toPosY), fromPiece.team):
				validMoveList.append((toPosX, toPosY))

	elif fromPiece.pieceType == PIECE_BISHOP:
		validMoveList.extend(directionalMoves(
			board,
			fromPosition,
			DIAGONAL_DIRECTION_INCREMENTS,
			7
		))

	elif fromPiece.pieceType == PIECE_QUEEN:
		validMoveList.extend(directionalMoves(
			board,
			fromPosition,
			ALL_DIRECTION_INCREMENTS,
			7
		))

	elif fromPiece.pieceType == PIECE_KING:
		validMoveList.extend(directionalMoves(
			board,
			fromPosition,
			ALL_DIRECTION_INCREMENTS,
			1
		))

	#print('valid moves for ', fromPosition, validMoveList)

	return list(zip([fromPosition] * len(validMoveList), validMoveList))

def copyBoard(board):
	return [[piece for piece in rank] for rank in board]


def movePiece(board, move, validate=True):
	#print('trying move', move)
	fromPosition, toPosition = move
	fromPosX, fromPosY = fromPosition
	toPosX, toPosY = toPosition
	fromPiece = board[fromPosY][fromPosX]
	toPiece = board[toPosY][toPosX]

	#print('before move:')
	#asciiBoard(board)
	if validate:
		validMoveList = validMoves(board, fromPosition)
	newBoard = copyBoard(board)
	
	if not validate or move in validMoveList:

		# Pawn special moves
		if fromPiece.pieceType == PIECE_PAWN:

			# Lay a special marker after a two step move
			moveYOffset =  toPosY - fromPosY
			if abs(moveYOffset) == 2:
				# Mark that an en-passant happened
				newBoard[fromPosY + int(moveYOffset / 2)][fromPosX] = SpecialPiece(PIECE_PASSANT_MARKER, fromPiece.team)

			# If we capture the special marker, we capture a pawn too
			if isEnemyPassantMarker(newBoard, toPosition, fromPiece.team):
				passingPiece = newBoard[fromPosY][toPosX]
				if type(passingPiece) == Piece and \
					passingPiece.pieceType == PIECE_PAWN and \
					passingPiece.team != fromPiece.team:
					# We passed a pawn that just two-stepped
					# So capture it
					newBoard[fromPosY][toPosX] = None

		newBoard[toPosY][toPosX] = newBoard[fromPosY][fromPosX]
		newBoard[fromPosY][fromPosX] = None

		#print('moved', move)

		# Now remove any lingering passant markers from the opposing team
		for (piece, position) in everyBoardSquare(newBoard):
			if isEnemyPassantMarker(newBoard, position, fromPiece.team):
				newBoard[position[1]][position[0]] = None

		#print('after move:')
		#asciiBoard(newBoard)
		#print('old board:')
		#asciiBoard(board)
		return newBoard
	print('rejected move', move)
	return False

def everyBoardSquare(board):
	everySquare = []
	for (rankIndex, rank) in enumerate(board):
		for (fileIndex, piece) in enumerate(rank):
			everySquare.append((piece, (fileIndex, rankIndex)))
	return everySquare

def everyPiece(board):
	everyPiece = []
	for (rankIndex, rank) in enumerate(board):
		for (fileIndex, piece) in enumerate(rank):
			if type(piece) == Piece:
				everyPiece.append((piece, (fileIndex, rankIndex)))
	return everyPiece

def everyTeamPiece(board, team):
	everyFriendly = []
	for (rankIndex, rank) in enumerate(board):
		for (fileIndex, piece) in enumerate(rank):
			if type(piece) == Piece and piece.team == team:
				everyFriendly.append((piece, (fileIndex, rankIndex)))
	return everyFriendly

def evaluateBoard(board, team):
	allPieces = everyPiece(board)

	kingPos = None
	for piece, piecePosition in allPieces:
		if piece.team != team and piece.pieceType == PIECE_KING:
			kingPos = piecePosition
			break

	kingDists = []
	pieceScore = 0
	for piece, piecePosition in allPieces:
		pieceScore += PIECE_SCORES[piece.pieceType] * (1 if piece.team == team else -1)
		if kingPos and piece.team == team:
			kingDists.append(abs(kingPos[0] - piecePosition[0]) + abs(kingPos[1] - piecePosition[1]))
	kingDist = (1 - sum(kingDists) / len(kingDists) / 9) if kingPos else 0
	return pieceScore + kingDist

def generateEvaluateMoveArguments(board, moves, team, maxDepth, currentDepth):
	for move in moves:
		yield (board, move, team, maxDepth, currentDepth)

# Engine took 1559ms
# Engine took 1819ms
# Engine took 2571ms
# Engine took 3425ms
# Engine took 3726ms
# Engine took 3865ms
# Engine took 4000ms
# Engine took 4467ms
# Engine took 4989ms

def findBestMove(board, team, maxDepth, currentDepth=0):

	scoredMoveList = []
	checkMovesForTeam = team if not (currentDepth % 2) else int(not team)
	if currentDepth == -1:

		moveList = []
		for piece, piecePosition in everyTeamPiece(board, checkMovesForTeam):
			moveList.extend(validMoves(board, piecePosition))
		scores = pool.starmap(evaluateMove, generateEvaluateMoveArguments(board, moveList, team, maxDepth, currentDepth+1), 10)
		scoredMoveList = list(zip(moveList, scores))

	else:

		for piece, piecePosition in everyTeamPiece(board, checkMovesForTeam):
			pieceMoveList = validMoves(board, piecePosition)
			for pieceMove in pieceMoveList:
				startTime = time.time()
				scoredMoveList.append((pieceMove, evaluateMove(board, pieceMove, team, maxDepth, currentDepth+1)))
				#if currentDepth == 0: print('Move took {}ms to evaluate'.format(int((time.time() - startTime) * 1000)))
		
	scoredMoveList.sort(key = lambda o: o[1], reverse=team==checkMovesForTeam)
	if currentDepth==0:
		#print('possible moves {}'.format(len(moveList)))
		#print(moveList)
		pass
	return scoredMoveList[0][1] if currentDepth > 0 else scoredMoveList[0][0]

def evaluateMove(board, move, team, maxDepth, currentDepth):

	#time.sleep(0.1)
	#+print('evaluating move / team / currentDepth / maxDepth:', move, team, currentDepth, maxDepth)
	board = movePiece(board, move, validate=False)
	if currentDepth == maxDepth:
		#print('max depth! returning score')
		return evaluateBoard(board, team)

	return findBestMove(board, team, maxDepth=maxDepth, currentDepth=currentDepth)

def main():
	pg.init()
	screen = pg.display.set_mode((BOARD_SIZE,BOARD_SIZE))

	board = createBoard()

	mouseLB = False
	selectPos = (0, 0)
	selectActive = False

	validMoveList = []

	turnTeam = TEAM_WHITE
	moveNumber = 1

	while(moveNumber < 3):
		events = pg.event.get()
		for event in events:
			if event.type == pg.QUIT:
				exit(0)

		# Drawing routines

		screen.fill(0)
		drawBoard(screen, board, BOARD_SIZE)
		if selectActive:
			for move in validMoveList:
				fromPosition, toPosition = move
				toPosX, toPosY = toPosition
				pg.draw.rect(
					screen,
					pg.Color('AQUA'),
					pg.Rect(
						toPosX * SQUARE_SIZE,
						BOARD_SIZE - toPosY * SQUARE_SIZE - SQUARE_SIZE,
						SQUARE_SIZE - 1,
						SQUARE_SIZE - 1
					),
					int(SQUARE_SIZE / 10)
				)

			pg.draw.rect(
				screen,
				pg.Color('GREEN'),
				pg.Rect(
					selectPos[0] * SQUARE_SIZE,
					BOARD_SIZE - selectPos[1] * SQUARE_SIZE - SQUARE_SIZE,
					SQUARE_SIZE - 1,
					SQUARE_SIZE - 1
				),
				int(SQUARE_SIZE / 10)
			)

		pg.display.flip()
		time.sleep(0.1)

		if ENABLE_ENGINE:# and turnTeam != PLAYER_TEAM:

			# AI move
			startTime = time.time()
			#moveThreadResult = pool.apply_async(findBestMove, (board, turnTeam, 3))
			#while (True):
			#	events = pg.event.get()
			#	for event in events:
			#		if event.type == pg.QUIT:
			#			exit(0)
			#	if moveThreadResult.ready():
			#		move = moveThreadResult.get()
			#		break
			move = findBestMove(board, turnTeam, 3)
			print('Engine took {}ms'.format(int((time.time() - startTime) * 1000)))
			newBoard = movePiece(board, move)
			if newBoard:
				animateMove(screen, board, move, BOARD_SIZE)
				board = newBoard
				turnTeam = int(not turnTeam)
				moveNumber += 0.5
			else:
				print('ERROR! Found move was not valid.')
				exit(1)
				
		else:

			# Player move

			oldMouseLB = mouseLB
			mouseX, mouseY = pg.mouse.get_pos()
			mouseLB, mouseRB, mouseMB = pg.mouse.get_pressed()

			if mouseLB and not oldMouseLB:
				# Left Click

				oldSelectPos = selectPos
				selectPos = (
					int(mouseX / BOARD_SIZE * 8),
					int((BOARD_SIZE - mouseY) / BOARD_SIZE * 8)
				)
				selectPiece = board[selectPos[1]][selectPos[0]]

				if selectActive:
					if oldSelectPos == selectPos:
						# Deselect piece
						selectActive = False
					else:
						newBoard = movePiece(board, (oldSelectPos, selectPos))
						if newBoard != False:
							print('player moved', move)
							board = newBoard
							selectActive = False
							turnTeam = int(not turnTeam)
							moveNumber += 0.5
						else:
							selectPos = oldSelectPos

				elif type(selectPiece) == Piece and selectPiece.team == turnTeam:
					selectActive = True
					validMoveList = validMoves(board, selectPos)
					print('Player score:', evaluateBoard(board, PLAYER_TEAM))
					print('Enemy score:', evaluateBoard(board, int(not PLAYER_TEAM)))

if __name__ == '__main__':
	main()
	exit(0)

	# Creating profile object
	ob = cProfile.Profile()
	ob.enable()
	main()
	ob.disable()
	sortby = SortKey.CUMULATIVE
	ps = pstats.Stats(ob).sort_stats(sortby)
	ps.print_stats()
