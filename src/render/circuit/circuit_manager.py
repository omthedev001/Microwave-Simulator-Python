import pygame
import pygame_gui
from render.circuit.power_circuit import PowerCircuit
from render.circuit.heating_circuit import HeatingCircuit
from render.circuit.protection_circuit import ProtectionCircuit
from render.circuit.control_circuit import ControlCircuit
from config import *

class CircuitManager:
    def __init__(self, rect, ui_manager):
        self.rect = rect
        self.ui_manager = ui_manager
        
        self.circuits = {
            'power': PowerCircuit(ui_manager, "Power Supply"),
            'heating': HeatingCircuit(ui_manager, "High Voltage & Heating"),
            'protection': ProtectionCircuit(ui_manager, "Protection & Safety"),
            'control': ControlCircuit(ui_manager, "Control / UI Circuit")
        }
        
    def handle_resize(self, new_rect):
        self.rect = new_rect
        w = new_rect.width // 2
        h = new_rect.height // 2
        
        self.circuits['power'].set_bounds(pygame.Rect(new_rect.x, new_rect.y, w, h))
        self.circuits['heating'].set_bounds(pygame.Rect(new_rect.x + w, new_rect.y, w, h))
        self.circuits['protection'].set_bounds(pygame.Rect(new_rect.x, new_rect.y + h, w, h))
        self.circuits['control'].set_bounds(pygame.Rect(new_rect.x + w, new_rect.y + h, w, h))

    def handle_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            for key, circuit in self.circuits.items():
                if event.ui_element == circuit.start_btn:
                    # Stop others
                    for k, c in self.circuits.items():
                        c.stop()
                    circuit.start()
                elif event.ui_element == circuit.stop_btn:
                    circuit.stop()

    def update(self, dt):
        for circuit in self.circuits.values():
            circuit.update(dt)
            
    def draw(self, screen):
        for circuit in self.circuits.values():
            circuit.draw(screen)
            pygame.draw.rect(screen, COLOR_TEXT, circuit.rect, 1)

    def show_ui(self):
        for circuit in self.circuits.values():
            circuit.show_ui()
            
    def hide_ui(self):
        for circuit in self.circuits.values():
            circuit.hide_ui()
