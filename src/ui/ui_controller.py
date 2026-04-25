import pygame
import pygame_gui
from config import *

class UIController:
    def __init__(self, ui_manager, window_width, window_height):
        self.ui_manager = ui_manager
        self.current_tab = 'simulation'
        
        # Title
        self.title_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 10), (300, 30)),
            text="MICROWAVE SIMULATOR",
            manager=self.ui_manager
        )
        
        # UI Elements
        self.tabs = pygame_gui.elements.UISelectionList(
            relative_rect=pygame.Rect((350, 10), (250, 30)),
            item_list=['Simulation', 'Circuit'],
            manager=self.ui_manager,
            default_selection='Simulation'
        )
        
        self.right_panel = pygame.Rect(window_width - 280, 60, 270, window_height - 70)
        
        # Right Panel Sliders
        self.sliders = {}
        self.labels = {}
        
        self._create_slider('freq', 'Frequency (GHz)', 1.0, 5.0, DEFAULT_FREQ_GHZ, 0)
        self._create_slider('amp', 'Amplitude', 10.0, 200.0, DEFAULT_AMPLITUDE, 1)
        self._create_slider('power', 'Power (W)', 100.0, 1500.0, DEFAULT_POWER, 2)
        self._create_slider('speed', 'Simulation Speed', 0.1, 5.0, DEFAULT_SPEED, 3)
        self._create_slider('density', 'Particle Density', 100, 2000, DEFAULT_PARTICLE_COUNT, 4)
        
    def _create_slider(self, key, label_text, min_val, max_val, default_val, index):
        y_offset = 80 + index * 80
        x_offset = self.right_panel.x
        
        label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((x_offset, y_offset), (260, 25)),
            text=f"{label_text}: {default_val}",
            manager=self.ui_manager
        )
        
        slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((x_offset, y_offset + 30), (260, 20)),
            start_value=default_val,
            value_range=(min_val, max_val),
            manager=self.ui_manager
        )
        
        self.labels[key] = (label, label_text)
        self.sliders[key] = slider

    def handle_event(self, event):
        if event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
            if event.ui_element == self.tabs:
                if event.text == 'Simulation':
                    self.current_tab = 'simulation'
                else:
                    self.current_tab = 'circuit'
                    
        elif event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            for key, slider in self.sliders.items():
                if event.ui_element == slider:
                    val = slider.get_current_value()
                    label, base_text = self.labels[key]
                    if key == 'density':
                        label.set_text(f"{base_text}: {int(val)}")
                    else:
                        label.set_text(f"{base_text}: {val:.2f}")

    def get_parameters(self):
        return {
            'freq': self.sliders['freq'].get_current_value(),
            'amp': self.sliders['amp'].get_current_value(),
            'power': self.sliders['power'].get_current_value(),
            'speed': self.sliders['speed'].get_current_value(),
            'density': int(self.sliders['density'].get_current_value())
        }
