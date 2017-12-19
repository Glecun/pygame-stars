
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import time
import random

class Vais:
	
	#Permet de creer le vaisseau
	def __init__(self):
		self.image = pygame.image.load("image/vaisseau.png").convert_alpha()
                self.position_vais = self.image.get_rect()
                self.position_vais.center = 500,700
		#Explosion
                self.exp = pygame.image.load("image/explosion.png").convert_alpha()
                self.position_exp = self.exp.get_rect()
                self.position_exp.center = 1300,70
                self.son_explosion = pygame.mixer.Sound("image/explosion.wav")
                self.tla = 1
                self.texp = 0
		self.boss = 0
		
	
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

	def explose(self,laserinv,fenetre):
                        #Introduis un temps avant fin de l'explosion
                        if(self.texp>=1):
                                self.texp+=1
                                laserinv.tirer_fin(True)
                        if self.texp>=20:
                                self.position_exp.center = 1300,70
                                self.tla=0
				self.texp=0
                        #Detecte la collision
                        if self.position_vais.colliderect(laserinv.position_laser) or self.boss==1:
                                self.son_explosion.play()
                                self.position_exp.center = self.position_vais.center
                                self.texp+=1
                                self.position_vais.center=1400,70
                        #Affiche l'explosion
                        fenetre.blit(self.image, self.position_vais)
                        fenetre.blit(self.exp, self.position_exp)

	def tirer(self,laser):
		laser.tirer_deb(self.position_vais.x,self.position_vais.y,0)

	def bosstest(self,inv):
		for i in range(0,len(inv.tablaser)):
			if inv.tablaser[i].position_laser.colliderect(self.position_vais):
				self.boss=1
				break
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
		
		#Permet de tirer
		def tirer(self,laserinv):
			laserinv.tirer_deb(self.position_vais.x,self.position_vais.y,1)

		def explose(self,laser,fenetre,score):
			#Introduis un temps avant fin de l'explosion
			if(self.texp>=1):
                                self.texp+=1
				laser.tirer_fin(True)
                        if self.texp>=20:
                                self.position_exp.center = 1300,70
				self.tla=0
				self.texp=0
			#Detecte la collision
			if self.position_vais.colliderect(laser.position_laser):
				self.son_explosion.play()
				self.position_exp.center = self.position_vais.center
				self.texp+=1
				self.position_vais.center=1400,70
				score.plusun()
			#Affiche l'explosion et l'invader
			fenetre.blit(self.image, self.position_vais)
			fenetre.blit(self.exp, self.position_exp)

		#Met à jour les tires et explosions
		def update(self,laser,laserinv,fenetre,score):
 			if ( self.tla==1 ): 
				self.explose(laser,fenetre,score)
			if (random.randint(0,500)==1 and laserinv.tire==0 and self.tla==1):
				self.tirer(laserinv)
		
		def affiche(self,fenetre):
			fenetre.blit(self.image, self.position_vais)
			
				
#La classe reunissant l'ensemble des invaders
class Invaders:
		def __init__(self,nb,x,y,nbpl):
			self.nb=nb
			self.tab=[]
			for i in range(0,nb):
				self.tab.append(Invader(x+100*(i%nbpl),y+(i/nbpl)*100))
		#Appelle l'update de Invader et fait mouvoir le laser
		def update(self,laser,laserinv,fenetre,score):
			laserinv.tirer_fin(False)
		        if laserinv.tire == 1:
               		        laserinv.deplacer()
			for i in range(0,self.nb):
				self.tab[i].update(laser,laserinv,fenetre,score)

		#Renvoi true si tout les invader sont detruis
		def reset(self):
			for i in range(0,self.nb):
				if (self.tab[i].tla == 1):
					return False
			return True
		
		def affiche(self,fenetre):
			for i in range(0,self.nb):
				self.tab[i].affiche(fenetre)

class Laser:
	
		def __init__(self):
			
			self.laser = pygame.image.load("image/laser.png").convert_alpha()
                	self.position_laser = self.laser.get_rect()
			self.position_laser.center= 1300,70
			self.tire = 0
			self.son_laser = pygame.mixer.Sound("image/laser.wav")

		#Initialise le tire quand il va s'effectuer
		def tirer_deb(self,x,y,sens):
			if(self.tire == 0):
				self.son_laser.play()
				self.position_laser.center = x,y
				if sens==0:
					self.position_laser = self.position_laser.move(26.5,0)
				if sens==1:
					self.position_laser = self.position_laser.move(26.5,30)
				self.tire = 1
				self.sens = sens
		#Déplace le laser dans le sens demandé
		def deplacer(self):
			if (self.sens == 0):
				self.position_laser = self.position_laser.move(0,-3)	
			if (self.sens == 1):
				self.position_laser = self.position_laser.move(0,3)	
				
		#Remet le laser quand il a fini sa course ou detruis un vaisseau
		def tirer_fin(self,stop):
			if(self.position_laser.y >= 765 or self.position_laser.y <= 0 or stop==True):
				self.tire = 0
				self.position_laser.center = 1200,70
		def update(self):
			self.tirer_fin(False)
		        if self.tire == 1:
               		        self.deplacer()
		
		def affiche(self,fenetre):
			fenetre.blit(self.laser,self.position_laser)
			
# A faire

class Boss:
	def __init__(self):
		self.boss = pygame.image.load("image/Boss.png").convert_alpha()
		self.position_boss = self.boss.get_rect()
                self.position_boss.center = 500,120
		self.tla=1
		self.tempo=0
		self.sens=1
		#Explosion
		self.exp = pygame.image.load("image/explosion.png").convert_alpha()
                self.position_exp = self.exp.get_rect()
                self.position_exp.center = 1400,70
		self.son_explosion = pygame.mixer.Sound("image/explosion.wav")
		self.texp=0
		self.nbtouch=0
		#Laser	
		self.laser1=Laser()
		self.laser2=Laser()
		self.laser3=Laser()
		self.tablaser=[self.laser1,self.laser2,self.laser3]
	
	def explose(self,fenetre,laser,score):
		#Introduis un temps avant fin de l'explosion
		if(self.texp>=1):
                        self.texp+=1
                if self.texp>=30:
                        self.position_exp.center = 1300,70
			self.tla=0
		#Detecte la collision
		if (self.position_boss.colliderect(laser.position_laser) and self.texp==0):
			#Termine le laser du vaisseau
			laser.tirer_fin(True)
			self.nbtouch+=1
			if self.nbtouch>=30:
				score.score+=5
				self.son_explosion.play()
				self.position_exp.center = self.position_boss.center
				self.texp+=1
				self.position_boss.center=1400,70
		#Affiche l'explosion
		fenetre.blit(self.boss, self.position_boss)
		fenetre.blit(self.exp, self.position_exp)
	
	def tirer(self):
		self.laser1.tirer_deb(self.position_boss.x+40,self.position_boss.y+100,1)
		self.laser2.tirer_deb(self.position_boss.x+92,self.position_boss.y+112,1)
		self.laser3.tirer_deb(self.position_boss.x+137,self.position_boss.y+100,1)

	def deplacer(self):
		if self.position_boss.x<=0:
			self.sens=0
		if self.position_boss.x>=785:
			self.sens=1
		if self.tempo==3:
			if self.sens==1:
				self.position_boss = self.position_boss.move(-1,0)
			if self.sens==0:
				self.position_boss = self.position_boss.move(1,0)
			self.tempo=0
		self.tempo+=1
	
	def update(self,laser,laserinv,fenetre,score):
		self.deplacer()
		for i in range(0,len(self.tablaser)):
			self.tablaser[i].update()
		if self.tla==1:
			self.explose(fenetre,laser,score)
		if random.randint(0,350)==1 and self.tablaser[1].tire==0 and self.tla==1:
			self.tirer()


	def reset(self):
		if self.tla==1:
			return False
		else:
			return True

	def affiche(self,fenetre):
		for i in range(0,len(self.tablaser)):
			self.tablaser[i].affiche(fenetre)
		fenetre.blit(self.boss,(self.position_boss.x,self.position_boss.y))
		fenetre.blit(self.exp,(self.position_exp.x,self.position_exp.y))
#Class du score
class Score:
		def __init__(self):
			self.score=0
			self.myfont = pygame.font.SysFont("monospace", 40)
		
		def plusun(self):
			self.score+=1
		
		def affiche(self,fenetre,temps):
			self.label = self.myfont.render("Score = " + str(self.score), 1, (250,250,250))
			fenetre.blit(self.label, (400, 580))
			pygame.display.flip()
			time.sleep(5)
class GameOver:

		def __init__(self):
			self.image=pygame.image.load("image/game_over.jpg")

		def test(self,vais):
			if (vais.tla==1):
				return False
			else:
				return True
					
		def affiche(self,fenetre):
			fenetre.blit(self.image,(-40,0))
			pygame.display.flip()
