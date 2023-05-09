import pygame

class SpriteSheet():
    def __init__(self,image):
        self.sheet=image

    def get_image(self,frame,genislik,yukseklik,scale,renk):
        image=pygame.Surface((genislik,yukseklik)).convert_alpha()
        image.blit(self.sheet,(0,0),((frame*genislik),0,genislik,yukseklik))
        image=pygame.transform.scale(image,(int(genislik*scale),int(yukseklik*scale)))
        image.set_colorkey(renk)

        return image
        
  
