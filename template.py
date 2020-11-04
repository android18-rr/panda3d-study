import sys
from math import pi, sin, cos

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.gui.OnscreenText import OnscreenText
from pandac.PandaModules import WindowProperties
from pandac.PandaModules import TextNode
from panda3d.core import LineSegs
from panda3d.core import NodePath


class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        # Basic configuration
        self.disableMouse()  # Disable default mouse function
        self.setBackgroundColor(0, 0, 0)
        self.setFrameRateMeter(True)

        # Set Camera
        self.camera.setPos(0, -10, 0)
        # self.camera.setHpr(0, 0, 0)
        self.camera.lookAt(0, 0, 0)

        # Window configuration
        properties = WindowProperties()
        properties.setTitle('Panda3D template')
        properties.setSize(480, 320)
        self.win.requestProperties(properties)

        # Show text (in 2D plane)
        OnscreenText(
            text='ESC: Quit', parent=self.a2dTopLeft, pos=(0.1, -0.1),
            fg=(1, 1, 1, 1), align=TextNode.ALeft, shadow=(0, 0, 0, 0.5),
            scale=0.1)

        # Bind key events
        # keys: 'space', 'enter', 'escape', 'arrow_left/right/up/down', 'a...'.
        self.accept('escape', sys.exit)
        self.accept('a', self.a_fn)
        self.accept('arrow_up', self.up_fn)
        self.accept('arrow_down', self.down_fn)

        # LoadModel
        # XYZ axis
        self.axis = self.loader.loadModel('models/misc/xyzAxis')
        self.axis.reparentTo(self.render)
        self.axis.setScale(0.5, 0.5, 0.5)
        # Ground
        self.g = self.loader.loadModel('models/misc/gridBack')
        self.g.reparentTo(self.render)
        self.g.setPos(0, 0, -3)
        self.g.setScale(10, 10, 10)
        self.g.setColor(1, 1, 0)

        self.cube = self.loader.loadModel('models/misc/rgbCube')
        self.cube.reparentTo(self.render)
        self.cube.setScale(1, 1, 1)
        # self.cube.setColor(1, 0, 0)
        self.cube.setPos(0, 3, 0)
        self.sphere = self.loader.loadModel('models/misc/sphere')
        self.sphere.reparentTo(self.render)
        self.sphere.setScale(1, 1, 1)
        self.sphere.setColor(1, 1, 0)
        self.sphere.setPos(3, 3, 0)

        # Draw lines
        self.lines = LineSegs()
        self.lines.setThickness(5)
        self.lines.setColor(1., 0., 0., 1.)
        self.lines.moveTo(0., 0., 0.)
        self.lines.drawTo(3., 0., 0.)
        self.node = self.lines.create()
        self.np = NodePath(self.node)
        self.np.reparentTo(self.render)

        # Loop event
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")
        # self.taskMgr.add(self.spinCameraTask2, "SpinCameraTask")

    def a_fn(self):
        print('key A is pushed.')
        return

    def up_fn(self):
        self.cube.setZ(self.cube.getZ()+1)

    def down_fn(self):
        self.cube.setZ(self.cube.getZ()-1)

    def spinCameraTask(self, task):
        angleDegrees = task.time * 6.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(10 * sin(angleRadians), -10 * cos(angleRadians), 3)
        self.camera.setHpr(angleDegrees, -10, 0)
        prefix = f'./log//scr_{task.frame:04}.jpg'
        self.screenshot(prefix, defaultFilename=False)
        return Task.cont

    def spinCameraTask2(self, task):
        if task.time < 2.0:
            print(f'{task.time} [s] is passed at {task.frame} frames.')
            prefix = f'./log//scr_{task.frame:04}.jpg',
            self.screenshot(prefix, defaultFilename=False)
            return Task.cont
        else:
            print('Task is finished.')
            return Task.done


if __name__ == '__main__':
    app = MyApp()
    app.run()
