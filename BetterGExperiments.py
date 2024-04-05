# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 10:25:48 2024

@author: owen.merrill
"""

import pygame, random, simpleGE, json

class Mario(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.marioRun = []
        self.marioRun.append(pygame.image.load("MarioRun-1.png"))
        self.marioRun.append(pygame.image.load("MarioRun-2.png"))
        self.marioRun.append(pygame.image.load("MarioRun-3.png"))
        self.marioRun.append(pygame.image.load("MarioRun-4.png"))

        self.image = self.marioRun[0]
        self.rect = self.image.get_rect()
        self.frame = 0
        self.hold = 0
        
        self.setSize(50, 75)
        self.position = (320, 400)
        self.moveSpeed = 5
        
    def process(self):
        
        self.image = pygame.image.load("MarioRun-1.png")
        
        if self.isKeyPressed(pygame.K_LEFT):
            self.x -= 5
            self.hold += 1
            if self.hold == 5:
                self.hold = 0
                self.frame += 1
                if self.frame > 3:
                    self.frame = 0
                
            self.image = pygame.transform.flip(self.marioRun[self.frame], 1, 0)
        if self.isKeyPressed(pygame.K_RIGHT):
            self.x += 5
            self.hold += 1
            if self.hold == 5:
                self.hold = 0
                self.frame += 1
                if self.frame > 3:
                    self.frame = 0
                
            self.image = self.marioRun[self.frame]

         

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
            
class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.setImage("white.jpg")
        self.score = 0
        
        self.timer = simpleGE.Timer()
        self.timer.totalTime = 10
        
        self.lblScore = simpleGE.Label()
        self.lblScore.center = (150, 100)
        
        
        self.lblTimeLeft = simpleGE.Label()
        self.lblTimeLeft.center = (500, 100)
        self.lblTimeLeft.text = "10"
        
        self.sndCoin = simpleGE.Sound("pickupCoin.wav")
    
        self.mario = Mario(self)
        self.coins = []
        for i in range(10):
            self.coins.append(Coin(self))
            
        self.sprites = [self.lblTimeLeft,
                        self.lblScore,
                        self.mario,
                        self.coins]
        
    def process(self):
        self.lblTimeLeft.text = f"{self.timer.getTimeLeft():.2f}"
        self.lblScore.text = f"{self.score}"
        
        if self.timer.getTimeLeft() <= 0:
            inFile = open("coinHighScore.json", "r")
            highScore = json.load(inFile)
            inFile.close()
            if self.score > highScore:
               outFile = open("coinHighScore.json", "w")
               json.dump(self.score, outFile, indent=2)
               outFile.close()
            self.stop()
        
        for coin in self.coins:
            if self.mario.collidesWith(coin):
                self.sndCoin.play()
                self.score += 1
                coin.reset()
    
class TitleScreen(simpleGE.Scene):
    def __init__(self, score):
        super().__init__()
        self.setImage("white.jpg")
        
        inFile = open("coinHighScore.json", "r")
        highScore = json.load(inFile)
        inFile.close()
        
        self.response = "P"
        self.highScore = highScore
        
        self.instructions = simpleGE.MultiLabel()
        self.instructions.textLines = [
            "Collect as many coins as you can.",
            "Move with the left and right arrow keys",
            "You have ten seconds",
            "Good Luck"
            ]
        
        self.instructions.center = (320, 240)
        self.instructions.size = (500, 250)
        
        self.prevScore = score
        self.lblLastScore = simpleGE.Label()
        self.lblLastScore.text = f"Last Score: {self.prevScore}"
        self.lblLastScore.center = (320, 400)
        
        self.btnPlay = simpleGE.Button()
        self.btnPlay.text = "Play (up)"
        self.btnPlay.center = (100, 400)
        
        self.btnQuit = simpleGE.Button()
        self.btnQuit.text = "Quit (down)"
        self.btnQuit.center = (550, 400)
        
        self.lblHighScore = simpleGE.Label()
        self.lblHighScore.text = f"High Score: {self.highScore}"
        self.lblHighScore.center = (320, 100)
        
        
        
        self.sprites = [self.instructions,
                        self.lblHighScore,
                        self.lblLastScore,
                        self.btnPlay,
                        self.btnQuit]
                
    def process(self):
        if self.btnQuit.clicked:
            self.response = "Quit"
            self.stop()
        if self.btnPlay.clicked:
            self.response = "Play"
            self.stop()
        if self.isKeyPressed(pygame.K_UP):
            self.response = "Play"
            self.stop()
        if self.isKeyPressed(pygame.K_DOWN):
            self.response = "Quit"
            self.stop()
            

def main():
    keepGoing = True
    score = 0
    while keepGoing:
        instructions = TitleScreen(score)
        instructions.start()
        if instructions.response == "Play":
            game = Game()
            game.start()
            score = game.score
        else:
            keepGoing = False

if __name__ == "__main__":
    main()