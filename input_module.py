import pygame

def angle_to_horiz_speed(angle, levels=9):
    """
    將 angle（-360 ~ 360）分為 levels 段，回傳整數速度值（例如 -4 ~ 4）
    """
    angle = max(-360, min(360, angle))
    shifted_angle = angle + 360
    segment = 720 / levels
    index = int(shifted_angle // segment)
    center = (levels - 1) // 2
    return index - center


PLAYER_KEY_CONFIGS = {
    1: {
        "angle_keys": {
            pygame.K_a: -180,
            pygame.K_s: -135,
            pygame.K_d: -90,
            pygame.K_f: -45,
            pygame.K_g: 0,
            pygame.K_h: 45,
            pygame.K_j: 90,
            pygame.K_k: 135,
            pygame.K_l: 180,
        },
        "accelerate": pygame.K_w,
        "brake": pygame.K_e
    },
    2: {
        "angle_keys": {
            pygame.K_q: -180,
            pygame.K_w: -135,
            pygame.K_e: -90,
            pygame.K_r: -45,
            pygame.K_t: 0,
            pygame.K_y: 45,
            pygame.K_u: 90,
            pygame.K_i: 135,
            pygame.K_o: 180,
        },
        "accelerate": pygame.K_UP,
        "brake": pygame.K_DOWN
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

    horiz_speed = angle_to_horiz_speed(angle)
    accelerate = keys[config["accelerate"]]
    brake = keys[config["brake"]]

    return horiz_speed, accelerate, brake

