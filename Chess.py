#Some code has been taken from https://www.youtube.com/watch?v=EnYui0e73Rs when i was unable to make my own, or my own was too slow

import ChessEngine
import pygame as p
from time import time
import sys

dim = 8  # Dimensions (8x8)
sqsize = 64
maxfps = 15
images = {}

board_c = int(input("Board color choices:\n1. Dark\n2. Light\n3. Blue\n4. Green\nPlease enter the number of the board color you want: "))
while board_c != 1 and board_c != 2 and board_c != 3 and board_c != 4:
    board_c = int(input("Board color choices:\n1. Dark\n2. Light\n3. Blue\n4. Green\nPlease enter the number of the board color you want: "))

depth = int(input("Please enter how many moves you want the AI to look forward\nThe bigger the number the slower the AI will play\n: "))
while depth != int and depth > 99:
    depth = int(input("Please enter how many moves you want the AI to look forward\nThe bigger the number the slower the AI will play\n: "))

b_color = int(input("Background color choices:\n1.White\n2.Black\nEnter either 1 or 2 for the background color: "))
while b_color != 1 and b_color != 2:
    b_color = int(input("Background color choices:\n1.White\n2.Black\nEnter either 1 or 2 for the background color: "))


p.init()


def loadImages():
    pieces = ["wp", "wR", "wN", "wB", "wQ", "wK", "bp", "bR", "bN", "bB", "bQ", "bK"]
    for piece in pieces:
        images[piece] = p.transform.scale(p.image.load("Images/" + piece + ".png"), (sqsize, sqsize))


def main():
    # p.init()
    # board_c = int(input("Board color choices:\n1. Dark\n2. Light\n3. Blue\n4. Green\nPlease enter the number of the board color you want: "))
    # while board_c != 1 and board_c != 2 and board_c != 3 and board_c != 4:
    #    board_c = int(input("Board color choices:\n1. Dark\n2. Light\n3. Blue\n4. Green\nPlease enter the number of the board color you want: "))

    # depth = int(input("Please enter how many moves you want the AI to look forward\nThe bigger the number the slower the AI will play\n: "))
    # if depth != int and depth > 99:
    #    depth = int(input("Please enter how many moves you want the AI to look forward\nThe bigger the number the slower the AI will play\n: "))

    # b_color = int(input("Background color choices:\n1.White\n2.Black\nEnter either 1 or 2 for the background color: "))
    # while b_color != 1 and b_color != 2:
    #    b_color = int(input("Background color choices:\n1.White\n2.Black\nEnter either 1 or 2 for the background color: "))

    screen = p.display.set_mode((512, 512))
    clock = p.time.Clock()
    moveLog = []

    screen.fill(p.Color("White"))

    gs = ChessEngine.GameState()
    m = ChessEngine.Move
    validMoves = gs.getValidMoves()
    board = gs.board
    turn = "white"
    whiteToMove = True
    moveMade = False
    loadImages()
    running = True

    sqSelected = ()
    playerClicks = []
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
                p.quit()
                exit()

            if e.type == p.MOUSEBUTTONDOWN and gs.whiteToMove:
                location = p.mouse.get_pos()
                col = location[0] // sqsize
                row = location[1] // sqsize
                if sqSelected == (row, col):
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)

                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    for i in range(len(validMoves)):
                        if move == validMoves[i]:
                            gs.makeMove(validMoves[i])
                            moveMade = True
                            #print(board)
                            sqSelected = ()
                            playerClicks = []
                            print(m.getChessNot(move))
                            moveLog.append(m.getChessNot(move))
                            print("Black's turn.")
                    if not moveMade:
                        playerClicks = [sqSelected]

            if e.type == p.KEYDOWN:
                if e.key == p.K_p:
                    p.quit()
                    exit()

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
            whiteToMove = not whiteToMove

        if whiteToMove:
            turn = "white"
        else:
            turn = "black"

        # sDepth = str(depth)
        # p.display.set_caption("Chess game - Depth" + sDepth)
        drawGameState(screen, gs, board_c)
        clock.tick(maxfps)
        p.display.flip()

        if gs.checkMate and not gs.AIturn:
            print("Black wins by checkmate") if gs.whiteToMove else print("White wins by checkmate")
            running = False
            f = open("Chess Game.txt", "w")
            f = open("Chess Game.txt", "a")
            f.write('\n'.join(map(str, moveLog)))
            p.quit()

        if gs.stalemate and not gs.AIturn:
            print("Draw by stalemate")
            running = False
            f = open("Chess Game.txt", "w")
            f = open("Chess Game.txt", "a")
            f.write('\n'.join(map(str, moveLog)))
            p.quit()

        if not gs.whiteToMove and len(validMoves) != 0 and not moveMade:
            t_0 = time()
            x = gs.getBestMove(depth, False)
            gs.makeMove(x)
            t_1 = time()
            moveMade = True
            #print(board)
            t_r = t_1 - t_0
            t = round(t_r, 4)
            print("That move took", t, "seconds.")
            print("White's turn.")





def drawGameState(screen, gs, board_c):
    drawBoard(screen, board_c)
    drawPieces(screen, gs.board)


def drawBoard(screen, board_c):
    if board_c == 1:
        colors = [p.Color(204, 183, 174), p.Color(112, 102, 119)]
    if board_c == 2:
        colors = [p.Color(240, 217, 181), p.Color(181, 136, 99)]
    if board_c == 3:
        colors = [p.Color(157, 172, 255), p.Color(111, 115, 210)]
    if board_c == 4:
        colors = [p.Color(238, 238, 210), p.Color(118, 150, 86)]
    for r in range(dim):
        for c in range(dim):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * sqsize, r * sqsize, sqsize, sqsize))


def drawPieces(screen, board):
    for r in range(dim):
        for c in range(dim):
            piece = board[r][c]
            if piece != "--":
                screen.blit(images[piece], p.Rect(c * sqsize, r * sqsize, sqsize, sqsize))


if __name__ == "__main__":
    main()

