# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 10:12:53 2024

@author: owen.merrill
"""

import pygame, simpleGE

scene = simpleGE.Scene()
scene.setImage ("white.jpg")

mario = simpleGE.Sprite(scene)
mario.setImage("MarioRun-1.png")
mario.setSize(50, 50)
mario.dx = 5
mario.dy = 5

scene.sprites = [mario]
scene.start