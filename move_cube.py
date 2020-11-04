import sys

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from pandac.PandaModules import WindowProperties
from panda3d.core import LPoint3, BitMask32

BLACK = (0, 0, 0, 1)
WHITE = (1, 1, 1, 1)
HIGHLIGHT = (0, 1, 1, 1)
PIECEBLACK = (.15, .15, .15, 1)


def SquarePos(i):
    return LPoint3((i % 8) - 3.5, int(i // 8) - 3.5, 0)


def SquareColor(i):
    if (i + ((i // 8) % 2)) % 2:
        return BLACK
    else:
        return WHITE


class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.disableMouse()  # Disable default mouse function
        self.setBackgroundColor(0, 0, 0)
        self.accept('escape', sys.exit)

        # Set Camera
        self.camera.setPos(0, -8, 1)
        # self.camera.setHpr(0, 0, 0)
        self.camera.lookAt(0, 0, 0)

        # Window configuration
        properties = WindowProperties()
        properties.setTitle('Panda3D template')
        properties.setSize(480, 480)
        self.win.requestProperties(properties)

        # Set checker style ground
        self.squareRoot = self.render.attachNewNode("squareRoot")
        N = 225
        self.squares = [None for i in range(N)]
        for i in range(N):
            # Load, parent, color, and position the model (a single square
            # polygon)
            self.squares[i] = self.loader.loadModel("models/square")
            self.squares[i].reparentTo(self.squareRoot)
            self.squares[i].setPos(SquarePos(i))
            self.squares[i].setColor(SquareColor(i))
            self.squares[i].find("**/polygon").node().setIntoCollideMask(
                BitMask32.bit(1))
            self.squares[i].find("**/polygon").node().setTag('square', str(i))

        # set model
        self.cube = self.loader.loadModel('models/misc/rgbCube')
        self.cube.reparentTo(self.render)
        self.cube.setScale(.5, .5, .5)
        self.cube.setPos(0, 15, .5)
        # Loop event
        self.taskMgr.add(self.move_cube, 'move_cube')

    def move_cube(self, task):
        prefix = f'./log//move_front_v3_{task.frame:04}.jpg'
        self.cube.setY(self.cube.getY() - 0.3)
        self.screenshot(prefix, defaultFilename=False)
        if self.cube.getY() <= -10:
            return Task.done
        else:
            return Task.cont


if __name__ == '__main__':
    app = MyApp()
    app.run()
