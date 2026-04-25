# Microwave Simulator

A complete, fully functional desktop application simulating the internal working of a microwave oven, built with Python, Pygame, and NumPy.

## Features

### Tab 1: Microwave Particle Simulation
*   **Real-time Particle Physics:** Simulates hundreds of water molecules with Brownian motion.
*   **Electromagnetic Wave Interaction:** Particles align and rotate in response to an oscillating electromagnetic field based on frequency and amplitude.
*   **Dynamic Heating Model:** Particles increase in temperature based on absorbed energy and friction, changing color dynamically (Blue -> Red -> White).
*   **Live Data Visualizations:** Real-time graphs for Electric Field waveform, Average Temperature vs. Time, and Power Absorption.
*   **Heatmap Overlay:** Visual representation of the temperature distribution inside the cavity.

### Tab 2: Sub-Circuit Simulation
*   **Detailed Quadrants:** View Power, Heating, Protection, and Control logic in isolation.
*   **Conventional Oven Components:** Simulates realistic details including Thermal Cutouts, Monitor Switch short-circuit logic, and the voltage-doubler network.

### Tab 3: Main Circuit Schematic
*   **Full System Diagram:** A dense, unified schematic displaying the complete wiring diagram.
*   **Holistic Simulation:** Traces AC current from the wall through the interlocks, transformer, and into the magnetron.

## Installation

1. Ensure you have Python 3.8+ installed.
2. Clone this repository or extract the files.
3. Install the dependencies using pip:
   ```bash
   pip install pygame-ce pygame_gui numpy
   ```

## Usage

Run the main application file from the project root:
```bash
python src/main.py
```

### Controls (Right Panel)
*   **Frequency:** Adjust the wave frequency. Higher frequencies create shorter wavelengths.
*   **Amplitude:** Adjust the strength of the electric field.
*   **Power (W):** Adjust the magnetron output power, directly affecting the heating rate.
*   **Simulation Speed:** Speed up or slow down the physics simulation and circuit animation.
*   **Particle Density:** Increase or decrease the number of simulated molecules (water/food).

## Technical Details

The simulation uses `numpy` arrays for fast vectorized updates of particle positions, velocities, dipole angles, and temperatures. This allows running thousands of particles smoothly on the CPU. The wave is modeled as a 1D standing sine wave interacting with the 2D particles' dipole moments.