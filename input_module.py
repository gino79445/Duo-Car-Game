import pygame

def angle_to_horiz_speed(angle, levels=5):
    """
    將 angle（-180 ~ 180）分為 levels 段，對應速度值（例如 -2 ~ 2）
    """
    angle = max(-180, min(180, angle))
    shifted_angle = angle + 180  # 轉為 0 ~ 360
    segment = 360 / levels       # 每段角度寬度
    index = int(shifted_angle // segment)
    center = (levels - 1) // 2
    return index - center


PLAYER_KEY_CONFIGS = {
    1: {
        "angle_keys": {
            pygame.K_a: -180,
            pygame.K_s: -90,
            pygame.K_d: 0,
            pygame.K_f: 90,
            pygame.K_g: 180,
        },
        "accelerate": pygame.K_w,
        "brake": pygame.K_e,
    },
    2: {
        "angle_keys": {
            pygame.K_j: -180,
            pygame.K_k: -90,
            pygame.K_l: 0,
            pygame.K_SEMICOLON: 90,
            pygame.K_QUOTE: 180,
        },
        "accelerate": pygame.K_UP,
        "brake": pygame.K_DOWN,
    }
}

def get_player_input(player_id):
    keys = pygame.key.get_pressed()
    config = PLAYER_KEY_CONFIGS.get(player_id)
    if not config:
        return 0, False, False

    angle = 0
    for key, value in config["angle_keys"].items():
        if keys[key]:
            angle = value
            break

    horiz_speed = angle_to_horiz_speed(angle, levels=5)
    accelerate = keys[config["accelerate"]]
    brake = keys[config["brake"]]

    return horiz_speed, accelerate, brake

