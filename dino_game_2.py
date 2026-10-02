import pygame as pg
import numpy as np
import sys
import os

# --- CRUCIAL ANDROID PATH & ENVIRONMENT FIXES ---
# This checks if the game is running inside an Android sandbox or a desktop
IS_ANDROID = "ANDROID_ARGUMENT" in os.environ

if IS_ANDROID:
    # Safely creates the high score file inside the app's private mobile directory
    # (Fixes permission crashes on Android!)
    from android.storage import app_storage_path
    base_dir = app_storage_path()
    hi_file_path = os.path.join(base_dir, 'hi.txt')
else:
    # Uses standard desktop workspace directory path
    hi_file_path = 'hi.txt'

# Pre-initialise high score records safely
hhi = 0
if os.path.exists(hi_file_path):
    with open(hi_file_path, mode='r') as his:
        try:
            hhi = int(his.read().strip())
        except:
            hhi = 0

s = [100, 135, 115, 150, 155, 95, 90]
pg.init()
clock = pg.time.Clock()
dy = 0
dx = 5
g = True
sr = 0
a = 1
tick = 100

# Setup display window sizes mapping dynamically
# On Android, it forces FULLSCREEN to match phone display shapes
if IS_ANDROID:
    screen = pg.display.set_mode((1100, 650), pg.FULLSCREEN)
else:
    screen = pg.display.set_mode((1100, 650))

f = pg.Rect(0, 510, 1100, 1000)
hb = pg.Rect(470, 300, 160, 160)
dino = pg.Rect(180, 440, 65, 100)
c = pg.Rect(1090, 410, 50, 100)

cr = pg.image.load("c.png").convert_alpha()
cs = pg.transform.scale(cr, (50, 100))
pg.display.set_caption("START MENU")
dr = pg.image.load("dino.png").convert_alpha()
ds = pg.transform.scale(dr, (65, 100))

# Fallback safely to standard system sans fonts if device lacks custom ones
z = pg.font.SysFont('playbill', 50)
zz = pg.font.SysFont('elephant', 100)
zzz = pg.font.SysFont('digital-7', 150)
zzzz = pg.font.SysFont('clibri light', 60)

ptp = [(515, 345), (515, 415), (585, 380)]
dg = "DINO GAME"
go = "GAME OVER"
r = "Tap screen to retry" # Swapped text label from 'Press R' to Tap!

def reset():
    global sr, tick, dx, dy, g
    sr = 0
    tick = 100
    dx = 5
    dy = 0
    c.x = 1090
    dino.x = 180
    dino.y = 440

def game():
    global sr, tick, dy, dx, g, hhi, cr, cs
    while True:
        sr += 1
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
                
            # --- TOUCHSCREEN JUMP (Replaces Spacebar!) ---
            # Mouse button 1 tracking registers perfectly as screen taps on mobile
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and g:
                dy = -25
                g = False
                
            # Keyboard support kept for desktop testing
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE and g:
                    dy = -25
                    g = False
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()

        dy += 1
        dino.y += dy
        x = np.random.choice(s)
        screen.fill((27, 191, 254))
        pg.draw.rect(screen, (255, 233, 145), f)
        
        if dino.colliderect(f):
            dino.bottom = f.top
            dy = 0
            g = True
            
        c.x -= dx
        if c.x <= 0:
            c.x = 1090
            c.height = x
            cs = pg.transform.scale(cr, (50, c.height))
            c.bottom = f.top
            
        screen.blit(cs, c)
        
        if dino.colliderect(c):
            dino.right = c.left
            dx = 0
            
        hhhi = "HI-" + str(hhi)
        ss = "Score :  " + str(sr)
        hiscr = z.render(hhhi, True, (255, 255, 255))
        scr = z.render(ss, True, (255, 255, 255))
        screen.blit(scr, (888, 10))
        screen.blit(hiscr, (888, 50))
        
        if dino.bottom == f.top and dino.right == c.left:
            break
            
        screen.blit(ds, dino)
        pg.display.flip()
        clock.tick(tick)
        
        if sr % 500 == 0:
            tick += 5
        sr += 1

    if hhi < sr:
        hhi = sr
        with open(hi_file_path, mode='w') as his:
            his.write(str(hhi))

# --- START MENU LOOP ---
while True:
    if a == 0:
        break
    sscr = zz.render(dg, True, (0, 106, 0))
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
            
        # Tap hidden rectangle or center circle to trigger start
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if hb.collidepoint(event.pos):
                a = 0
                
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            a = 0

    screen.fill((255, 255, 255))
    screen.blit(sscr, (220, 130))
    pg.draw.rect(screen, (255, 255, 255), hb)
    pg.draw.circle(screen, (255, 10, 10), (550, 380), 80)
    pg.draw.polygon(screen, (255, 255, 255), ptp)
    pg.display.flip()

pg.display.set_caption(dg)
game()

# --- GAME OVER / RESTART LOOP ---
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
            
        # --- TOUCHSCREEN RETRY (Replaces 'R' Key!) ---
        # Tapping anywhere on screen will trigger game loop reset
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            reset()
            game()
            
        if event.type == pg.KEYDOWN and event.key == pg.K_r:
            reset()
            game()

    rr = zzzz.render(r, True, (67, 255, 76))
    Go = zzz.render(go, True, (245, 10, 5))
    screen.blit(Go, (300, 250))
    screen.blit(rr, (350, 380))
    pg.display.flip()
