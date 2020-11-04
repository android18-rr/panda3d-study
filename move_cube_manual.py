import sys

from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import WindowProperties
from panda3d.core import LPoint3, BitMask32

BLACK = (0, 0, 0, 1)
WHITE = (1, 1, 1, 1)
HIGHLIGHT = (0, 1, 1, 1)
PIECEBLACK = (.15, .15, .15, 1)
DELTA = 0.05


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
        self.frame = 0
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

        self.accept('arrow_up', self.up_fn)
        self.accept('arrow_down', self.down_fn)
        self.accept('arrow_left', self.left_fn)
        self.accept('arrow_right', self.right_fn)
        self.accept('f', self.f_fn)
        self.accept('b', self.b_fn)
        self.accept('h', self.h_fn)
        self.accept('p', self.p_fn)
        self.accept('r', self.r_fn)
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
        self.cube.setPos(0, 0, .5)

    def save_image(self):
        prefix = f'./log//move_manual_v1_{self.frame:04}.jpg'
        self.screenshot(prefix, defaultFilename=False)
        self.frame += 1

    def up_fn(self):
        self.cube.setZ(self.cube.getZ()+DELTA)
        self.save_image()

    def down_fn(self):
        self.cube.setZ(self.cube.getZ()-DELTA)
        self.save_image()

    def left_fn(self):
        self.cube.setX(self.cube.getX()-DELTA)
        self.save_image()

    def right_fn(self):
        self.cube.setX(self.cube.getX()+DELTA)
        self.save_image()

    def f_fn(self):
        self.cube.setY(self.cube.getY()-DELTA)
        self.save_image()

    def b_fn(self):
        self.cube.setY(self.cube.getY()+DELTA)
        self.save_image()

    def h_fn(self):
        self.cube.setH(self.cube.getH()+2)
        self.save_image()

    def p_fn(self):
        self.cube.setP(self.cube.getP()+2)
        self.save_image()

    def r_fn(self):
        self.cube.setR(self.cube.getR()+2)
        self.save_image()


if __name__ == '__main__':
    app = MyApp()
    app.run()
