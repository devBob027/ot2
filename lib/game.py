from lib import io, presets
import logging
import random

# DO NOT WRITE CODE LIKE THIS. SPLIT IT UP INTO FILES. THIS IS TRASH
# TODO: fix thiS

class Game:
    def __init__(self): 
        self.gameStatus = -1

        # Party
        self.chars = ['', '', '', '', '']
        self.health = [100, 100, 100, 100, 100]
        self.bodilyHarm = [0, 0, 0, 0, 0]
        self.luck = 0
        # Inventory
        self.oxen = 2
        self.rations = 0
        self.clothes = 0
        self.ammo = 0
        self.parts = 0
        self.money = 16000
        # Other things
        self.pointer = 'placeholder'
        self.distance = 2000
        self.day = 1
        self.animFrame = 0
        self.eventPointer = ''

    def drawMenu(self, buffer):
        buffer = io.clearBuffer(buffer)
        # Logo
        buffer = io.squareFill(
            buffer, 
            (7, 7), 
            (99, 18), 
            '#'
            )
        buffer = io.squareFill(
            buffer, 
            (9, 9), 
            (97, 16), 
            ' '
            )
        logo = io.importImage(presets.oregonTrail)
        buffer = io.renderImage(buffer, (10, 10), logo)
        
        # Text
        buffer = io.printText(buffer, (7, presets.BUFFER_Y - 16), '(1) New game')
        buffer = io.printText(buffer, (7, presets.BUFFER_Y - 15), '(2) Load game [WIP]')
        buffer = io.printText(buffer, (7, presets.BUFFER_Y - 14), '(3) Quit')
        return buffer

    def gameLogic(self, kb):
        match self.gameStatus:
            case 0:
                # This is a bad way of doing things.
                if self.pointer == 'placeholder':
                    self.pointer = 0
                if kb:
                    if kb == '\n': # enter
                        self.pointer = self.pointer + 1
                        if self.pointer == 5:
                            self.gameStatus = 1
                            self.pointer = 2
                    else:
                        self.chars[self.pointer] = self.chars[self.pointer] + kb
            case 1:
                if kb:
                    match kb:
                        case '1':
                            if self.money >= 500:
                                self.oxen += 2
                                self.money -= 500
                        case '2':
                            if self.money >= 200:
                                self.rations += 10
                                self.money -= 200
                        case '3':
                            if self.money >= 50:
                                self.ammo += 20
                                self.money -= 50
                        case '4':
                            if self.money >= 500:
                                self.parts += 1
                                self.money -= 500
                        case '5':
                            if self.money >= 40:
                                self.clothes += 1
                                self.money -= 40
                        case 'G':
                            self.gameStatus = self.pointer
                            self.pointer = 'placeholder'
                        case 'g':
                            self.gameStatus = self.pointer
                            self.pointer = 'placeholder'
            case 2:
                if self.pointer == 'placeholder':
                    self.pointer = 0
                
                if self.pointer != 0:

                    # ----------------------------------#
                    # ALL THE GAME LOGIC SHOULD BE HERE #
                    # ----------------------------------#
                    match self.pointer:
                        case -2: # Game Over
                            if kb:
                                self.gameStatus = -1
                                self.pointer = 0
                        case -1: # Game start
                            if kb:
                                self.pointer = 0
                        case 1:  # Shop 1501-1550
                            if kb:
                                if kb == '1':
                                    self.pointer = 2
                                    self.gameStatus = 1
                                elif kb == '2':
                                    self.pointer = 0
                        case 2:  # Dysentry 1551 - 1600
                            if kb:
                                self.bodilyHarm[self.eventPointer] += 5
                                self.pointer = 0
                        case 3:  # Bandits 1601 - 1650
                            if kb:
                                if kb == '1':
                                    if self.money >= 500:
                                        self.money -= 500
                                        self.pointer = 0
                                elif kb == '2':
                                    r = random.randint(0, 15)
                                    if self.ammo >= r:
                                        self.ammo -= r
                                    else:
                                        self.ammo = 0    
                                        for i in range(5):
                                            self.health[i] - random.randint(0, 25)
                                    r = random.randint(0, 5)
                                    self.health[0] -= r
                                    self.health[1] -= r
                                    self.health[2] -= r
                                    self.health[3] -= r
                                    self.health[4] -= r
                                    r = random.randint(0, 6)
                                    if r > 4:
                                        self.oxen -= r - 4
                                        if self.oxen < 0: self.oxen = 0
                                    self.pointer = 0
                                    self.money += r * 50    
                        case 4:  # Cart breakdown 1651 - 1700
                            if kb == '2':
                                if self.parts > 0:
                                    self.parts -= 1
                                    self.pointer = 0
                            elif kb == '1':
                                # Yeah cart breakdowns do nothing
                                self.pointer = 0
                        case 5:  # River crossing 1701 - 1900
                            if kb == '1':
                                # Yeah, neither does trudging through a river. TODO: add consequences
                                self.pointer = 0
                            elif kb == '2':
                                if self.rations >= 5:
                                    self.rations -= 5
                                    self.pointer = 0
                        case 6:  # Hay fever 1901 - 1980
                            if kb:
                                self.bodilyHarm[self.eventPointer] += 3
                                self.pointer = 0
                        case 7:  # Lost limb 1981 - 2000
                            if kb:
                                self.bodilyHarm[self.eventPointer] += 10
                                self.pointer = 0
                        case 8:  # Death
                            if kb:
                                self.pointer = 0
                        case 9: # Win
                            if kb:
                                self.gameStatus = -1
                                self.pointer = 0
                                # Ironically enough, winning does the same things as loosing TODO: Make winning cooler

    def drawGame(self, buffer, deltatime):
        if self.gameStatus == -1:
            return buffer
        buffer = io.clearBuffer(buffer)
        match self.gameStatus:
            case 0: # Character naming
                # Main box
                buffer = io.squareFill(
                    buffer, 
                    (1, presets.BUFFER_Y - 20), 
                    (presets.BUFFER_X-1, presets.BUFFER_Y - 2), 
                    '#'
                    )
                buffer = io.squareFill(
                    buffer, 
                    (4, presets.BUFFER_Y - 17), 
                    (presets.BUFFER_X - 4, presets.BUFFER_Y - 5), 
                    '.'
                    )
                # Text
                buffer = io.printText(buffer, (6, presets.BUFFER_Y - 15), f'Name the five people in your party. DO NOT USE BACKSPACE    ')
                buffer = io.printText(buffer, (6, presets.BUFFER_Y - 14), f'1:{self.chars[0]}')
                buffer = io.printText(buffer, (6, presets.BUFFER_Y - 13), f'2:{self.chars[1]}')
                buffer = io.printText(buffer, (6, presets.BUFFER_Y - 12), f'3:{self.chars[2]}')
                buffer = io.printText(buffer, (6, presets.BUFFER_Y - 11), f'4:{self.chars[3]}')
                buffer = io.printText(buffer, (6, presets.BUFFER_Y - 10), f'5:{self.chars[4]}')
            case 1: # Buy materials
                # Top Box
                buffer = io.squareFill(
                    buffer, 
                    (1, 3), 
                    (presets.BUFFER_X-1, 30), 
                    '#'
                    )
                buffer = io.squareFill(
                    buffer, 
                    (4, 6), 
                    (presets.BUFFER_X-4, 27), 
                    '.'
                    )
                
                # Bottom box
                buffer = io.squareFill(
                    buffer, 
                    (1, presets.BUFFER_Y - 20), 
                    (presets.BUFFER_X-1, presets.BUFFER_Y - 2), 
                    '#'
                    )
                buffer = io.squareFill(
                    buffer, 
                    (4, presets.BUFFER_Y - 17), 
                    (presets.BUFFER_X - 4, presets.BUFFER_Y - 5), 
                    '.'
                    )

                # Shop text
                buffer = io.printText(buffer, (2, 4), 'Shop')
                buffer = io.printText(buffer, (6, 7), 'Here are the various things you can buy:')

                buffer = io.printText(buffer, (6, 9), 'Oxen. Oxen pull your wagon, you need two to do that but what if they die?. $500 for two')
                buffer = io.printText(buffer, (6, 10), 'Food. People and oxen eat food. People eat one ration a day. $200 per 10 rations.')
                buffer = io.printText(buffer, (6, 11), 'Ammunition. Obvious, $50 per box of 20.')
                buffer = io.printText(buffer, (6, 12), 'Wagon parts. Your wagon might break down. 500$ for one set of parts')
                buffer = io.printText(buffer, (6, 13), 'Clothes. They might get ruined. $40 for one outfit for.')
                buffer = io.printText(buffer, (6, 14), 'Here are the various things you can buy:')
    
                # UI text
                buffer = io.printText(buffer, (6, presets.BUFFER_Y - 16), f'(1) Oxen, 2 [500] You have {self.oxen}')
                buffer = io.printText(buffer, (6, presets.BUFFER_Y - 15), f'(2) Food, 10 [200] You have {self.rations}')
                buffer = io.printText(buffer, (6, presets.BUFFER_Y - 14), f'(3) Ammo, 20 [50] You have {self.ammo}')
                buffer = io.printText(buffer, (6, presets.BUFFER_Y - 13), f'(4) Wagon parts [500] You have {self.parts}')
                buffer = io.printText(buffer, (6, presets.BUFFER_Y - 12), f'(5) Clothes [40] You have {self.clothes}')
                buffer = io.printText(buffer, (6, presets.BUFFER_Y - 7), f'Money: ${self.money} | Go on (G)')
            case 2: # Gameplay
                # Bottom box
                buffer = io.squareFill(
                    buffer, 
                    (1, presets.BUFFER_Y - 20), 
                    (presets.BUFFER_X-1, presets.BUFFER_Y - 2), 
                    '#'
                    )
                buffer = io.squareFill(
                    buffer, 
                    (4, presets.BUFFER_Y - 17), 
                    (presets.BUFFER_X - 4, presets.BUFFER_Y - 5), 
                    '.'
                    )

                # Top box
                buffer = io.squareFill(
                    buffer, 
                    (0, 2), 
                    (presets.BUFFER_X, 10), 
                    '#'
                    )

                # Ahhh logic shouldn't be here, yet here it is!
                if deltatime >= 0.25 and self.pointer == 0:
                    self.animFrame += 1
                    if self.animFrame % 20 == 0:
                        self.day += 1
                        for i in range(0, 5):
                            if self.health[i] > 0:
                                # Hurt
                                if self.bodilyHarm[i] > 0:
                                    self.health[i] -= self.bodilyHarm[i]
                                    self.bodilyHarm[i] -= 1
                                else:
                                    self.health[i] += 1
                                    if self.health[i] > 100:
                                        self.health[i] = 100
                                # Eat
                                if self.rations > 0:
                                    self.rations -= 1
                                else:
                                    self.health[i] -= 15
                                # Die
                                if self.health[i] <= 0:
                                    self.health[i] = 0
                                    self.pointer = 8
                                    self.eventPointer = i
                        # Random events!
                        if self.pointer != 8:
                            r = random.randint(self.luck * 100, 2000)
                            x = random.randint(0, 4)
                            if r > 1980:
                                self.luck = 0
                                self.pointer = 7
                                self.eventPointer = x
                            elif r > 1900:
                                self.luck = 0
                                self.pointer = 6
                                self.eventPointer = x
                            elif r > 1700:
                                self.luck = 0
                                self.pointer = 5
                            elif r > 1650:
                                self.luck = 0
                                self.pointer = 4
                            elif r > 1600:
                                self.luck = 0
                                self.pointer = 3
                            elif r > 1550:
                                self.luck = 0
                                self.pointer = 2
                                self.eventPointer = x
                            elif r > 1500:
                                self.luck = 0
                                self.pointer = 1
                            else:
                                self.luck + 1
                        if self.oxen:
                            self.distance -= 50
                            if self.oxen > 1:
                                self.distance -= 50
                        if (self.health[0] + self.health[1] + self.health[2] + self.health[3] + self.health[4])/5 == 0:
                            self.pointer = -2
                        if self.distance == 0:
                            self.pointer = 9
                buffer = io.squareFill(
                    buffer, 
                    (0, 12), 
                    (presets.BUFFER_X, presets.BUFFER_Y - 26), 
                    ' '
                    )

                # Art
                wagon = io.importImage(presets.wagon)
                wagon2 = io.importImage(presets.wagon2)
                if self.animFrame % 2:
                    buffer = io.renderImage(buffer, ((1, presets.BUFFER_Y - 34)), wagon)
                else:
                    buffer = io.renderImage(buffer, ((1, presets.BUFFER_Y - 34)), wagon2)
                
                sage = io.importImage(presets.sagebrush)
                buffer = io.renderImage(buffer, (presets.BUFFER_X-self.animFrame, presets.BUFFER_Y - 30), sage)
                buffer = io.renderImage(buffer, (presets.BUFFER_X-self.animFrame + 14, presets.BUFFER_Y - 30), sage)
                buffer = io.renderImage(buffer, (presets.BUFFER_X-self.animFrame + 79, presets.BUFFER_Y - 30), sage)
                    
                if self.animFrame == presets.BUFFER_X + 90:
                    self.animFrame = 0
                
                # Info
                buffer = io.printText(buffer, (6, presets.BUFFER_Y - 16), f'You\'re on the move! It\'s day {self.day}')
                buffer = io.printText(buffer, (6, presets.BUFFER_Y - 15), f'Food: {self.rations}')
                buffer = io.printText(buffer, (6, presets.BUFFER_Y - 14), f'Ammo: {self.ammo}')
                buffer = io.printText(buffer, (6, presets.BUFFER_Y - 13), f'Money: {self.money}')
                buffer = io.printText(buffer, (6, presets.BUFFER_Y - 12), f'Avarage health: {(int(self.health[0] + self.health[1] + self.health[2] + self.health[3] + self.health[4])/5)}')
                buffer = io.printText(buffer, (6, presets.BUFFER_Y - 10), f'Distance left: {self.distance} miles')

                # Overlays
                if self.pointer != 0:
                    buffer = io.squareFill(buffer, (int(presets.BUFFER_X/2) - 30, 20), (int(presets.BUFFER_X/2) + 30, 26), '-')
                    match self.pointer:
                        case -2: # Game Over
                            buffer = io.printText(buffer, (int(presets.BUFFER_X/2) - 28, 21), f'Your whole party died, game over.')
                        case -1: # Game start
                            pass
                        case 1:  # Shop 1501-1550
                            buffer = io.printText(buffer, (int(presets.BUFFER_X/2) - 28, 21), f'You come accross a trader. You can:')
                            buffer = io.printText(buffer, (int(presets.BUFFER_X/2) - 28, 22), f'[1] Go in')
                            buffer = io.printText(buffer, (int(presets.BUFFER_X/2) - 28, 23), f'[2] Ignore')
                        case 2:  # Dysentry 1551 - 1600
                            buffer = io.printText(buffer, (int(presets.BUFFER_X/2) - 28, 23), f'{self.chars[self.eventPointer]} has dysentry')
                        case 3:  # Bandits 1601 - 1650
                            buffer = io.printText(buffer, (int(presets.BUFFER_X/2) - 28, 21), f'Bandit\'s have surrounded you! Will you:')
                            buffer = io.printText(buffer, (int(presets.BUFFER_X/2) - 28, 22), f'[1] Give them their money ($500)')
                            buffer = io.printText(buffer, (int(presets.BUFFER_X/2) - 28, 23), f'[2] YOU\'LL NEVER TAKE ME ALIVE!')

                        case 4:  # Cart breakdown 1651 - 1700
                            buffer = io.printText(buffer, (int(presets.BUFFER_X/2) - 28, 21), f'Something broke in the wagon. You will:')
                            buffer = io.printText(buffer, (int(presets.BUFFER_X/2) - 28, 22), f'[1] It\'ll be fine!')
                            buffer = io.printText(buffer, (int(presets.BUFFER_X/2) - 28, 23), f'[2] Ask help from a local (Payment: 5 rations)')

                        case 5:  # River crossing 1701 - 1900
                            buffer = io.printText(buffer, (int(presets.BUFFER_X/2) - 28, 21), f'You find that the only way to continue')
                            buffer = io.printText(buffer, (int(presets.BUFFER_X/2) - 28, 22), f'is to cross a river. Will you:')
                            buffer = io.printText(buffer, (int(presets.BUFFER_X/2) - 28, 23), f'[1] Trudge the river (may have consequences)')
                            buffer = io.printText(buffer, (int(presets.BUFFER_X/2) - 28, 24), f'[2] Ask help from a local (Payment: 5 rations)')
                        case 6:  # Hay fever 1901 - 1980
                            buffer = io.printText(buffer, (int(presets.BUFFER_X/2) - 28, 21), f'{self.chars[self.eventPointer]} has hay fever!')
                        case 7:  # Lost limb 1981 - 2000
                            buffer = io.printText(buffer, (int(presets.BUFFER_X/2) - 28, 21), f'{self.chars[self.eventPointer]} has lost a limb!')
                        case 8:  # Death
                            buffer = io.printText(buffer, (int(presets.BUFFER_X/2) - 28, 21), f'{self.chars[self.eventPointer]} has passed away!')
                        case 9: # Win
                            buffer = io.printText(buffer, (int(presets.BUFFER_X/2) - 28, 21), f'Congrats! You reached Oregon!')
        return buffer
