# 🚗 Duo Car Challenge

**Duo Car Challenge** is a two-player vertical racing game built with **Python** and **Pygame**. Each player controls a car to race through a scrolling track filled with obstacles. The first player to reach 2000 meters wins!

---

## 🧩 Modular Architecture (STM32-Ready)

The game uses a modular design, making it easy to customize and integrate with external hardware such as **STM32** microcontrollers.

### 🔌 `input_module.py`
- Handles all player input (default: keyboard)
- ✅ Can be extended to receive data from **STM32**, **Bluetooth modules**, or **serial sensors**
- Example: Read angle or throttle values via UART and convert to in-game movement

### 📤 `output_module.py`
- Handles game output events (e.g., collisions, victory)
- ✅ Easily connected to **STM32** or other hardware to trigger feedback:
  - Vibration motors
  - LEDs
  - Buzzers
- Example: Send a UART message like `"P1:HIT\n"` when Player 1 collides

---

## 🕹 Gameplay Overview

- 2 players control cars on a vertically scrolling track
- Dodge enemies while accelerating upward
- Collisions cause temporary stun and screen shake
- First to reach 2000 meters wins

---

## ⌨️ Default Controls

### Player 1 (Red Car)

| Action       | Key     |
|--------------|---------|
| Accelerate   | `W`     |
| Brake        | `E`     |
| Hard Left    | `A` (-180°) |
| Left         | `S` (-90°)  |
| Straight     | `D` (0°)    |
| Right        | `F` (90°)   |
| Hard Right   | `G` (180°)  |

### Player 2 (Blue Car)

| Action       | Key              |
|--------------|------------------|
| Accelerate   | `↑` Arrow key    |
| Brake        | `↓` Arrow key    |
| Hard Left    | `J` (-180°)      |
| Left         | `K` (-90°)       |
| Straight     | `L` (0°)         |
| Right        | `;` (90°)        |
| Hard Right   | `'` (180°)       |

> Each direction key maps to an **angle** (-180° to 180°), which is converted to horizontal speed (`-2` to `2`) inside `input_module.py`.

---

## ⚙️ Speed System

- **Vertical Speed**:
  - 5 levels (0 to 4)
  - Acceleration increases speed level
  - Braking decreases it
  - Faster = higher movement and score gain

- **Horizontal Speed**:
  - Determined by angle input
  - Converted internally to a speed from `-2` to `2`

---

## 🧪 Modular Output Events

Output events are handled in `output_module.py`, making it easy to plug into other systems:

| Event     | Function                     | Example Use Case                        |
|-----------|------------------------------|-----------------------------------------|
| Collision | `handle_collision_output()`  | Send UART signal to STM32 or activate motor |
| Victory   | `handle_victory_output()`    | Flash LED, trigger sound, send score    |

These functions can be extended to log data, transmit over serial, or interface with external hardware.

---

