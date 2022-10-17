import pygame as pg
import moderngl as mgl
import sys

from model import *
from scene import Scene
from camera import Camera
from textures import TextureManager

class Color :
    def __init__(self, rgb) -> None:
        self.r = rgb[0]
        self.g = rgb[1]
        self.b = rgb[2]
    
    def normalize(self) :
        return (self.r/255, self.g/255, self.b/255)

class GraphicsEngine :
    def __init__(self, windowSize=(1600, 900), maxFramerate=60) :
        pg.init()
        self.windowSize = windowSize

        self.maxFramerate = maxFramerate

        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)

        pg.display.set_mode(self.windowSize, flags=pg.OPENGL | pg.DOUBLEBUF | pg.RESIZABLE)

        #Mouse lock
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)

        #Detect and use existing OpenGL context
        self.ctx = mgl.create_context()
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE)

        #Clock and time
        self.clock = pg.time.Clock()
        self.time = 0
        self.deltaTime = 0

        #Camera
        self.camera = Camera(self)

        #Texture manager
        self.textureMan = TextureManager(self)

        #Scene
        self.scene = Scene(self)

    def check_events(self) :
        for e in pg.event.get() :
            if e.type == pg.QUIT or (e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE) :
                self.scene.destroy()
                pg.quit()
                sys.exit(0)
    
    def render(self) :
        #Clear framebuffer
        self.ctx.clear(color=(Color((42, 42, 42)).normalize()))

        #Render the scene
        self.scene.render()

        #Swap buffers
        pg.display.flip()
    
    def getTime(self) :
        self.time = pg.time.get_ticks() / 1000
    
    def run(self) :
        while True :
            self.getTime()
            self.check_events()
            self.camera.update()
            self.render()
            self.deltaTime = self.clock.tick(self.maxFramerate)

if __name__ == "__main__" :
    app = GraphicsEngine()
    app.run()