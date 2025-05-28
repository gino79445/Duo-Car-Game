def handle_collision_output(player):
    print(f"[Collision] {player.player_id} collided! Score: {player.score:.1f}")

def handle_victory_output(player):
    print(f"[Victory] {player.player_id} wins! Final score: {player.score:.1f}")
