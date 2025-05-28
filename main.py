# 完整的 Duo Car Challenge 升級版程式碼請分多段提供

# 導入與初始化
import pygame
import sys
import random
import math
from input_module import get_player_input
from output_module import handle_collision_output, handle_victory_output
from PIL import Image

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
HALF_WIDTH = SCREEN_WIDTH // 2
WORLD_WIDTH = 400
WORLD_HEIGHT = 50000

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Duo Car Challenge")

WHITE = (255, 255, 255)
GRAY = (60, 60, 60)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

car_size = (40, 80)
font = pygame.font.SysFont("arial", 48, bold=True)
small_font = pygame.font.SysFont("arial", 28)
clock = pygame.time.Clock()
car_speed = 5
ENEMY_SCROLL_SPEED = 2
SCORE_TO_WIN = 2000
FINISH_Y = WORLD_HEIGHT - SCORE_TO_WIN * car_speed

car_img1 = pygame.image.load("car/car1.png").convert_alpha()
car_img2 = pygame.image.load("car/car2.png").convert_alpha()

enemy_frames = [
    pygame.transform.scale(pygame.image.load(f"enemy_frames/frame_{i}.png").convert_alpha(), (50, 50))
    for i in range(5)
]

try:
    collision_sound = pygame.mixer.Sound("collision.wav")
    pygame.mixer.music.load("start_theme.mp3")
    pygame.mixer.music.play(-1)
except:
    collision_sound = None

# 星星背景動畫
stars = [[random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), random.randint(1, 3)] for _ in range(100)]
def create_explosion(x, y):
    group = pygame.sprite.Group()
    for _ in range(20):
        p = Particle(x, y)
        p.velocity = [random.uniform(-3.0, 3.0), random.uniform(-3.0, 3.0)]
        p.total_lifetime = 40
        p.lifetime = 40
        p.image.fill((10, random.randint(50, 100), 0))
        group.add(p)
    return group

def update_and_draw_stars(surface):
    for star in stars:
        star[1] += star[2]
        if star[1] > SCREEN_HEIGHT:
            star[0] = random.randint(0, SCREEN_WIDTH)
            star[1] = 0
        pygame.draw.circle(surface, (255, 255, 255), (star[0], star[1]), star[2])

class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        size = random.randint(8, 12)
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (250, random.randint(100, 180), 0), (size // 2, size // 2), size // 2)
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = [random.uniform(-1.0, 1.0), random.uniform(2.0, 4.0)]
        self.lifetime = 30
        self.total_lifetime = 30

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        self.lifetime -= 1
        alpha = max(0, int(255 * (self.lifetime / self.total_lifetime)))
        self.image.set_alpha(alpha)
        if self.lifetime <= 0:
            self.kill()

class ConfettiParticle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.size = random.randint(10, 30)
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        color = random.choice([
            (255, 0, 0), (0, 255, 0), (0, 128, 255),
            (255, 255, 0), (255, 0, 255), (255, 255, 255)
        ])
        center = self.size // 2
        for radius in range(center, 0, -1):
            alpha = int(255 * (radius / center))
            pygame.draw.circle(self.image, color + (alpha,), (center, center), radius)

        self.original_image = self.image.copy()
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = [random.uniform(-1.5, 1.5), random.uniform(0.5, 2.0)]
        self.gravity = 0.05
        self.angle = random.uniform(0, 360)
        self.rotate_speed = random.uniform(-2, 2)
        self.lifetime = 300  # 持續更久

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        self.angle += self.rotate_speed
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()



class Player(pygame.sprite.Sprite):
    def __init__(self, image, keys, start_pos, player_id):
        super().__init__()
        self.original_image = image
        self.image = pygame.transform.scale(image, car_size)
        self.rect = self.image.get_rect(center=start_pos)
        self.player_id = player_id
        self.keys = keys
        self.alive = True
        self.score = 0
        self.flash_timer = 0
        self.stun_timer = 0
        self.shake_offset = 0
        self.shake_time = 0
        self.vert_speed_level = 0.0
        self.horiz_speed_value = 0
        self.max_speed = 4.0
        self.speed_unit = car_speed
        self.last_spawn_y = start_pos[1]
        self.particles = pygame.sprite.Group()

    def handle_api_input(self, horiz_speed, accelerate, brake, enemies):
        if not self.alive or self.stun_timer > 0:
            return
        old_rect = self.rect.copy()
        self.horiz_speed_value = horiz_speed
        if accelerate:
            self.vert_speed_level = min(self.max_speed, self.vert_speed_level + 0.2)
        if brake:
            self.vert_speed_level = max(0.0, self.vert_speed_level - 0.2)

        self.rect.x += self.horiz_speed_value * self.speed_unit
        self.rect.y -= int(self.vert_speed_level * self.speed_unit)
        self.score = (WORLD_HEIGHT - self.rect.y) / self.speed_unit
        self.rect.clamp_ip(pygame.Rect(0, 0, WORLD_WIDTH, WORLD_HEIGHT))

        if accelerate:
            for _ in range(2):
                self.particles.add(Particle(self.rect.centerx, self.rect.bottom))

        if pygame.sprite.spritecollideany(self, enemies):
            self.rect = old_rect
            self.flash_timer = 200
            self.stun_timer = 300
            self.shake_time = 6
            handle_collision_output(self)
            if collision_sound:
                collision_sound.play()
        if pygame.sprite.spritecollideany(self, enemies):
            self.rect = old_rect
            self.flash_timer = 200
            self.stun_timer = 300
            self.shake_time = 6
            handle_collision_output(self)
            if collision_sound:
                collision_sound.play()
            self.particles.add(create_explosion(self.rect.centerx, self.rect.centery))


    def update(self, dt):
        if self.flash_timer > 0:
            self.flash_timer -= dt
        if self.stun_timer > 0:
            self.stun_timer -= dt
        if self.shake_time > 0:
            self.shake_time -= 1
            self.shake_offset = random.choice([-3, 3])
        else:
            self.shake_offset = 0
        self.particles.update()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frames = enemy_frames
        self.frame_index = 0
        self.frame_timer = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=(x + 20, y + 20))

    def update(self):
        self.rect.y += ENEMY_SCROLL_SPEED
        self.frame_timer += 1
        if self.frame_timer >= 5:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]
            self.frame_timer = 0


def create_players():
    p1 = Player(car_img1, None, (WORLD_WIDTH // 2 - 60, WORLD_HEIGHT - 100), "Player 1")
    p2 = Player(car_img2, None, (WORLD_WIDTH // 2 + 60, WORLD_HEIGHT - 100), "Player 2")
    return p1, p2

# 主遊戲執行迴圈與邏輯控制
start_screen = True
running = True
glow_phase = 0

while running:
    restart_game = False

    if start_screen:
        screen.fill(BLACK)
        update_and_draw_stars(screen)

        glow_phase += 1
        glow_alpha = int(128 + 127 * (1 + math.sin(glow_phase * 0.05)) / 2)

        title_surface = font.render("Duo Car Challenge", True, YELLOW)
        title_glow = font.render("Duo Car Challenge", True, RED)

        glow_layer = pygame.Surface(title_surface.get_size(), pygame.SRCALPHA)
        glow_layer.blit(title_glow, (0, 0))
        glow_layer.set_alpha(glow_alpha)
        screen.blit(glow_layer, (SCREEN_WIDTH//2 - title_surface.get_width()//2, 180 - 4))
        screen.blit(title_surface, (SCREEN_WIDTH//2 - title_surface.get_width()//2, 180))

        msg = small_font.render("Press SPACE to Start", True, WHITE)
        screen.blit(msg, (SCREEN_WIDTH//2 - msg.get_width()//2, 260))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                start_screen = False
        continue

    p1, p2 = create_players()
    players = pygame.sprite.Group(p1, p2)
    enemies = pygame.sprite.Group()
    confetti = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group(p1, p2)
    game_started = False
    countdown_start = pygame.time.get_ticks()
    show_winner = False
    winner_text = ""

    while not restart_game:
        dt = clock.tick(60)
        screen.fill(BLACK)
        update_and_draw_stars(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if show_winner and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                restart_game = True

        if not game_started:
            elapsed = (pygame.time.get_ticks() - countdown_start) // 1000
            if elapsed < 3:
                countdown_text = font.render(str(3 - elapsed), True, WHITE)
            elif elapsed == 3:
                countdown_text = font.render("GO!", True, YELLOW)
            else:
                countdown_text = None
                game_started = True
        elif not show_winner:
            angle1, acc1, brake1 = get_player_input(1)
            angle2, acc2, brake2 = get_player_input(2)
            p1.handle_api_input(angle1, acc1, brake1, enemies)
            p2.handle_api_input(angle2, acc2, brake2, enemies)

            for player in [p1, p2]:
                if abs(player.rect.y - player.last_spawn_y) >= 600:
                    for _ in range(random.randint(2, 4)):
                        lane_x = random.randint(0, WORLD_WIDTH - car_size[0])
                        e = Enemy(lane_x, player.rect.y - random.randint(800, 1200))
                        enemies.add(e)
                        all_sprites.add(e)
                    player.last_spawn_y = player.rect.y

            enemies.update()
            p1.update(dt)
            p2.update(dt)

            if p1.rect.y <= FINISH_Y:
                winner_text = f"{p1.player_id} Wins! Press R to Restart"
                handle_victory_output(p1)
                show_winner = True
                for _ in range(300):
                    confetti.add(ConfettiParticle(random.randint(0, SCREEN_WIDTH), -10))

            elif p2.rect.y <= FINISH_Y:
                winner_text = f"{p2.player_id} Wins! Press R to Restart"
                handle_victory_output(p2)
                show_winner = True
                for _ in range(100):
                    confetti.add(ConfettiParticle(random.randint(0, SCREEN_WIDTH), -10))

        for i, player in enumerate([p1, p2]):
            cam_x = player.rect.centerx - HALF_WIDTH // 2
            cam_y = player.rect.centery - SCREEN_HEIGHT // 2
            cam_x = max(0, min(cam_x, WORLD_WIDTH - HALF_WIDTH))
            cam_y = max(0, min(cam_y, WORLD_HEIGHT - SCREEN_HEIGHT))

            view = pygame.Surface((HALF_WIDTH, SCREEN_HEIGHT))
            view.fill((30, 30, 30))
            pygame.draw.rect(view, (100, 100, 100), view.get_rect(), 4)

            base_line_y = player.rect.y % 100
            for y in range(-100, SCREEN_HEIGHT + 100, 100):
                y_pos = y - base_line_y
                pygame.draw.rect(view, YELLOW, (WORLD_WIDTH // 2 - cam_x - 5, y_pos, 10, 40))

            if FINISH_Y >= cam_y and FINISH_Y <= cam_y + SCREEN_HEIGHT:
                for x in range(0, HALF_WIDTH, 20):
                    pygame.draw.rect(view, WHITE if x // 20 % 2 == 0 else RED, (x, FINISH_Y - cam_y, 10, 10))

            for sprite in all_sprites:
                world_pos = sprite.rect.copy()
                screen_pos = pygame.Rect(
                    world_pos.x - cam_x + player.shake_offset,
                    world_pos.y - cam_y,
                    world_pos.width,
                    world_pos.height
                )
                if view.get_rect().colliderect(screen_pos):
                    view.blit(sprite.image, screen_pos)
            for other_player in [p1, p2]:
                for particle in other_player.particles:
                    screen_pos = pygame.Rect(
                        particle.rect.x - cam_x + player.shake_offset,
                        particle.rect.y - cam_y,
                        particle.rect.width,
                        particle.rect.height
                    )
                    if view.get_rect().colliderect(screen_pos):
                        view.blit(particle.image, screen_pos)

            score_text = small_font.render(f"Distance: {player.score:.1f} m", True, WHITE)
            speed_text = small_font.render(f"V-Speed: {player.vert_speed_level:.1f}  H-Speed: {player.horiz_speed_value}", True, WHITE)
            view.blit(score_text, (10, 10))
            view.blit(speed_text, (10, 40))

            if player.flash_timer > 0:
                flash_overlay = pygame.Surface((HALF_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                flash_overlay.fill((255, 50, 50, 100))
                view.blit(flash_overlay, (0, 0))

            screen.blit(view, (i * HALF_WIDTH, 0))

        pygame.draw.line(screen, WHITE, (HALF_WIDTH, 0), (HALF_WIDTH, SCREEN_HEIGHT), 4)

        if not game_started and countdown_text:
            screen.blit(countdown_text, (SCREEN_WIDTH // 2 - countdown_text.get_width() // 2,
                                         SCREEN_HEIGHT // 2 - countdown_text.get_height() // 2))

        if show_winner:
            confetti.update()
            for particle in confetti:
                screen.blit(particle.image, particle.rect)
            text = font.render(winner_text, True, YELLOW)
            glow = font.render(winner_text, True, RED)
            screen.blit(glow, (SCREEN_WIDTH // 2 - text.get_width() // 2 + 2, SCREEN_HEIGHT // 2 - 28))
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 30))
            confetti.add(ConfettiParticle(random.randint(0, SCREEN_WIDTH), -10))


        pygame.display.flip()

