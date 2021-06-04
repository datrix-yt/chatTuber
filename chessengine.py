import functools
import operator
import chess
import pytchat
import time
import pygame

class GameState:
    def __init__(self):
        self.board = chess.Board()
        self.boarditems = self.board.fen(promoted=True).split()[0].split('/')
        self.boardgui = self.finToboard(self.boarditems)
        self.whiteToMove = True
        self.history = []
        self.turn = self.getTurn()
        self.over = self.isGameOver()
        self.draw = self.board.is_stalemate()
        self.chat = None
        self.chattimeToMove = 5

    def newGame(self):
        self.board = chess.Board('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
        self.boarditems = self.board.fen(promoted=True).split()[0].split('/')
        self.boardgui = self.finToboard(self.boarditems)

    def updateTime(self):
        return self.chattimeToMove

    def setTime(self,time):
        self.chattimeToMove = time

    def isConnected(self):
        if self.chat!= None:
            return True
        else:
            return False
    def chatIdPaste(self,text):
        self.chat = pytchat.create(video_id=text)

    def getMove(self):
        return self.board.fen().split()[1]


    def chatMove(self):
        if self.isGameOver() or self.isDraw():
            pass
        else:
            try:
                def most_frequent(List):
                    counter = 0
                    num = List[0]

                    for i in List:
                        curr_frequency = List.count(i)
                        if(curr_frequency> counter):
                            counter = curr_frequency
                            num = i

                    return num
                temp = int(self.chattimeToMove)
                chatlist = []
                finallist = []
                ti = temp
                while ti:
                    pygame.event.pump()
                    for c in self.chat.get().sync_items():
                        chatlist.append(c.message)
                    time.sleep(1)

                    ti -= 1

                for i in chatlist:

                    try:
                        m = chess.Move.from_uci(i)
                    except:
                        continue
                    if m in self.board.legal_moves:
                        finallist.append(i)
                if finallist == []:
                    self.chatMove()
                else:
                    max = most_frequent(finallist)
                    self.makeMove(max)
            except:
                self.newGame()


    def makeMove(self,move):

        try:
            moved = move.getChessNotation()
        except:
            moved = move
        m = chess.Move.from_uci(moved)

        # check legal moves

        self.history.append(moved)
        self.board.promoted = chess.QUEEN
        if m in self.board.legal_moves:
            self.board.push(m)
            self.boarditems = self.board.fen().split()[0].split('/')
            self.boardgui = self.finToboard(self.boarditems)
            print(self.boardgui)
            print(self.board)
        else:
            # pawn promotion move
            if "p" in self.boarditems[6] or "P" in self.boarditems[1]:
                if move.startRow == 1 or move.startRow == 6:
                    self.board.push(m)
                    self.board.promoted = chess.QUEEN
                    self.boarditems = self.board.fen().split()[0].split('/')
                    self.boardgui = self.finToboard(self.boarditems)
                    boardlist = list(self.board.fen().split())
                    if "p" in self.boardgui[7] or "P" in self.boardgui[0]:
                        if "p" in self.boardgui[7]:
                            idx = self.boardgui[7].index("p")
                            self.boardgui[7].remove("p")
                            self.boardgui[7].insert(idx,"q")
                        elif "P" in self.boardgui[0]:
                            idx = self.boardgui[0].index("P")
                            self.boardgui[0].remove("P")
                            self.boardgui[0].insert(idx,"Q")
                    newfen = self.boardTofin(self.boarditems,boardlist)
                    self.board = chess.Board(newfen)
                    print(self.boardgui[0])
                    print(self.boardgui)
                    print(self.board)



            if m not in self.board.legal_moves:
                print ("")

        self.draw = self.board.is_stalemate()
        return move
    def isPicesOnHighlight(self,r,c):
        self.boardgui = self.finToboard(self.boarditems)
        if self.boardgui[r][c] != '-':
            return True
        else:
            return False

    def undoMove(self):
        self.board.pop()
        self.boarditems = self.board.fen().split()[0].split('/')
        self.boardgui = self.finToboard(self.boarditems)

    def currentMove(self):
        self.turn = self.board.fen().split()[0]

    def isGameOver(self):
        return self.board.is_checkmate()

    def isDraw(self):
        if self.board.is_stalemate() or self.board.is_variant_draw() or  self.board.can_claim_threefold_repetition():
            return True
        else:
            return False

    def getTurn(self):
        return self.board.fen().split()[1]
    def boardTofin(self,fin,finboard):
        pieces = ["R","N","B","Q","K","r","n","b","q","k","p","P"]
        newlist = []
        for i in range(len(fin)):
            lastalpha =0

            string = ''
            for j in range(len(fin)):
                if fin[i][j] in pieces:
                    new = fin[i][lastalpha:j]
                    lastalpha = j+1
                    if len(new)!=0:
                        string = string + str(len(new))
                    string = string + fin[i][j]

            new = fin[i][lastalpha:8]
            if len(new)!=0:
                string = string + str(len(new))
            newlist.append(string)
        newlist = '/'.join(newlist)
        newfin = finboard[1:]
        newfin = " ".join(newfin)
        finalfen = newlist+" "+newfin
        return finalfen


    def finToboard(self,board):
        pieces = ["R","N","B","Q","K","r","n","b","q","k","p","P"]
        for i in range(len(board)):
            board[i] = list(board[i])

        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] not in pieces and board[i][j] != '-':
                    num = int(board[i].pop(j))
                    string = list(num*'-')
                    board[i].insert(j,string)
            board[i] = functools.reduce(operator.iconcat, board[i], [])
        return board

class Move:

    ranksToRows = {"1":7, "2":6,"3":5,"4":4,"5":3,"6":2,"7":1,"8":0}
    rowsToRanks = {v: k for k,v in ranksToRows.items()}
    filesToCols = {"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}
    colsToFiles = {v:k for k,v in filesToCols.items()}
    def __init__(self,startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow= endSq[0]
        self.endCol = endSq[1]
        self.peiceMoved = board[self.startRow][self.startCol]
        self.pieceCapture = board[self.endRow][self.endCol]

        if self.peiceMoved == "-":
            self.emptyspace = 1
        else:
            self.emptyspace = 0

    def getRowCol(self,notation):
        col = self.filesToCols[notation[0]]
        row = self.ranksToRows[notation[1]]
        return [row,col]

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self,r,c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
