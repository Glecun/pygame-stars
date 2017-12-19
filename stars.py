
import time
import pygame
from pygame.locals import *
from classes import *
# -*- coding: utf-8 -*-

pygame.init()

#Ouverture fenetre Pygame
fenetre = pygame.display.set_mode((1024, 768))
#Titre
pygame.display.set_caption("Stars")
#Possibilite de rester appuye sur la touche
pygame.key.set_repeat(40, 10)
#Volume du son
pygame.mixer.music.set_volume(0.5)

#BOUCLE PRINCIPALE
continuer = 1
while continuer:
	
	#Variable boucle a 1
	continuer_jeu = 1
	continuer_accueil = 1
	quit = 0	

	#Chargement et collage de l'ecran acceuil
	accueil = pygame.image.load("image/background_accueil.jpg").convert()
	fenetre.blit(accueil, (0,0))
	
	#Son de l'ecran d'accueuil
#	pygame.mixer.music.load("image/Soundtrack_accueil.mp3")
#	pygame.mixer.music.queue("image/Soundtrack_accueil.mp3")
#	pygame.mixer.music.play()

	#Rafraichissement
    	pygame.display.flip()
	
	#BOUCLE ACCUEIL
	while continuer_accueil:
		
		#Limitation de vitesse de la boucle
    		pygame.time.Clock().tick(30)

		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_RETURN:
					continuer_accueil = 0
			if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                                continuer_jeu = 0
                                continuer = 0
                                continuer_accueil = 0
                                quit = 1

	#Arret du son de l'accueil
#	pygame.mixer.music..stop()			
	
	if (quit == 0):
		#Chargement et collage de fond du jeu
		fond = pygame.image.load("image/background.jpg").convert()
		fenetre.blit(fond, (0,0))

		#Creation Score
		score=Score()
		
		#Creation Game_over
		gameover=GameOver()
		fini=0
		#Creation du vaisseau
		vais=Vais()
		
		#Creation des Lasers
		laser=Laser()
		laserinv=Laser()
		
		#Creation des Mechants
		inv=Invaders(20,70,20,10)
	#	inv=Boss()
		nbreset=0

		#Son du jeu
       		#pygame.mixer.music.load("image/Soundtrack_jeu.mp3")
       		#pygame.mixer.music.queue("image/Soundtrack_jeu.mp3")
	        #pygame.mixer.music.play()
	

	#BOUCLE JEU
	while continuer_jeu:
		for event in pygame.event.get():   #On parcours la liste de tous les evenements recus
       	 		if event.type == QUIT:     #Si un de ces evenements est de type QUIT
            			continuer = 0      #On arrete la boucle
				continuer_jeu = 0
				quit = 1
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					continuer_jeu=0
					fini=1
            			if event.key == K_RIGHT: #Si "fleche doite"
                			vais.deplacer('droite')
				if event.key == K_LEFT: #Si "fleche gauche"
                			vais.deplacer('gauche')
				if event.key == K_SPACE:
					vais.tirer(laser)
		
		#Vaisseau tire
		laser.tirer_fin(False)
		if laser.tire == 1:
			laser.deplacer()	
		#Vaisseau se fait toucher par boss
		if nbreset==1:
			vais.bosstest(inv)

		#Reset des mechants
		if (inv.reset()):
			if (nbreset==0):
				inv=Boss()
				nbreset=1
			else:
				inv=Invaders(20,70,20,10)
				nbreset=0

		#Re-collage fond
    		fenetre.blit(fond, (0,0))  
		
		#Si le laser touche l'invader
		inv.update(laser,laserinv,fenetre,score)
		vais.explose(laserinv,fenetre)
		#Re-collage laser+vais
    		inv.affiche(fenetre)
		fenetre.blit(laser.laser, laser.position_laser)
    		fenetre.blit(laserinv.laser, laserinv.position_laser)
		fenetre.blit(vais.image, vais.position_vais)
		#Rafraichissement
    		pygame.display.flip()
		#GameOver
		if (gameover.test(vais) or fini==1):
			gameover.affiche(fenetre)
			continuer_jeu = 0
	#Arret du son du jeu
        #pygame.mixer.music.stop()
	if quit == 0:
		score.affiche(fenetre,5)

