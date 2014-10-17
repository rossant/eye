import numpy as np
import pygame
import pygame.camera
import pygame.image
from vispy import app
from vispy import gloo

from eyetracker import EyeTracker

vertex = """
    attribute vec2 position;
    attribute vec2 texcoord;
    varying vec2 v_texcoord;
    void main()
    {
        gl_Position = vec4(position, 0.0, 1.0);
        v_texcoord = texcoord;
    }
"""

fragment = """
    uniform sampler2D texture;
    varying vec2 v_texcoord;
    void main()
    {
        gl_FragColor = texture2D(texture, v_texcoord);
    }
"""

size = 640, 480

class Canvas(app.Canvas):
    def __init__(self):
        app.Canvas.__init__(self, size=size, keys='interactive')
        self.program = gloo.Program(vertex, fragment, count=4)
        self.program['position'] = [(-1, -1), (-1, +1), (+1, -1), (+1, +1)]
        self.program['texcoord'] = [(1, 1), (0, 1), (1, 0), (0, 0)]
        self.program['texture'] = np.zeros(size + (3,)).astype(np.uint8)

        pygame.camera.init()
        cameras = pygame.camera.list_cameras()
        self.webcam = pygame.camera.Camera(cameras[0])
        self.webcam.start()
        self._surf = pygame.Surface(size)

        self.tracker = EyeTracker(size)

        self._timer = app.Timer('auto', connect=self.on_timer, start=True)

    def on_resize(self, event):
        width, height = event.size
        gloo.set_viewport(0, 0, width, height)

    def on_draw(self, event):
        gloo.clear('black')
        img = self.webcam.get_image(self._surf)
        im = pygame.surfarray.pixels3d(img)

        self.tracker.input(im)

        # Display eyes.
        for (x, y, w, h), c in zip(self.tracker.eyes, [0, 255]):
            im[x:x+w,y:y+w,:] = c

        self.program['texture'][...] = im
        self.program.draw('triangle_strip')
        
    def on_timer(self, event):
        self.update()
        
c = Canvas()
c.show()
app.run()
