# 🚗 Duo Car Challenge

A two-player racing game built with Python and Pygame. Each player controls a car and races through a vertically scrolling track filled with enemies. The first to reach the finish line wins!

## 🕹 Gameplay

- Supports 2 players on the same keyboard.
- Each player controls their car's speed and direction.
- Colliding with enemies causes temporary flashing and a stun effect.
- The first player to reach 2000 meters wins the game.

## ⌨️ Controls

### Player 1 (Red Car)

| Action     | Keys         |
|------------|--------------|
| Accelerate | `W`          |
| Brake      | `S`          |
| Move Left  | `Z`, `X`     |
| Neutral    | `C`          |
| Move Right | `V`, `B`     |

### Player 2 (Blue Car)

| Action     | Keys             |
|------------|------------------|
| Accelerate | `↑ Arrow`        |
| Brake      | `↓ Arrow`        |
| Move Left  | `J`, `K`         |
| Neutral    | `L`              |
| Move Right | `;`, `'` (quote) |

## ⚙️ 5-Level Vertical Speed System

Each player's vertical speed is controlled through **five levels**, from 0 to 4:

- Pressing the **accelerate key** (`W` for Player 1, `↑` for Player 2) increases vertical speed by 1 level (up to level 4).
- Pressing the **brake key** (`S` or `↓`) decreases speed by 1 level (down to level 0).
- Higher speed levels move the car faster upward and accumulate distance points more quickly.

### 💡 Strategy Tips

- Start slow to get used to steering and avoiding enemies.
- Use higher speed levels to gain distance and race ahead.
- Slow down near dense enemy zones or close to the finish line for better control.

This system adds depth to the gameplay, requiring players to balance speed and safety.

## 🎮 How to Play

- Launch the game and press `SPACE` to start.
- After the game ends, press `R` to restart.

## 📦 Requirements

- Python 3.x
- Pygame library

Install Pygame via pip:

```bash
pip install pygame
