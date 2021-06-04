import pygame as pg
import pyperclip


pg.init()
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
FONT = pg.font.Font("Font/Louis George Cafe.ttf", 20)


class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.chatId = None
        self.txt_surface = FONT.render(text, True, (255,255,255))
        self.active = False


    def handle_event(self, event):
        ctrl = False
        v = False
        if event.type == pg.MOUSEBUTTONDOWN:

            if self.rect.collidepoint(event.pos):

                self.active = not self.active
            else:
                self.active = False

            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE

        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key== pg.K_p:

                    result = pyperclip.paste()
                    result = result.split('=')
                    if len(result)>=2:

                        self.text = result[1]
                elif event.key == pg.K_RETURN:
                    print(self.text)
                    self.chatId = self.text
                    self.text = ''

                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

                self.txt_surface = FONT.render(self.text, True, (255,255,255))

    def update(self):

        width = max(180, self.txt_surface.get_width()+10)
        self.rect.w = width
    def getText(self):
        return self.chatId
    def draw(self, screen):
        pg.draw.rect(screen, (32.5, 38, 38.4), self.rect)
        pg.draw.rect(screen, self.color, self.rect,2)
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))

