import pygame, sys
import time
from random import randint, choice
pygame.init()
class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.moving_speed = 300
		turtle1 = pygame.image.load('graphics//reversed turtle.png')
		turtle2 = pygame.image.load('graphics//turtle.png')
		self.ani = [turtle1, turtle2]
		
		turtledef1 = pygame.image.load('graphics//turtle1def.png')
		turtledef2 = pygame.image.load('graphics//turtle2def.png')
		self.def_ani= [turtledef2, turtledef1]
		
		self.defend = True
		self.index = 0
		self.def_image = self.def_ani[0]
		self.image = self.ani[0]
		
		self.player_pos = pygame.Vector2(400, 330)
		self.rect = self.image.get_rect(midbottom = self.player_pos)
	def player_input(self,dt,aim):
		global SCREEN_WIDTH
		keys = pygame.key.get_pressed()
		if self.rect.left > 0:
			if keys[pygame.K_a]:
				if self.defend == False:
					self.player_pos.x -= self.moving_speed* dt
					self.index = 1
		if self.rect.right<SCREEN_WIDTH:
			if keys[pygame.K_d]:
				if self.defend == False:
					self.player_pos.x += self.moving_speed* dt
					self.index = 0
		#update the player's position
		self.rect = self.image.get_rect(midbottom = self.player_pos)
	def collision(self):
		pass
	def defend_state(self, globaldef):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_SPACE]:
			self.defend = True
		else :
			self.defend = False
		globaldef = self.defend
		return globaldef
	def animation_state(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_a]:
			self.image= self.ani[1]
		if keys[pygame.K_d]:
			self.image= self.ani[0]
		
		if self.defend == True :
			self.image = self.def_ani[self.index]
		else :
			self.image = self.ani[self.index]

			
	def update(self,globaldef):
		self.player_input(dt,aim)
		self.defend_state(globaldef)
		self.animation_state()
		self.collision()

class Enemy1(pygame.sprite.Sprite):
	def __init__(self,type_):
		super().__init__()
		shark1 = pygame.image.load('graphics//weirdshark1.png')
		shark2 = pygame.image.load('graphics//weirdshark2.png')
		shark3 = pygame.image.load('graphics//weirdshark3.png')
		shark4 = pygame.image.load('graphics//weirdshark4.png')
		shark5 = pygame.image.load('graphics//weirdshark5.png')
		if type_ ==0:
			self.type = type_
			self.ani = [shark1, shark2, shark3, shark4, shark5]
			x_pos = 850
		elif type_ ==1:
			shark1 = pygame.transform.flip(shark1, True, False)
			shark2 = pygame.transform.flip(shark2, True, False)
			shark3 = pygame.transform.flip(shark3, True, False)
			shark4 = pygame.transform.flip(shark4, True, False)
			shark5 = pygame.transform.flip(shark5, True, False)
			self.ani=[shark1, shark2, shark3, shark4, shark5]
			x_pos = -50
			self.type=type_
		self.ani_index = 0
		self.image = self.ani[0]
		self.image = pygame.transform.scale(self.image, (128, 64))
		self.rect = self.image.get_rect(midbottom = (x_pos, 320))
	def animation(self):
		self.ani_index += 0.2
		if self.ani_index >= len(self.ani):
			self.ani_index=0
		self.image = self.ani[int(self.ani_index)]
		self.image = pygame.transform.scale(self.image, (128, 64))
	def destroy(self):
		if self.rect.x <= -150 or self.rect.x >=900:
			self.kill()
	def update(self):
		self.animation()
		if self.type == 0:
			self.rect.x -=6
		elif self.type == 1:
			self.rect.x +=6
		self.destroy()
class Enemy2(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		anchor = pygame.image.load('graphics//anchor.png')
		self.image = anchor
		self.image = pygame.transform.scale(self.image, (128,128))
		self.rect = self.image.get_rect(midbottom = (player.sprite.rect.x,randint(-300,-100)))
	def destroy(self):
		if self.rect.y >= 280 :
			self.kill()
	def update(self):
		self.destroy()
		self.rect.y +=5

	
def collision_sprite():
	if pygame.sprite.spritecollide(player.sprite,enemy_group, True):
		if globaldef == True:
			return True
		if globaldef ==False :
			enemy_group.empty()
			dodge_enemy_group.empty()
			return False

	if pygame.sprite.spritecollide(player.sprite,dodge_enemy_group, True):
		enemy_group.empty()
		dodge_enemy_group.empty()
		return False
	else : return True
def display_score():
    current_time = int(pygame.time.get_ticks()/1000) - start_time
    score_surface = test_font.render (f'{current_time}', False,(255,255,255))
    score_rect = score_surface.get_rect(center =(400,50))
    screen.blit(score_surface, score_rect)
    return current_time
SCREEN_WIDTH, SCREEN_HEIGTH = 800,400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGTH))
icon_surface = pygame.image.load('graphics//turtle_icon.png')
pygame.display.set_caption('turtleeee')
pygame.display.set_icon(icon_surface)
clock = pygame.time.Clock()
player = pygame.sprite.GroupSingle()
player.add(Player())
enemy_group = pygame.sprite.Group()
dodge_enemy_group = pygame.sprite.Group()
dt = 0
background = pygame.image.load('graphics//ocean.png')
background = pygame.transform.scale(background,(800,400))
game_active = False
globaldef = False
test_font = pygame.font.Font(None, 50)
gameover_title = test_font.render ('Press SPACE to play again', False, (255,255,255))
gameover_rect = gameover_title.get_rect(center = (400,200))
gameover_turtle = pygame.image.load('graphics//turtleover.png')
gameover_turtle_rect = gameover_turtle.get_rect(center = (400,150))
aim = pygame.Vector2(0,0)
obstacles_timer = pygame.USEREVENT + 1
spawntime = 1500
pygame.time.set_timer(obstacles_timer, 1000)
score = 0
instructions_surface = test_font.render ('Press SPACE to start', False, (255,255,255))
instructions_rect = instructions_surface.get_rect(center=(400, 200))
start_time = 0
while True :
	spawnrate = 2
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if game_active:
			if event.type == obstacles_timer and game_active:
				if randint(0,1)==0:
					dodge_enemy_group.add(Enemy2())
			if event.type == obstacles_timer and game_active:
				if randint(0,1) == 0:
					enemy_group.add(Enemy1(choice([0,1])))
		else :
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					game_active = True
					start_time = int(pygame.time.get_ticks()/1000)
	if game_active == True:
		screen.blit(background, (0,0))
		player.draw(screen)
		player.update(globaldef)
		globaldef = Player().defend_state(globaldef)
		enemy_group.draw(screen)
		enemy_group.update()
		dodge_enemy_group.draw(screen)
		dodge_enemy_group.update()
		game_active = collision_sprite()
		aim = Player().player_input(dt,aim)
		score = display_score()
	else :
		screen.blit(background,(0,0))
		score_message = test_font.render(f' Your score : {score}', False, (255,255,255))
		score_message_rect = score_message.get_rect(center =(400,250))
		if score == 0:
			screen.blit(instructions_surface, instructions_rect)
		else:
			screen.blit(gameover_title,gameover_rect)
			screen.blit(score_message, score_message_rect)
			screen.blit(gameover_turtle,gameover_turtle_rect)
	pygame.display.update()
	dt =clock.tick(60)/1000