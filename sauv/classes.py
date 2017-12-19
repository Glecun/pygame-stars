# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import time

class Vais:
	
	#Permet de creer le vaisseau
	def __init__(self):
		#
		self.image = pygame.image.load("image/vaisseau.png").convert_alpha()
                self.position_vais = self.image.get_rect()
                self.position_vais.center = 500,700
		#Laser
		self.laser = pygame.image.load("image/laser.png").convert_alpha()
                self.position_laser = self.laser.get_rect()
		self.position_laser.center= 1200,70
		self.tire = 0
		self.son_laser = pygame.mixer.Sound("image/laser.wav")

	#Permet de le deplacer
	def deplacer(self,direction):
		#Déplacement vers la droite
                if direction == 'droite':
                        #Pour ne pas dépasser l'écran
                        if self.position_vais.x < 961:
                                        #Déplacement d'une case
                                        self.position_vais = self.position_vais.move(5,0)
                #Déplacement vers la gauche
                if direction == 'gauche':
                        #Pour ne pas dépasser l'écran
                        if self.position_vais.x > 0 :
                                        #Déplacement d'une case
                                        self.position_vais = self.position_vais.move(-5,0)
	#Permet de tirer
	def tirer(self):
		#Quand le vaisseau ne tire pas
		if(self.tire == 0):
			self.son_laser.play()
			self.position_laser = self.position_vais
			self.position_laser = self.position_laser.move(27,0) 
			self.tire = 1
		
		#Avance le laser
		self.position_laser = self.position_laser.move(0,-5)	
		
		#Quand le laser a fini sa course
		if(self.position_laser.y <= 6):
			self.tire = 0
			self.position_laser.center = 1200,70

class Invader:

		def __init__(self,x,y):
			#Invaders
			self.image = pygame.image.load("image/space_invader.png").convert_alpha()
                	self.position_vais = self.image.get_rect()
                	self.position_vais.center = x,y
			#Explosion
			self.exp = pygame.image.load("image/explosion.png").convert_alpha()
                        self.position_exp = self.exp.get_rect()
                        self.position_exp.center = 1300,70
			self.son_explosion = pygame.mixer.Sound("image/explosion.wav")
			self.tla = 1
			self.texp = 0			

		def explose(self,vais,fenetre):
			if(self.texp>=1):
                                self.texp+=1
                        if self.texp>=20:
                                self.position_exp.center = 1300,70
				self.tla=0
			if self.position_vais.colliderect(vais.position_laser):
				self.son_explosion.play()
				self.position_exp.center = self.position_vais.center
				self.texp+=1
				self.position_vais.center=1400,70
			fenetre.blit(self.image, self.position_vais)
			fenetre.blit(self.exp, self.position_exp)

		def update(self,vais,fenetre):
 			if ( self.tla==1 ): 
				self.explose(vais,fenetre)
				

class Invaders:
		def __init__(self,nb,x,y,nbpl):
			self.nb=nb
			self.tab=[]
			for i in range(0,nb):
				self.tab.append(Invader(x+100*(i%nbpl),y+(i/nbpl)*100))

		def update(self,vais,fenetre):
			for i in range(0,self.nb):
				self.tab[i].update(vais,fenetre)


