import pygame

#button class
class Button():
	def __init__(self, x, y, image, scale = 1,text= ""):
		width = image.get_width()
		height = image.get_height()
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.font = pygame.font.SysFont(None, 48)

		self.clicked = False

	def draw(self, surface):
		action = False
		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button on screen
		surface.blit(self.image, (self.rect.x, self.rect.y))

		return action