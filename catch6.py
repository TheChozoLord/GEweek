import pygame, random, simpleGE

""" catch the Cash 6
    multiple coins
"""

class Coin(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("Coin.png")
        self.setSize(25, 25)
        self.reset()
        
    def reset(self):
        self.y = 10
        self.x = random.randint(0, self.screenWidth)
        self.dy = random.randint(3, 8)
        
    def checkBounds(self):
        if self.bottom > self.screenHeight:
            self.reset()

class Charlie(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("MarioRun-1.png")
        self.setSize(50, 50)
        self.position = (320, 400)
        self.moveSpeed = 5
    
    def process(self):
        if self.isKeyPressed(pygame.K_LEFT):
            self.x -= self.moveSpeed
        if self.isKeyPressed(pygame.K_RIGHT):
            self.x += self.moveSpeed        

class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.setImage("white.jpg")
        
        self.sndCoin = simpleGE.Sound("pickupCoin.wav")
        
        self.charlie = Charlie(self)
        self.coins = []
        for i in range(10):
            self.coins.append(Coin(self))
        
        self.sprites = [self.charlie,
                        self.coins]
        
    def process(self):
        for coin in self.coins:
            if self.charlie.collidesWith(coin):
                self.sndCoin.play()
                coin.reset()
    
def main():
    game = Game()
    game.start()
    
if __name__ == "__main__":
    main()

