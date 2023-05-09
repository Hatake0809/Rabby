import pygame
import random


class Uzaylı(pygame.sprite.Sprite):
    def __init__(self, ekran_genislik, y, sprite_sheet, scale):
        pygame.sprite.Sprite.__init__(self)

        self.animasyon_listesi = []
        self.cerceve_index = 0
        self.update_süre = pygame.time.get_ticks()

        self.yon = random.choice([-1, 1])

        if self.yon == 1:
            self.cevirmek = True

        else:
            self.cevirmek = False

        animasyon_adimlari = 8
        for animasyon in range(animasyon_adimlari):
            image = sprite_sheet.get_image(animasyon, 44, 44, scale, (0, 0, 0))
            image = pygame.transform.flip(image, self.cevirmek, False)
            image.set_colorkey((0, 0, 0))
            self.animasyon_listesi.append(image)

        self.image = self.animasyon_listesi[self.cerceve_index]
        self.rect = self.image.get_rect()

        if self.yon == 1:

            self.rect.x = 0
        else:
            self.rect.x = ekran_genislik
        self.rect.y = y

    def update(self, kaydir, ekran_genislik):

        animasyon_bekleme = 50
        self.image = self.animasyon_listesi[self.cerceve_index]

        if pygame.time.get_ticks() - self.update_süre > animasyon_bekleme:
            self.update_süre = pygame.time.get_ticks()
            self.cerceve_index += 1

        if self.cerceve_index >= len(self.animasyon_listesi):
            self.cerceve_index = 0

        self.rect.x += self.yon * 2
        self.rect.y += kaydir

        if self.rect.right < 0 or self.rect.left > ekran_genislik:
            self.kill()


