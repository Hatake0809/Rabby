import pygame
import button
import oyun

screen_width=400
screen_height=600

screen=pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Menu')

#resimleri tanımlama
basla_resmi=pygame.image.load("start.png").convert_alpha()
cikis_resmi=pygame.image.load("exit.png").convert_alpha()


start_button=button.Button(50,300,basla_resmi,0.5)
exit_button=button.Button(120,470,cikis_resmi,0.6)
    
class Button():
    def __init__(self,x,y,image,scale):
        width=image.get_width()
        height=image.get_height()
        self.image=pygame.transform.scale(image, (int(width*scale),int(height*scale)))
        self.rect=self.image.get_rect()
        self.rect.topleft=(x,y)
        self.clicked = False

    def draw(self,surface):
        
        action=False
        pos=pygame.mouse.get_pos()
        
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked==False:
                self.clicked = True
                action=True

        if pygame.mouse.get_pressed()[0]==0:
            self.clicked=False

        surface.blit(self.image,(self.rect.x,self.rect.y))

        return action

run=True
while run:

    screen.fill((202,228,241))
    

    if start_button.draw(screen):
        print('start')

    if exit_button.draw(screen):
        print('exit')
       # run=False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
