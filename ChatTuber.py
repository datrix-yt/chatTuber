import time
import pygame as pg
import chessengine
import inputfield
H = 512
W = 700

DIMENSION = 8
SQ_SIZE = H//DIMENSION
MAX_FPS = 15
IMAGES= {}
currentpiece = "pieces_image"
def loadImage():
    global currentpiece
    pieces = ["R","N","B","Q","K","r","n","b","q","k","p","P"]
    for piece in pieces:
        if piece.islower():
            IMAGES[piece] = pg.transform.scale(pg.image.load(currentpiece+"/b/"+piece+".png"),(SQ_SIZE,SQ_SIZE))
        else:
            IMAGES[piece] = pg.transform.scale(pg.image.load(currentpiece+"/w/"+piece+".png"),(SQ_SIZE,SQ_SIZE))

def main():
    # initborad = gs.board.fen().split()[0].split("/")
    global currentpiece
    pg.init()
    surface = pg.image.load('logo.png')
    pg.display.set_icon(surface)
    screen = pg.display.set_mode((W,H))
    pg.display.set_caption("Chat vs Tuber")
    clock = pg.time.Clock()
    screen.fill(pg.Color((32.5, 38, 38.4)))
    gs = chessengine.GameState()
    input_box = inputfield.InputBox(H+((W-H)//2)-90, H//2+170, 40, 28)
    chattimer = inputfield.InputBox(H+((W-H)//2)-90, H//2+90, 30, 28)
    loadImage()
    pressed = False
    running = True
    sqSelected =()
    playerClicks = []
    button = pg.Rect(H+((W-H)//2)-60, H//2-25, 120, 50)
    switch_p = pg.Rect(H+((W-H)//2)-60, H//2-100, 120, 50)
    font = pg.font.Font("Font/Uniflex_PersonalUseOnly.ttf", 20)
    white = (255,255, 255)

    # ui text above submit form of link
    linkxt = "Press 'P' To Paste (YT Link)"
    linkposx =H+((W-H)//2)
    linkposy = H//2+150

    timerxt = "Chat Time(sec) To Move"
    timerposx =H+((W-H)//2)
    timerposy = H//2+70
    def showTxtOnScreen(screen,text,x,y):
        linkxt = text
        linktextshow = pg.font.Font("Font/Louis George Cafe.ttf",15)
        linktextshow = linktextshow.render(linkxt,True, white)
        linktextshowRect = linktextshow.get_rect()
        linktextshowRect.center = (x, y)
        screen.blit(linktextshow,linktextshowRect)

    starttext = font.render("Start New", True, white)

    starttextRect = starttext.get_rect()

    switchtext = font.render("Switch Pieces", True, white)

    seitchtextrect = starttext.get_rect()

    starttextRect.center = (H+((W-H)//2), H//2)
    seitchtextrect.center = (H+((W-H)//2-18), H//2-75)
    switched_button_color = (154,205,50)
    while running:
        if gs.getMove() == 'b':
            gs.chatMove()

        if gs.isGameOver():
            displayGameOver(screen,gs)
        if gs.isDraw():
            displayDraw(screen)
        for e in pg.event.get():
            input_box.handle_event(e)
            chattimer.handle_event(e)
            if e.type == pg.QUIT:
                
                running = False
                pg.display.quit()
                pg.quit()
            elif e.type == pg.MOUSEBUTTONDOWN:
                location = pg.mouse.get_pos()
                if H//2-25<location[1]<H//2-25+50 and H+((W-H)//2)-60<location[0]<H+((W-H)//2)+60:

                    gs.newGame()
                if H//2-100<location[1]<H//2-100+50 and H+((W-H)//2)-60<location[0]<H+((W-H)//2)+60:

                    if currentpiece == "pieces_image":
                        currentpiece = "legend_picese"
                        pressed = True
                    else:
                        currentpiece = "pieces_image"
                        pressed = False
                    loadImage()
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE

                if sqSelected == (row,col):
                    sqSelected = ()
                    playerClicks = []
                else:


                    if row>7 or col>7:
                        sqSelected = ()
                        playerClicks = []

                    else:
                        sqSelected = (row,col)
                        playerClicks.append(sqSelected)
                if len(playerClicks) == 1:
                    if not gs.isPicesOnHighlight(playerClicks[0][0],playerClicks[0][1]):
                            sqSelected = ()
                            playerClicks = []

                if len(playerClicks)==2:

                    move = chessengine.Move(playerClicks[0],playerClicks[1], gs.boardgui)
                    if move.emptyspace != 1:

                        gs.makeMove(move)

                        sqSelected = ()
                        playerClicks = []

            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_z:
                    gs.undoMove()
        if gs.isGameOver():
            displayGameOver(screen,gs)
        if gs.isDraw():
            displayDraw(screen)
        # input field
        input_box.update()
        chattimer.update()

        # shows game screen
        drawGameState(screen,gs,sqSelected)
        showTxtOnScreen(screen,linkxt,linkposx,linkposy)
        showTxtOnScreen(screen,timerxt,timerposx,timerposy)

        # displays inputbox
        input_box.draw(screen)
        chattimer.draw(screen)
        # get youtube stream watch id
        chatId = input_box.getText()
        if chatId != None:
            gs.chatIdPaste(chatId)

        #chat time set in sec
        chattime = chattimer.getText()
        if chattime != None:
            gs.setTime(chattime)
        if pressed == True:
            switched_button_color = (50,205,50)
        else:
            switched_button_color = (154,205,50)
        # start new button
        pg.draw.rect(screen, (154,205,50), button)
        pg.draw.rect(screen, switched_button_color, switch_p)
        screen.blit(starttext,starttextRect)
        screen.blit(switchtext,seitchtextrect)
        clock.tick(MAX_FPS)
        pg.display.flip()


def pieceInSquare():
    pass

def displayDraw(screen):
    font = pg.font.Font('Font/Uniflex_PersonalUseOnly.ttf', 32)
    green = (0, 255, 0)
    blue = (0, 0, 128)
    text = font.render("DRAW", True, green, blue)

    textRect = text.get_rect()

    textRect.center = (H // 2, W // 2)
    screen.blit(text,textRect)

def drawGameState(screen,gs,sqselected):
    drawBoard(screen)
    displayTurn(screen, gs)
    drawName(screen,gs)
    displayTimer(screen,gs)
    displayConnected(screen,gs)
    highlight(screen,sqselected)
    drawPieces(screen, gs.boardgui)
    if gs.isGameOver():
        displayGameOver(screen,gs)

def displayTimer(screen,gs):
    font = pg.font.Font('Font/Louis George Cafe.ttf', 25)
    green = (255, 255, 255)
    text = str(gs.updateTime())
    text = font.render(text, True, green,(32.5, 38, 38.4))
    textRect = text.get_rect()

    textRect.center = (H+((W-H)//2), H//2)
    screen.blit(text,textRect)


def drawBoard(screen):
    colors = [pg.Color(238,238,210), pg.Color(118,150,86)]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)% 2)]
            pg.draw.rect(screen,color,pg.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))

def drawPieces(screen,board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "-":
                screen.blit(IMAGES[piece],pg.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))

def drawName(screen,gs):
    file = ['a','b','c','d','e','f','g','h']
    rank = ['8','7','6','5','4','3','2','1']
    for i in range(DIMENSION):
        font = pg.font.Font("Font/rev's_messy_handwriting.otf", 20)
        green = (20, 20, 20)

        text = font.render(file[i], True, green)

        textRect = text.get_rect()

        textRect.center = (i*SQ_SIZE+10, 8*SQ_SIZE-10)
        screen.blit(text,textRect)
    for i in range(DIMENSION):
        font = pg.font.Font("Font/rev's_messy_handwriting.otf", 20)
        green = (20, 20, 20)

        text = font.render(rank[i], True, green)

        textRect = text.get_rect()

        textRect.center = (10, i*SQ_SIZE+10)
        screen.blit(text,textRect)

def highlight(screen,clicked):
    if clicked!= ():
        r,c = clicked
        s = pg.Surface((SQ_SIZE,SQ_SIZE))
        s.set_alpha(100)

        s.fill(pg.Color((186,202,68)))
        screen.blit(s,(c*SQ_SIZE,r*SQ_SIZE))

def displayConnected(screen,gs):
    font = pg.font.Font('Font/Louis George Cafe.ttf', 25)
    green = (255, 255, 255)
    if gs.isConnected():
        text = "  Connected  "
    else:
        text = "Disconnected"
    text = font.render(text, True, green,(32.5, 38, 38.4))
    textRect = text.get_rect()

    textRect.center = (H+((W-H)//2), H//2+220)
    screen.blit(text,textRect)


def displayTurn(screen,gs):
    font = pg.font.Font('Font/Uniflex_PersonalUseOnly.ttf', 32)
    green = (255, 255, 255)
    if gs.getTurn() == 'b':
        turntext = "Black's Turn"
    else:
        turntext = "white's Turn"
    text = font.render(turntext, True, green,(32.5, 38, 38.4))
    textRect = text.get_rect()

    textRect.center = (H+((W-H)//2), H//7)
    screen.blit(text,textRect)


def displayGameOver(screen,gs):
    print("game over")
    font = pg.font.Font('Font/Uniflex_PersonalUseOnly.ttf', 32)
    green = (0, 255, 0)
    blue = (0, 0, 128)
    if gs.getTurn() =='b':
        text = font.render("WHITE WON!!", True, green, blue)


    else:
        text = font.render("BLACK WON!!", True, green, blue)

    textRect = text.get_rect()

    textRect.center = (H // 2, W // 2)
    screen.blit(text,textRect)


if __name__ == '__main__':
    main()
