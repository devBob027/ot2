import time, os
from lib import presets

#
# Keyboard
#

'''
A Python class implementing KBHIT, the standard keyboard-interrupt poller.
Works transparently on Windows and Posix (Linux, Mac OS X). Doesn't work
with IDLE.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as 
published by the Free Software Foundation, either version 3 of the 
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

'''

# Windows
if os.name == 'nt':
    import msvcrt

# Posix (Linux, OS X)
else:
    import sys
    import termios
    import atexit
    from select import select


class KBHit:

    def __init__(self):
        '''Creates a KBHit object that you can call to do various keyboard things.
        '''

        if os.name == 'nt':
            pass

        else:

            # Save the terminal settings
            self.fd = sys.stdin.fileno()
            self.new_term = termios.tcgetattr(self.fd)
            self.old_term = termios.tcgetattr(self.fd)

            # New terminal setting unbuffered
            self.new_term[3] = (self.new_term[3] & ~termios.ICANON & ~termios.ECHO)
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)

            # Support normal-terminal reset at exit
            atexit.register(self.set_normal_term)


    def set_normal_term(self):
        ''' Resets to normal terminal.  On Windows this is a no-op.
        '''

        if os.name == 'nt':
            pass

        else:
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)


    def getch(self):
        ''' Returns a keyboard character after kbhit() has been called.
            Should not be called in the same program as getarrow().
        '''

        s = ''

        if os.name == 'nt':
            return msvcrt.getch().decode('utf-8')

        else:
            return sys.stdin.read(1)


    def getarrow(self):
        ''' Returns an arrow-key code after kbhit() has been called. Codes are
        0 : up
        1 : right
        2 : down
        3 : left
        Should not be called in the same program as getch().
        '''

        if os.name == 'nt':
            msvcrt.getch() # skip 0xE0
            c = msvcrt.getch()
            vals = [72, 77, 80, 75]

        else:
            c = sys.stdin.read(3)[2]
            vals = [65, 67, 66, 68]

        return vals.index(ord(c.decode('utf-8')))


    def kbhit(self):
        ''' Returns True if keyboard character was hit, False otherwise.
        '''
        if os.name == 'nt':
            return msvcrt.kbhit()

        else:
            dr,dw,de = select([sys.stdin], [], [], 0)
            return dr != []

#
# Rendering
#
def display(buffer):
    x = ''
    # Yes, this causes X and Y to be switched around. Oh well.
    for i in buffer:
        for i2 in i:
            x = x + i2 + ' '
        x = x + '\n'
    print(x)
    time.sleep(1/presets.FPS)

def clearBuffer(buffer):
    buffer = []
    for i in range(presets.BUFFER_Y):
        buffer.append(['.'] * presets.BUFFER_X)
    return buffer

def squareFill (buffer, start, end, letter):
    buffer = buffer
    for x in range(start[0], end[0]):
        for y in range(start[1], end[1]):
            # The X and Y have to be switched around because of how display() works.
            if y < len(buffer) and x < len(buffer[0]):
                buffer[y][x] = letter
    return buffer

def printText (buffer, start, text):
    x = start[0]
    for l in text:
        if start[1] < len(buffer) and x < len(buffer[0]):
            buffer[start[1]][x] = l
        x = x + 1
    return buffer

def renderImage (buffer, start, image):
    end = (len(image[0]), len(image))
    buffer = buffer
    for x in range(end[0]):
        for y in range(end[1]):
            if y + start[1] < len(buffer) and x + start[0] < len(buffer[0]):
                if image[y][x] != 'ü':
                    buffer[y + start[1]][x + start[0]] = image[y][x]
    return buffer

def importImage (imageRaw):
    image = []
    for i in imageRaw.split('\n'):
        image.append(list(i))
    return image
