from lib import io, game, presets
import logging, time
# God forgive me for the code I'm about to write.

# Debugging is for cowards.
#logging.basicConfig(filename= f'logs/OT-{int(time.time())}.txt', level=logging.INFO)

buffer = []
buffer = io.clearBuffer(buffer)

g = game.Game()
t = time.time()
kb = io.KBHit()

# Main loop
run = True
while run:
    if kb.kbhit():
        if g.gameStatus == -1:
            match kb.getch():
                case '1':
                    g = game.Game()
                    g.gameStatus = 0 
                case '3':
                    run = False
        else:
            g.gameLogic(kb.getch())
    elif g.gameStatus != -1:
        g.gameLogic(None)

    if g.gameStatus == -1:
        buffer = g.drawMenu(buffer)
    else:
        buffer = g.drawGame(buffer, time.time()-t)
    
    if time.time() - t >= 0.25:
        t = time.time()
    # Rendered last so it's above all
    buffer = io.printText(buffer,(0, 0),'Oregon Trail 2')
    io.display(buffer)

kb.set_normal_term()