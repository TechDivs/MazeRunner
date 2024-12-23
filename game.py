import pygame
from sys import exit
from random import randint

def display_score():
    current_time=int(pygame.time.get_ticks()/1000.000)-start_time
    score_surf=font2.render(f"Score: {current_time}",False,"White")
    score_rect=score_surf.get_rect(center=(690,30))
    pygame.draw.rect(screen,"Black",score_rect)
    screen.blit(score_surf,score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x-=6

            if obstacle_rect.bottom==345:
                screen.blit(enemy,obstacle_rect)
            else:
                screen.blit(fly,obstacle_rect)

        obstacle_list=[obstacle for obstacle in obstacle_list if obstacle.x > -100]
        
        return obstacle_list
    
    else: return []

def collisions(player,obstacles):
    if obstacles:
        for obstacles_rect in obstacles:
            if player.colliderect(obstacles_rect): return False
    return True

def player_animate():
    global player,player_index
    player_index+=0.1
    if player_index >= len(player_run): player_index=0
    player=player_run[int(player_index)]

pygame.init()
screen=pygame.display.set_mode((800,400))
pygame.display.set_caption("Pixel Runner")
clock=pygame.time.Clock()
font2=pygame.font.Font(None,50)
game_active=False
start_time=0
score=0
bg=pygame.image.load("Game Code/Graphics/bg.jpg").convert()

enemy1=pygame.image.load("Game Code/Graphics/snail4.png").convert_alpha()
enemy2=pygame.image.load("Game Code/Graphics/snail5.png").convert_alpha()
enemy3=pygame.image.load("Game Code/Graphics/snail6.png").convert_alpha()
enemy_frames=[enemy1,enemy2,enemy3]
enemy_frame_index=0
enemy=enemy_frames[enemy_frame_index]

fly1=pygame.image.load("Game Code/Graphics/fly1.png").convert_alpha()
fly2=pygame.image.load("Game Code/Graphics/fly2.png").convert_alpha()
fly3=pygame.image.load("Game Code/Graphics/fly3.png").convert_alpha()
fly4=pygame.image.load("Game Code/Graphics/fly4.png").convert_alpha()
fly_frames=[fly1,fly2,fly3,fly4]
fly_frame_index=0
fly=fly_frames[fly_frame_index]

obstacle_rect_list=[]

player1=pygame.image.load("Game Code/Graphics/PlayerRun1bg.png").convert_alpha()
player2=pygame.image.load("Game Code/Graphics/PlayersRun2bg.png").convert_alpha()
player3=pygame.image.load("Game Code/Graphics/PlayersRun3bg.png").convert_alpha()
player4=pygame.image.load("Game Code/Graphics/PlayersRun4bg.png").convert_alpha()
player5=pygame.image.load("Game Code/Graphics/PlayersRun5bg.png").convert_alpha()
player6=pygame.image.load("Game Code/Graphics/PlayersRun6bg.png").convert_alpha()
player_run=[player1,player2,player3,player4,player5,player6]
player_index=0
player=player_run[player_index]
player_rect=player.get_rect(midbottom=(100,345))
player_gravity=0

player_stand=pygame.image.load("Game Code/Graphics/PlayerRun1bg.png").convert_alpha()
player_stand=pygame.transform.scale2x(player_stand)
player_stand_rect=player_stand.get_rect(center=(400,200))
game_name=font2.render("Pixel Runner",False,"White")
game_rect=game_name.get_rect(center=(400,50))
game_msg=font2.render("Press Space to Start",False,"White")
game_msg_rect=game_msg.get_rect(center=(400,350))

obstacle_timer=pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

enemy_animation_timer=pygame.USEREVENT + 2
pygame.time.set_timer(enemy_animation_timer,500)

fly_animation_timer=pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer,200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if game_active:
            if (event.type==pygame.MOUSEBUTTONDOWN and player_rect.bottom==345):
                if player_rect.collidepoint(event.pos):
                    player_gravity=-17    

            if (event.type==pygame.KEYDOWN and player_rect.bottom==345):
                if event.key==pygame.K_SPACE:
                    player_gravity=-17

            if(event.type==obstacle_timer and game_active):
                if randint(0,2):
                    obstacle_rect_list.append(enemy.get_rect(midbottom=(randint(900,1100),345)))
                else:
                    obstacle_rect_list.append(fly.get_rect(midbottom=(randint(900,1100),220)))
        
            if(event.type==enemy_animation_timer and game_active):
                enemy_frame_index+=1
                if enemy_frame_index >= len(enemy_frames): enemy_frame_index=0
                enemy=enemy_frames[enemy_frame_index]
        
            if(event.type==fly_animation_timer and game_active):
                fly_frame_index+=1
                if fly_frame_index >= len(fly_frames): fly_frame_index=0
                fly=fly_frames[fly_frame_index]
        
        
        else:
            if(event.type==pygame.KEYDOWN and event.key==pygame.K_SPACE):
                game_active=True
                start_time=int(pygame.time.get_ticks()/1000.000)
    
    if game_active:    
        screen.blit(bg,(0,0))
        #pygame.draw.rect(screen,"Black",score_rect)
        #screen.blit(score_surf,score_rect)
        #player_rect.right+=1
        score=display_score()
        player_gravity+=1
        player_rect.y+=player_gravity
        if player_rect.bottom > 345 : player_rect.bottom=345
        screen.blit(player,player_rect) #sk
        
        player_animate()
        obstacle_rect_list=obstacle_movement(obstacle_rect_list)

        game_active=collisions(player_rect,obstacle_rect_list)
        
    else:
        screen.fill((64,129,162))
        screen.blit(player_stand,player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.bottom=345
        
        score_msg=font2.render(f"Your Score: {score}",False,"White")
        score_msg_rect=score_msg.get_rect(center=(400,330))
        screen.blit(game_name,game_rect)
        if score==0:
            screen.blit(game_msg,game_msg_rect)
        else:
            screen.blit(score_msg,score_msg_rect)
    pygame.display.update()
    clock.tick(60)