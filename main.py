import pygame
import random
import time
import math

# --- CONFIG ---
BASE_WIDTH, BASE_HEIGHT = 500, 700
pygame.init()
screen = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT))
pygame.display.set_caption("Nadeera Pro Racer - Multi-Platform")

# COLORS
GRAY, WHITE, YELLOW, RED, BLUE, GREEN, BLACK = (50, 50, 50), (255, 255, 255), (255, 255, 0), (255, 0, 0), (0, 0, 255), (0, 255, 0), (0, 0, 0)
GRASS_GREEN = (34, 139, 34)

# FONTS
font = pygame.font.SysFont("Arial", 20, bold=True)
small_font = pygame.font.SysFont("Arial", 14, bold=True)
big_font = pygame.font.SysFont("Arial", 40, bold=True)

# --- VARIABLES ---
player = pygame.Rect(230, 550, 35, 65)
enemies = []
ghost_balls = []
speed = 0
score = 0
game_state = "PYTHON_LOGO"
is_ghost = False
ghost_timer = 0
night_mode = False
road_offset = 0
full_screen = False

TOWNS = {10: "DERANIYAGALA", 20: "AVISSAVELLA", 40: "COLOMBO", 100: "KURUNEGALA"}
current_town_name = ""
town_display_timer = 0

# UI Buttons (Android Style)
btn_acc = pygame.Rect(20, 580, 80, 80)
btn_brk = pygame.Rect(35, 520, 50, 50)
btn_left = pygame.Rect(320, 590, 70, 70)
btn_right = pygame.Rect(410, 590, 70, 70)

def draw_car(surface, rect, color, night, braking):
    pygame.draw.rect(surface, color, rect, border_radius=8)
    pygame.draw.rect(surface, (150, 150, 200), (rect.x+5, rect.y+10, rect.width-10, 15), border_radius=3)
    if night:
        pygame.draw.circle(surface, YELLOW, (rect.x+8, rect.y+5), 4)
        pygame.draw.circle(surface, YELLOW, (rect.x+rect.width-8, rect.y+5), 4)
    if braking:
        pygame.draw.rect(surface, RED, (rect.x+5, rect.y+rect.height-5, 8, 4))
        pygame.draw.rect(surface, RED, (rect.x+rect.width-13, rect.y+rect.height-5, 8, 4))

def draw_speedometer(surface, speed_val):
    center = (BASE_WIDTH - 80, 100) # මීටරය උඩට ගත්තා බටන් නිසා
    pygame.draw.circle(surface, BLACK, center, 65)
    pygame.draw.circle(surface, WHITE, center, 65, 3)
    
    # Numbers
    for i in range(0, 181, 30):
        ang = math.radians(135 + i)
        tx = center[0] + 45 * math.cos(ang)
        ty = center[1] + 45 * math.sin(ang)
        val_txt = small_font.render(str(int(i*0.8)), True, WHITE)
        surface.blit(val_txt, (tx-10, ty-7))

    # Needle
    angle = math.radians(135 + (speed_val * 2.5))
    end_x = center[0] + 55 * math.cos(angle)
    end_y = center[1] + 55 * math.sin(angle)
    pygame.draw.line(surface, RED, center, (end_x, end_y), 3)



def reset_game():
    global score, speed, enemies, ghost_balls, is_ghost, player, current_town_name
    score, speed = 0, 6
    enemies, ghost_balls = [], []
    is_ghost = False
    current_town_name = ""
    player.x, player.y = 230, 550

# --- MAIN LOOP ---
clock = pygame.time.Clock()
logo_start_time = time.time()
run = True
game_surface = pygame.Surface((BASE_WIDTH, BASE_HEIGHT))

while run:
    mouse_pos = pygame.mouse.get_pos()
    if full_screen:
        win_w, win_h = screen.get_size()
        mouse_pos = (mouse_pos[0] * (BASE_WIDTH/win_w), mouse_pos[1] * (BASE_HEIGHT/win_h))

    mouse_click = pygame.mouse.get_pressed()[0]
    mouse_just_clicked = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT: run = False
        if event.type == pygame.MOUSEBUTTONDOWN: mouse_just_clicked = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and game_state == "PLAYING": game_state = "MENU"

    game_surface.fill(BLACK)

    if game_state == "PYTHON_LOGO":
        game_surface.blit(big_font.render("PYTHON PRODUCT", True, YELLOW), (90, 300))
        if time.time() - logo_start_time > 2: game_state = "NADEERA_LOGO"

    elif game_state == "NADEERA_LOGO":
        game_surface.blit(big_font.render("NADEERA GAMING", True, BLUE), (100, 270))
        btn_start = pygame.Rect(150, 350, 200, 50)
        pygame.draw.rect(game_surface, (30,30,30), btn_start)
        game_surface.blit(font.render("CLICK TO START", True, WHITE), (175, 365))
        if mouse_just_clicked and btn_start.collidepoint(mouse_pos): game_state = "MENU"

    elif game_state == "MENU":
        game_surface.fill(GRAY)
        pygame.draw.rect(game_surface, BLACK, (50, 50, 400, 600))
        menu_btns = [("RESUME", 100), ("START GAME", 180), ("SETTINGS", 260), ("SAVE SCORE", 340), ("EXIT", 420)]
        for txt, y in menu_btns:
            r = pygame.Rect(100, y, 300, 50)
            c = (0, 150, 0) if r.collidepoint(mouse_pos) else (0, 80, 0)
            pygame.draw.rect(game_surface, c, r)
            game_surface.blit(font.render(txt, True, WHITE), (180, y+15))
            if mouse_just_clicked and r.collidepoint(mouse_pos):
                if txt == "RESUME" and score > 0: game_state = "PLAYING"
                if txt == "START GAME": reset_game(); game_state = "PLAYING"
                if txt == "SETTINGS": game_state = "SETTINGS"
                if txt == "EXIT": run = False

    elif game_state == "SETTINGS":
        game_surface.fill(GRAY)
        fs_r = pygame.Rect(100, 250, 300, 50)
        bk_r = pygame.Rect(100, 350, 300, 50)
        pygame.draw.rect(game_surface, BLUE, fs_r)
        pygame.draw.rect(game_surface, RED, bk_r)
        game_surface.blit(font.render(f"FULLSCREEN: {'ON' if full_screen else 'OFF'}", True, WHITE), (140, 265))
        game_surface.blit(font.render("BACK", True, WHITE), (220, 365))
        if mouse_just_clicked:
            if fs_r.collidepoint(mouse_pos):
                full_screen = not full_screen
                screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN) if full_screen else pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT))
            if bk_r.collidepoint(mouse_pos): game_state = "MENU"

    elif game_state == "PLAYING":
        game_surface.fill(GRASS_GREEN)
        night_mode = (score // 30) % 2 == 1
        pygame.draw.rect(game_surface, (50,50,50) if not night_mode else (20,20,20), (60, 0, 380, BASE_HEIGHT))
        
        road_offset = (road_offset + speed) % 80
        for lx in [135, 210, 285, 360]:
            for ly in range(-80, BASE_HEIGHT, 80):
                pygame.draw.rect(game_surface, WHITE, (lx, ly + road_offset, 4, 35))

        # --- CONTROLS (Hybrid: Keys + Touch) ---
        keys = pygame.key.get_pressed()
        braking = False
        
        # Steering
        if keys[pygame.K_a] or (mouse_click and btn_left.collidepoint(mouse_pos)): player.x -= 8
        if keys[pygame.K_d] or (mouse_click and btn_right.collidepoint(mouse_pos)): player.x += 8
        
        # Accel / Brake
        if keys[pygame.K_w] or (mouse_click and btn_acc.collidepoint(mouse_pos)): speed = min(speed + 0.05, 18)
        elif keys[pygame.K_s] or (mouse_click and btn_brk.collidepoint(mouse_pos)): speed = max(speed - 0.2, 3); braking = True
        else: speed = max(speed - 0.01, 3)
        
        player.clamp_ip(pygame.Rect(60, 0, 380, BASE_HEIGHT))

        # Draw Touch Controls
        pygame.draw.rect(game_surface, (0, 200, 0, 100), btn_acc, border_radius=10)
        game_surface.blit(small_font.render("GO", True, BLACK), (btn_acc.x+30, btn_acc.y+30))
        pygame.draw.rect(game_surface, (200, 0, 0, 100), btn_brk, border_radius=10)
        game_surface.blit(small_font.render("STOP", True, WHITE), (btn_brk.x+5, btn_brk.y+15))
        
        pygame.draw.circle(game_surface, (100, 100, 100), btn_left.center, 35)
        game_surface.blit(font.render("<", True, WHITE), (btn_left.x+25, btn_left.y+20))
        pygame.draw.circle(game_surface, (100, 100, 100), btn_right.center, 35)
        game_surface.blit(font.render(">", True, WHITE), (btn_right.x+25, btn_right.y+20))

        # Ghost Ball
        if not is_ghost and random.random() < 0.005:
            ghost_balls.append(pygame.Rect(random.randint(80, 400), -50, 25, 25))
        for b in ghost_balls[:]:
            b.y += speed
            pygame.draw.circle(game_surface, GREEN, b.center, 12)
            if player.colliderect(b): is_ghost, ghost_timer = True, time.time() + 10; ghost_balls.remove(b)
        
        if is_ghost:
            rem = int(ghost_timer - time.time())
            if rem <= 0: is_ghost = False
            game_surface.blit(font.render(f"GHOST: {rem}s", True, GREEN), (10, 50))

        # Enemies
        if len(enemies) < 4 and random.random() < 0.02:
            ex = random.choice([75, 150, 225, 300, 375])
            enemies.append({"rect": pygame.Rect(ex, -100, 35, 65), "color": (random.randint(100,255), 50, 50)})
        for e in enemies[:]:
            e["rect"].y += speed + 2 if e["rect"].x > 250 else speed - 2
            if e["rect"].y > BASE_HEIGHT: enemies.remove(e); score += 1
            if player.colliderect(e["rect"]) and not is_ghost: game_state = "MENU"

        draw_car(game_surface, player, BLUE if not is_ghost else (100,100,255), night_mode, braking)
        for e in enemies: draw_car(game_surface, e["rect"], e["color"], night_mode, False)
        
        game_surface.blit(font.render(f"SCORE: {score}", True, WHITE), (10, 10))
        draw_speedometer(game_surface, speed * 6)

    # Rendering
    if full_screen:
        win_w, win_h = screen.get_size()
        screen.blit(pygame.transform.scale(game_surface, (win_w, win_h)), (0, 0))
    else:
        screen.blit(game_surface, (0, 0))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
