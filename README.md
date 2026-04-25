# Microwave Simulator (Python)

A complete, highly detailed, engineering-grade Microwave Oven Simulator built in Python using Pygame.

This application simulates both the **internal physics** of dielectric heating (particle dynamics and electromagnetic waves) and the detailed **electrical engineering circuitry** (power, heating, protection, and control systems) of a conventional microwave oven.

## Features

### Tab 1: Particle Physics Simulation
*   **Dielectric Heating:** Simulates water molecules (particles) reacting to an oscillating electromagnetic field.
*   **Vectorized Collisions:** N-body elastic collisions prevent particles from overlapping, yielding realistic fluid-like movement.
*   **Live Data Visualizations:** Real-time graphs for Electric Field waveform, Average Temperature vs. Time, and Power Absorption.
*   **Heatmap Overlay:** Visual representation of the temperature distribution inside the cavity (capped at 500°C).

### Tab 2: Sub-Circuit Simulation
*   **4 Isolated Quadrants:** View Power, Heating, Protection, and Control logic in isolation.
*   **Authentic Components:** Simulates realistic details including Thermal Cutouts, Monitor Switch short-circuit logic, Soft-Start limiters, and voltage-doubler networks.
*   **Dynamic Visuals:** Electrons flow procedurally through standard electrical schematic shapes (inductors, capacitors, resistors) along orthogonal wiring paths.

### Tab 3: Main Circuit Schematic
*   **Full System Diagram:** A dense, unified schematic displaying the complete wiring diagram of a conventional microwave oven.
*   **Holistic Simulation:** Traces AC current from the wall through the interlocks, transformer, and into the magnetron.
*   **Thermal Protection:** Includes a dynamic thermal trip system. If temperatures exceed 120°C, the system physically breaks the circuit to prevent a fire.

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/omthedev001/Microwave-Simulator-Python.git
cd Microwave-Simulator-Python

# 2. Set up a virtual environment (Recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

## How to Operate the Simulator

Run the application using:
```bash
python src/main.py
```

### Navigating the UI
The application features a Chrome-like tab bar at the very top of the window. Click on **Simulation**, **Sub-Circuits**, or **Main Circuit** to switch views. The window is fully resizable and will proportionally scale all elements.

### Operating Tab 1: Simulation
1. Look at the right-hand panel for your control sliders.
2. Adjust the **Frequency**, **Amplitude**, and **Power (W)**.
3. Watch the particles respond to the electromagnetic wave. They will begin to jiggle (Brownian motion) and heat up, shifting from Blue (Cold) to White (Hot, up to 500°C).
4. You can increase the **Simulation Speed** to accelerate the heating process.
5. Monitor the real-time graphs on the left to track Power Absorption and Temperature over time.

### Operating Tab 2: Sub-Circuits
1. This tab isolates the 4 main electrical systems of a microwave.
2. **Important:** Only *one* circuit quadrant can be active at a time to prevent UI overlap.
3. Click the **Start** button inside a quadrant to run that specific circuit.
4. **Interactive Testing:**
   - In the **Protection Circuit**, click `Door: CLOSED` to open the door. You will see the interlock switches physically snap open and the current halt immediately.
   - In the **Heating Circuit**, tweak the `Power` slider to see the Magnetron glow intensity change.
   - In the **Control Circuit**, watch the MCU timer count down. Once it hits `00:00`, the relay drops and the buzzer sounds.

### Operating Tab 3: Main Circuit
1. This is the holistic master diagram.
2. At the bottom of the screen, set your desired **Power** and **Timer**.
3. Ensure the **Door** is set to `CLOSED` and the **Temperature** is below `120.0`.
4. Click **Start**.
5. Watch the AC current flow from the mains, through the EMI filters, into the Primary Interlock, down into the Main Relay, and finally into the High-Voltage Transformer and Magnetron.
6. **Thermal Trip Test:** While the circuit is running, drag the **Temperature (°C)** slider past `120.0`. The `Cavity TCO` (Thermal Cutout switch) will instantly trip open, throwing a `THERMAL TRIP!` warning and safely cutting power to the primary transformer.