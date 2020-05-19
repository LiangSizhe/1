import pygame
from pygame.locals import *
from sys import exit

img_size = iwidth, iheight = 680, 680
back_ground_size = bwidth, bheight = iwidth+0, iheight+50
WHITE = (255, 255, 255)
GRAY = (234, 234, 234)
BLACK = (0, 0, 0)
bg_color = WHITE
prompt_color = BLACK
colorkey = (0, 0, 6)

pygame.init()
pygame.mixer.init()
pygame.font.init()
screen = pygame.display.set_mode(back_ground_size) # , FULLSCREEN)
pygame.display.set_caption("test")

bad_sound = pygame.mixer.Sound('bad.wav')
bad_sound.set_volume(0.2)
good_sound = pygame.mixer.Sound('good.wav')
good_sound.set_volume(0.2)

bad = pygame.image.load("bad.png").convert()
bad = pygame.transform.smoothscale(bad, img_size)
good = pygame.image.load("good.png").convert()
good = pygame.transform.smoothscale(good, img_size)
start = pygame.image.load("start.png").convert()
start = pygame.transform.smoothscale(start, img_size)
f = False

prompt_text = "not selected"
text_font = pygame.font.SysFont('arial', 36)


def paste(src, cx, cy, radius):
    left = 0 if cx - radius < 0 else cx - radius
    right = iwidth if cx + radius > iwidth else cx + radius
    bottom = 0 if cy - radius < 0 else cy - radius
    top = iheight if cy + radius > iheight else cy + radius

    surf = pygame.Surface((right-left, top-bottom))
    surf.fill(colorkey)
    surf.set_colorkey(colorkey)
    surf.set_alpha(184)

    for j in range(bottom, top):
        for i in range(left, right):
            dis = ((cx-i)*(cx-i)+(cy-j)*(cy-j)) ** 0.5
            pixel = src.get_at((i, j))

            if dis < radius:
                degree = dis/radius/2
                pixel = int(pixel[0]+bg_color[0]*degree), int(pixel[1]+bg_color[1]*degree), \
                    int(pixel[2]+bg_color[2]*degree)
                pixel = list(pixel)
                pixel[0] = 255 if pixel[0] > 255 else pixel[0]
                pixel[1] = 255 if pixel[1] > 255 else pixel[1]
                pixel[2] = 255 if pixel[2] > 255 else pixel[2]
                surf.set_at((i - left, j - bottom), pixel)

    rect = surf.get_rect()
    rect.left, rect.top = left, bottom
    screen.blit(surf, rect)


def draw_prompt(key_down):
    pygame.draw.rect(screen, GRAY, (0, iheight, iwidth, bheight-iheight), 0)
    if prompt_text and key_down:
        prompt_suf = text_font.render(str(prompt_text), 1, prompt_color)
        prompt_rect = prompt_suf.get_rect()
        prompt_rect.top = iheight
        prompt_rect.left = 10
        screen.blit(prompt_suf, prompt_rect)

    prompt_suf = text_font.render("press s to restart", 1, prompt_color)
    prompt_rect = prompt_suf.get_rect()
    prompt_rect.top = iheight
    prompt_rect.left = 450
    screen.blit(prompt_suf, prompt_rect)


def restart():
    global screen, start, f
    pygame.draw.rect(screen, WHITE, (0, 0, iwidth, iheight), 0)
    start = pygame.image.load("start.png").convert()
    start = pygame.transform.smoothscale(start, img_size)
    f = False


def main():
    global prompt_text, start, f
    screen.fill(bg_color)
    click_pos = None
    img = None
    key_down = False
    key_up = False
    sound = None
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == MOUSEBUTTONDOWN and img:
                click_pos = event.pos

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    exit()

                elif event.key == K_a:
                    img = bad
                    sound = bad_sound
                    prompt_text = "black chess"
                    key_down = True
                    key_up = False
                    if start:
                        f = True
                    start = None
                elif event.key == K_d:
                    img = good
                    sound = good_sound
                    prompt_text = "white chess"
                    key_down = True
                    key_up = False
                    if start:
                        f = True
                    start = None
                elif event.key == K_s:
                    restart()
                else:
                    img = None
                    prompt_text = ""

            elif event.type == KEYUP:
                key_down = False
                key_up = True

        if start:
            screen.blit(start, start.get_rect())
        if f:
            screen.fill(bg_color)
            f = False
        if click_pos and img and key_down and not key_up:
            paste(img, click_pos[0], click_pos[1], iwidth//6)
            sound.play()
        click_pos = None

        draw_prompt(key_down)
        pygame.display.flip()
        pygame.time.delay(30)


if __name__ == "__main__":
    main()
