import pygame
import pygame_gui
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import *
from ui.ui_controller import UIController
from physics.engine import ParticleEngine
from physics.wave import WaveModel
from render.microwave_view import MicrowaveView
from render.graph_view import GraphView
from render.circuit.circuit_manager import CircuitManager
from render.circuit.main_circuit import MainCircuit

def main():
    pygame.init()
    pygame.display.set_caption(APP_TITLE)
    screen = pygame.display.set_mode((DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT), pygame.RESIZABLE)
    clock = pygame.time.Clock()

    ui_manager = pygame_gui.UIManager((DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT))
    
    ui_controller = UIController(ui_manager, DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT)
    
    wave_model = WaveModel(freq=DEFAULT_FREQ_GHZ, amplitude=DEFAULT_AMPLITUDE)
    particle_engine = ParticleEngine(num_particles=DEFAULT_PARTICLE_COUNT)
    
    microwave_view = MicrowaveView(pygame.Rect(0, 0, 0, 0))
    graph_view = GraphView(pygame.Rect(0, 0, 0, 0))
    circuit_manager = CircuitManager(pygame.Rect(0, 0, 0, 0), ui_manager)
    main_circuit = MainCircuit(ui_manager, "Full Microwave Schematic")

    def handle_resize(w, h):
        w = max(w, MIN_WINDOW_WIDTH)
        h = max(h, MIN_WINDOW_HEIGHT)
        pygame.display.set_mode((w, h), pygame.RESIZABLE)
        ui_manager.set_window_resolution((w, h))
        ui_controller.handle_resize(w, h)
        
        tab_h = 40
        right_panel_w = 280
        left_panel_w = max(250, int(w * 0.25))
        center_w = w - left_panel_w - right_panel_w - 30
        
        graph_view.rect = pygame.Rect(10, tab_h + 10, left_panel_w, h - tab_h - 20)
        microwave_view.rect = pygame.Rect(left_panel_w + 20, tab_h + 10, center_w, h - tab_h - 20)
        particle_engine.set_bounds(microwave_view.rect)
        
        circuit_manager.handle_resize(pygame.Rect(10, tab_h + 10, w - 20, h - tab_h - 20))
        main_circuit.set_bounds(pygame.Rect(10, tab_h + 10, w - 20, h - tab_h - 20))

    # Initial sizing
    handle_resize(DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT)

    is_running = True
    while is_running:
        time_delta = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            elif event.type == pygame.VIDEORESIZE:
                handle_resize(event.w, event.h)
            
            ui_manager.process_events(event)
            ui_controller.handle_event(event)
            if ui_controller.current_tab == 'sub_circuits':
                circuit_manager.handle_event(event)
            elif ui_controller.current_tab == 'main_circuit':
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == main_circuit.start_btn:
                        main_circuit.start()
                    elif event.ui_element == main_circuit.stop_btn:
                        main_circuit.stop()

        ui_manager.update(time_delta)
        
        params = ui_controller.get_parameters()
        
        screen.fill(COLOR_BG)
        ui_controller.draw_tabs(screen)
        
        if ui_controller.current_tab == 'simulation':
            circuit_manager.hide_ui()
            main_circuit.hide_ui()
            ui_controller.show_simulation_ui()
            
            wave_model.update(time_delta, params)
            particle_engine.update(time_delta, wave_model, params)
            microwave_view.draw(screen, particle_engine, wave_model)
            graph_view.draw(screen, particle_engine, wave_model)
            
        elif ui_controller.current_tab == 'sub_circuits':
            ui_controller.hide_simulation_ui()
            main_circuit.hide_ui()
            circuit_manager.show_ui()
            
            circuit_manager.update(time_delta)
            circuit_manager.draw(screen)
            
        elif ui_controller.current_tab == 'main_circuit':
            ui_controller.hide_simulation_ui()
            circuit_manager.hide_ui()
            main_circuit.show_ui()
            
            main_circuit.update(time_delta)
            main_circuit.draw(screen)

        ui_manager.draw_ui(screen)
        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
