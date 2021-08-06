#classe que monitora os elementos do jogo, se uma colisão é detectada o gameController é modificada
from math import sqrt, pow

class ColisionMonitor:
    def __init__(self, master, canvas, onCollid, elements = [], obstacles = [], dinosOnScreen = 0):
        self.master = master
        self.canvas = canvas
        # elements that can't crash with blocks
        self.elements = elements #dinos
        self.obstacles = obstacles
        self.onCollid = onCollid
        self.dinosOnScreen = dinosOnScreen
        self.start_id = None
        self.activated = False
        
    def run(self):
        self.activated = True
        self.start()

    def start(self):
        if(self.dinosOnScreen>0 and self.activated):
            self.verify_colisions()
            self.start_id = self.canvas.after(20, self.start)

    def verify_colisions(self):
       
        for i, element in enumerate(self.elements):
            if(element.onScreen):
                for obstacle in self.obstacles:
                    
                    if(obstacle.onScreen and obstacle.canCollid and self.crash(element, obstacle)):
                        element.die()
                    
                    if(self.dinosOnScreen==1):
                        element.best = 2 #2melhor dino

                    if(self.dinosOnScreen==0):
                        element.best = 1 #melhor dino
                        self.stop_all()
                        return True

    def crash(self, element, obstacle):
        el_info = element.getColisionInfo()
        ob_info = obstacle.getColisionInfo()

        distance = sqrt(pow(ob_info['coords']['x'] - el_info['coords']['x'], 2) + pow(ob_info['coords']['y'] - el_info['coords']['y'], 2))

        if(distance<=el_info['radius_x']+ob_info['radius_x'] or distance<=el_info['radius_y']+ob_info['radius_y']):
            for pixel in obstacle.mask:
                if(element.pixelInMask(pixel, obstacle.move_factor)):
                    return True
            return False
            
    def stop_all(self):
        self.activated = False
        if(self.start_id):
            self.canvas.after_cancel(self.start_id)
        for element in self.elements:
            if(element.moving_id):
                self.canvas.after_cancel(element.moving_id)
        for obstacle in self.obstacles:
            if(obstacle.moving_id):
                self.canvas.after_cancel(obstacle.moving_id)
        self.onCollid()