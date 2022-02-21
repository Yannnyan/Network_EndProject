import sys

import pygame
import Client


def createButton(x: int, y: int, width: int, height: int, color: (int, int, int)):
    pygame.draw.rect(screen, color, [x, y, width, height])


pygame.init()

screen = pygame.display.set_mode([1000, 500])
# colors
color_button = (0, 200, 0)
color_text = (0, 0, 150)
# sizes
buttonDim = (240, 50)
# margins
marginX = 10 + buttonDim[0]
marginY = 5 + buttonDim[1]
# location buttons
buttonsX = [5, 5 + marginX, 5 + marginX * 2, 5 + marginX * 3]
buttonsY = [5, 5 + marginY]
# fonts and texts
smallFont = pygame.font.SysFont('Corbel', 25)
text_quit = smallFont.render('Start Client', True, color_text)
text_connect = smallFont.render('Connect', True, color_text)
text_disconnect = smallFont.render('Disconnect', True, color_text)
text_download_file = smallFont.render('Download file', True, color_text)
text_clickToWrite = smallFont.render('Click To Write', True, color_text)
text_userText = smallFont.render('',True,color_text)
# userTextBox
userText = ''
active = False

running = True
while running:

    createButton(buttonsX[0], buttonsY[0], buttonDim[0], buttonDim[1], color_button)
    createButton(buttonsX[1], buttonsY[0], buttonDim[0], buttonDim[1], color_button)
    createButton(buttonsX[2], buttonsY[0], buttonDim[0], buttonDim[1], color_button)
    createButton(buttonsX[3], buttonsY[0], buttonDim[0], buttonDim[1], color_button)
    if not active:
        createButton(buttonsX[0], buttonsY[1], buttonDim[0], buttonDim[1], color_button)
    else:
        createButton(buttonsX[0], buttonsY[1], buttonDim[0], buttonDim[1], (155, 155, 155))

    screen.blit(text_quit, (buttonsX[0] + buttonDim[0] / 4, buttonsY[0] + buttonDim[1] / 8))
    screen.blit(text_connect, (buttonsX[1] + buttonDim[0] / 4, buttonsY[0] + buttonDim[1] / 8))
    screen.blit(text_disconnect, (buttonsX[2] + buttonDim[0] / 4, buttonsY[0] + buttonDim[1] / 8))
    screen.blit(text_download_file, (buttonsX[3] + buttonDim[0] / 4, buttonsY[0] + buttonDim[1] / 8))
    if not active:
        screen.blit(text_clickToWrite, (buttonsX[0] + buttonDim[0] / 4, buttonsY[1] + buttonDim[1] / 8))
    else:
        screen.blit(text_userText, (buttonsX[0] + buttonDim[0] / 4, buttonsY[1] + buttonDim[1] / 8))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            # start Client
            if buttonsX[0] <= mouse[0] <= buttonsX[0] + marginX - 10 and buttonsY[0] <= mouse[1] <= buttonsY[0] \
                    + marginY - 10:
                client = Client.Client_()
                print("[Client] started!")
            # connect
            if buttonsX[1] <= mouse[0] <= buttonsX[1] + marginX - 10 and buttonsY[0] <= mouse[1] <= buttonsY[0] \
                    + marginY - 10:
                client.connect()
                print("[Client] connect")
            # disconnect
            if buttonsX[2] <= mouse[0] <= buttonsX[2] + marginX - 10 and buttonsY[0] <= mouse[1] <= buttonsY[0] \
                    + marginY - 10:
                client.disconnect()
                print("[Client] disconnect")
            # download file
            if buttonsX[3] <= mouse[0] <= buttonsX[3] + marginX - 10 and buttonsY[0] <= mouse[1] <= buttonsY[0] \
                    + marginY - 10:
                client.download_file()
                print("[Client] download file")
            # Text Field
            if buttonsX[0] <= mouse[0] <= buttonsX[0] + marginX - 10 and buttonsY[1] <= mouse[1] <= buttonsY[1] \
                    + marginY - 10:
                active = True
            else:
                active = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                userText = userText[:-1]
                text_userText = smallFont.render(userText,True,color_text)
            else:
                userText += event.unicode
                text_userText = smallFont.render(userText, True, color_text)

    pygame.display.update()
