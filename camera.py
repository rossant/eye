import pygame
import pygame.camera
import pygame.image
import sys
import cv2

import numpy as np
from vispy import app
from vispy import gloo

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


class Canvas(app.Canvas):
    def __init__(self):
        app.Canvas.__init__(self, size=(640, 480), keys='interactive')
        self.program = gloo.Program(vertex, fragment, count=4)
        self.program['position'] = [(-1, -1), (-1, +1), (+1, -1), (+1, +1)]
        self.program['texcoord'] = [(1, 1), (0, 1), (1, 0), (0, 0)]
        self.program['texture'] = np.zeros((640, 480, 3)).astype(np.uint8)

        pygame.camera.init()
        cameras = pygame.camera.list_cameras()
        self.webcam = pygame.camera.Camera(cameras[0])
        self.webcam.start()
        self.face_cascade = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')
        self._surf = pygame.Surface((640, 480))

        self._timer = app.Timer('auto', connect=self.on_timer, start=True)

    def on_resize(self, event):
        width, height = event.size
        gloo.set_viewport(0, 0, width, height)

    def on_draw(self, event):
        gloo.clear('black')
        img = self.webcam.get_image(self._surf)
        im = pygame.surfarray.pixels3d(img)

        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        # print gray.shape
        
        for x, y, w, h in self.face_cascade.detectMultiScale(gray.T, 1.3):
            im[x:x+w,y:y+w,:] = 0

        self.program['texture'][...] = im
        self.program.draw('triangle_strip')
        
    def on_timer(self, event):
        self.update()
        
c = Canvas()
c.show()
app.run()
