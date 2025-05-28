def handle_collision_output(player):
    player_id = "Player 1" if player.base_color == (200, 0, 0) else "Player 2"
    print(f"[Collision] {player_id} collided! Score: {player.score:.1f}")

def handle_victory_output(player):
    player_id = "Player 1" if player.base_color == (200, 0, 0) else "Player 2"
    print(f"[Victory] {player_id} wins! Final score: {player.score:.1f}")

