import pygame
import pygame_gui
import sys
import os

# Add src to python path for internal imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import *
from ui.ui_controller import UIController
from physics.engine import ParticleEngine
from physics.wave import WaveModel
from render.microwave_view import MicrowaveView
from render.graph_view import GraphView
from render.circuit_view import CircuitView

def main():
    pygame.init()
    pygame.display.set_caption(APP_TITLE)
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    ui_manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT))
    
    # Initialize Core Components
    ui_controller = UIController(ui_manager, WINDOW_WIDTH, WINDOW_HEIGHT)
    
    wave_model = WaveModel(freq=DEFAULT_FREQ_GHZ, amplitude=DEFAULT_AMPLITUDE)
    particle_engine = ParticleEngine(num_particles=DEFAULT_PARTICLE_COUNT)
    
    microwave_view = MicrowaveView(rect=pygame.Rect(300, 60, 680, 640))
    graph_view = GraphView(rect=pygame.Rect(10, 60, 280, 640))
    circuit_view = CircuitView(rect=pygame.Rect(10, 60, 970, 640)) # Full left + center area for circuit

    is_running = True
    while is_running:
        time_delta = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            
            ui_manager.process_events(event)
            ui_controller.handle_event(event)

        # Update UI state
        ui_manager.update(time_delta)
        
        # Get parameters from sliders
        params = ui_controller.get_parameters()
        
        # Update logic based on current tab
        if ui_controller.current_tab == 'simulation':
            wave_model.update(time_delta, params)
            particle_engine.update(time_delta, wave_model, params)
            
        elif ui_controller.current_tab == 'circuit':
            circuit_view.update(time_delta, params)

        # Draw
        screen.fill(COLOR_BG)
        
        if ui_controller.current_tab == 'simulation':
            microwave_view.draw(screen, particle_engine, wave_model)
            graph_view.draw(screen, particle_engine, wave_model)
        elif ui_controller.current_tab == 'circuit':
            circuit_view.draw(screen)

        ui_manager.draw_ui(screen)
        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
