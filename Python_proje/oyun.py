import pygame
import random
import os
import button
from pygame import mixer
from spritesheet import SpriteSheet
from dusman import Dusman

mixer.init()
pygame.init()

# oyun penceresi boyutları
ekran_genislik = 400
ekran_yukseklik = 600

# oyun penceresi oluştur
ekran = pygame.display.set_mode((ekran_genislik, ekran_yukseklik))
pygame.display.set_caption('rabby')

# kare hızını ayarla
sure = pygame.time.Clock()
kare_hizi = 60

# müzikler ve sesleri yükle
oyun_muzigi = pygame.mixer.music.load("themesong.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1, 0.5)
jump_fx = pygame.mixer.Sound("jump.mp3")
jump_fx.set_volume(0.5)
öldün_fx = pygame.mixer.Sound("öldün.mp3")
öldün_fx.set_volume(0.5)

# oyun değişkenleri
yercekimi = 1
max_basamak = 12
kaydirmak = 200
kaydir = 0
arkaplan_kaydir = 0
menu=True
oyun_bitis = False
puan = 0
sayaç = 0

if os.path.exists('score.txt'):

    with open('score.txt', 'r') as file:
        yuksek_score = int(file.read())
else:

    yuksek_score = 0

# renkleri tanımla
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PANEL = (130, 90, 180)

# fontları tanımla
font_küçük = pygame.font.SysFont('Arial', 20)
font_büyük = pygame.font.SysFont('Arial', 24)
font_cokbuyuk=pygame.font.SysFont('Arial',75)

# resimleri yükle
karakter_resmi = pygame.image.load("tavanck.png").convert_alpha()
arkaplan_resmi = pygame.image.load("bg1.jpeg").convert_alpha()
basamak_resmi = pygame.image.load("platformcicek2.png").convert_alpha()
dusman_resmi = pygame.image.load("bird.png").convert_alpha()
helikopter = SpriteSheet(dusman_resmi)
#resimleri tanımlama
basla_resmi=pygame.image.load("start.png").convert_alpha()
cikis_resmi=pygame.image.load("exit.png").convert_alpha()


start_button=button.Button(75,300,basla_resmi,0.5)
exit_button=button.Button(145,470,cikis_resmi,0.6)


# ekrana çıktı alma
def çiz_yazı(text, font, text_col, x, y):
    resim = font.render(text, True, text_col)
    ekran.blit(resim, (x, y))


# çizim paneli
def çiz_panel():
    # pygame.draw.rect(ekran,PANEL,(0,0,ekran_genislik,30))
    # pygame.draw.line(ekran,WHITE,(0,30),(ekran_genislik,30),2)
    çiz_yazı('PUAN: ' + str(puan), font_küçük, WHITE, 2, 2)


# arkaplan çizme
def arkaplan_çizimi(arkaplan_kaydir):
    ekran.blit(arkaplan_resmi, (0, 0 + arkaplan_kaydir))
    ekran.blit(arkaplan_resmi, (0, -600 + arkaplan_kaydir))


# oyuncu sınıfı
class Oyuncu():
    def __init__(self, x, y):

        self.image = pygame.transform.scale(karakter_resmi, (50, 50))
        self.genislik = 40
        self.yukseklik = 25
        self.rect = pygame.Rect(0, 0, self.genislik, self.yukseklik)
        self.rect.center = (x, y)
        self.hiz_y = 0
        self.çevir = False

    def hareket(self):
        # değerleri resetle
        delta_x = 0
        delta_y = 0
        kaydir = 0

        # tuş işlemleri
        anahtar = pygame.key.get_pressed()
        if anahtar[pygame.K_a]:
            delta_x = -10
            self.çevir = True

        if anahtar[pygame.K_d]:
            delta_x = 10
            self.çevir = False

        # yer çekimi
        self.hiz_y += yercekimi
        delta_y += self.hiz_y

        # oyuncunun ekrandan çıkmasını engelleme
        if self.rect.left + delta_x < 0:
            delta_x = 0 - self.rect.left
        if self.rect.right + delta_x > ekran_genislik:
            delta_x = ekran_genislik - self.rect.right

        # platformlarla temas
        for basamak in basamak_grubu:
            if basamak.rect.colliderect(self.rect.x, self.rect.y + delta_y, self.genislik, self.yukseklik):
                if self.rect.bottom < basamak.rect.centery:
                    if self.hiz_y > 0:
                        self.rect.bottom = basamak.rect.top
                        delta_y = 0
                        self.hiz_y = -20
                        jump_fx.play()

        # oyuncunun ekranın üst kısmından çıkmasını engelleme
        if self.rect.top <= kaydirmak:
            # eğer karakter zıplıyorsa
            if self.hiz_y < 0:
                kaydir = -delta_y

        # rect'in konumunu güncelleme
        self.rect.x += delta_x
        self.rect.y += delta_y + kaydir

        # güncelleme maskesi
        self.mask = pygame.mask.from_surface(self.image)

        return kaydir
    def oyuncu_ciz():
        ekran.blit(karakter_resmi, (30,15))

    def çiz(self):
        ekran.blit(pygame.transform.flip(self.image, self.çevir, False), (self.rect.x - 12, self.rect.y - 5))

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
    
# platform sınıfı
class Basamak(pygame.sprite.Sprite):
    def __init__(self, x, y, genislik, hareket):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(basamak_resmi, (genislik + 7, 30))
        self.moving = hareket
        self.hareket_merkezi = random.randint(0, 50)
        self.yon = random.choice([-1, 1])
        self.hiz = random.randint(1, 2)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, kaydir):
        # eğer platform hareketliyse hareket etme işlemi
        if self.moving == True:
            self.hareket_merkezi += 1
            self.rect.x += self.yon * self.hiz

        # hareketini tamamladıysa ya da duvara çarptıysa platformun yönünü değiştir
        if self.hareket_merkezi >= 100 or self.rect.left < 0 or self.rect.right > ekran_genislik:
            self.yon *= -1
            self.hareket_merkezi = 0

        # platformun dikey konumunu güncelleme
        self.rect.y += kaydir

        # platformun ekrandan çıkıp çıkmadığını kontrol etme
        if self.rect.top > ekran_yukseklik:
            self.kill()


# oyuncu durumu
zıpla = Oyuncu(ekran_genislik // 2, ekran_yukseklik - 150)

# hareketli grup oluşturma
basamak_grubu = pygame.sprite.Group()
dusman_grubu = pygame.sprite.Group()

# başlangıç platformu oluşturma
basamakk = Basamak(ekran_genislik // 2 - 50, ekran_yukseklik - 50, 100, False)
basamak_grubu.add(basamakk)

# oyun döngüsü
run = True
while run:

    sure.tick(kare_hizi)
    if menu==True and oyun_bitis==False:
        ekran.fill((202,228,241))
        Oyuncu.oyuncu_ciz()
        çiz_yazı('RABBY',font_cokbuyuk,BLACK,100,300)

        if start_button.draw(ekran):
            menu= False

        if exit_button.draw(ekran):
                    run = False

    

    if oyun_bitis == False and menu== False:

        kaydir = zıpla.hareket()

        # arkaplanı çiz
        arkaplan_kaydir += kaydir
        if arkaplan_kaydir >= 600:
            arkaplan_kaydir = 0
        arkaplan_çizimi(arkaplan_kaydir)

        # platform üretme
        if len(basamak_grubu) < max_basamak:
            basamak_genislik = random.randint(40, 60)
            basamak_x = random.randint(0, ekran_genislik - basamak_genislik)
            basamak_y = basamakk.rect.y - random.randint(80, 180)
            basamak_tip = random.randint(1, 2)
            if basamak_tip == 1 and puan > 1000:
                basamak_hareket = True
            else:
                basamak_hareket = False

            basamakk = Basamak(basamak_x, basamak_y, basamak_genislik, basamak_hareket)
            basamak_grubu.add(basamakk)

        # platform güncelle
        basamak_grubu.update(kaydir)

        # düşman üretme
        if len(dusman_grubu) == 0 and puan > 1500:
            dusman = Dusman(ekran_genislik, 100, helikopter, 1.5)
            dusman_grubu.add(dusman)

        # düşman güncelle
        dusman_grubu.update(kaydir, ekran_genislik)

        # skoru güncelle
        if kaydir > 0:
            puan += kaydir

        # en yüksek skoru gösteren çizgi
        pygame.draw.line(ekran, WHITE, (0, puan - yuksek_score + kaydirmak),
                          (ekran_genislik, puan - yuksek_score + kaydirmak), 3)
        çiz_yazı('YÜKSEK SKOR', font_küçük, WHITE, ekran_genislik - 150, puan - yuksek_score + kaydirmak)

        
        # karakteri çizme
        basamak_grubu.draw(ekran)
        dusman_grubu.draw(ekran)
        zıpla.çiz()

        # paneli çizme
        çiz_panel()

        # oyunun sonunu kontrol et
        if zıpla.rect.bottom > ekran_yukseklik:
            oyun_bitis = True
            öldün_fx.play()

        # düşmanlarla çarpışmayı kontrol
        if pygame.sprite.spritecollide(zıpla, dusman_grubu, False):
            if pygame.sprite.spritecollide(zıpla, dusman_grubu, False, pygame.sprite.collide_mask):
                oyun_bitis = True
                öldün_fx.play()

    if menu==False and oyun_bitis== True:
        if sayaç < ekran_genislik:
            sayaç += 5
            for y in range(0, 6, 2):
                pygame.draw.rect(ekran, BLACK, (0, y * 100, sayaç, 100))
                pygame.draw.rect(ekran, BLACK, (ekran_genislik - sayaç, (y + 1) * 100, ekran_genislik, 100))

        else:

            çiz_yazı('OYUN BİTTİ', font_büyük, WHITE, 130, 200)
            çiz_yazı('PUAN: ' + str(puan), font_büyük, WHITE, 130, 250)
            çiz_yazı('TEKRAR OYNAMAK İÇİN SPACE', font_büyük, WHITE, 40, 300)
            çiz_yazı('EN YUKSEK SKOR: ' + str(yuksek_score), font_büyük, WHITE, 2, 2)
            çiz_yazı('MÜZİĞİ KAPAT: M', font_küçük, WHITE, 0, 570)
            # en yüksek skoru güncelle
            if puan > yuksek_score:
                yuksek_score = puan
                with open('score.txt', 'w') as file:
                    file.write(str(yuksek_score))
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                # değerleri resetle
                oyun_bitis = False
                puan = 0
                kaydir = 0
                sayaç = 0
                #arkaplan_resmi = pygame.image.load("deneme-bg3.png").convert_alpha()    
                # zıplamayı yeniden konumlandır
                zıpla.rect.center = (ekran_genislik // 2, ekran_yukseklik - 150)
                # düşmanları resetle
                dusman_grubu.empty()
                # platformları resetle
                basamak_grubu.empty()
                # başlangıç platformunu oluştur
                basamakk = Basamak(ekran_genislik // 2 - 50, ekran_yukseklik - 50, 100, False)
                basamak_grubu.add(basamakk)
            # müziği durdur
            if key[pygame.K_m]:
                pygame.mixer.music.stop()

    # olay işleyicisi
    for olay in pygame.event.get():
        if olay.type == pygame.QUIT:
            # en yüksek skoru güncelle
            if puan > yuksek_score:
                yuksek_score = puan
                with open('score.txt', 'w') as file:
                    file.write(str(yuksek_score))
            run = False

    pygame.display.update()

pygame.quit()