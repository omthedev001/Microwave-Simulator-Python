import pygame
import pygame_gui
from config import *

class UIController:
    def __init__(self, ui_manager, window_width, window_height):
        self.ui_manager = ui_manager
        self.current_tab = 'simulation'
        self.tabs_rect = pygame.Rect(0, 0, window_width, 40)
        
        self.right_panel = pygame.Rect(0, 0, 0, 0)
        self.sliders = {}
        self.labels = {}
        
        self._create_slider('freq', 'Frequency (GHz)', 1.0, 5.0, DEFAULT_FREQ_GHZ)
        self._create_slider('amp', 'Amplitude', 10.0, 200.0, DEFAULT_AMPLITUDE)
        self._create_slider('power', 'Power (W)', 100.0, 1500.0, DEFAULT_POWER)
        self._create_slider('speed', 'Simulation Speed', 0.1, 5.0, DEFAULT_SPEED)
        self._create_slider('density', 'Particle Density', 100, 800, 300)
        
    def _create_slider(self, key, label_text, min_val, max_val, default_val):
        label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(0, 0, 200, 25),
            text=f"{label_text}: {default_val}",
            manager=self.ui_manager,
            visible=False
        )
        slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(0, 0, 100, 20),
            start_value=default_val,
            value_range=(min_val, max_val),
            manager=self.ui_manager,
            visible=False
        )
        self.labels[key] = (label, label_text)
        self.sliders[key] = slider

    def handle_resize(self, w, h):
        self.tabs_rect.width = w
        
        right_panel_w = 270
        self.right_panel = pygame.Rect(w - right_panel_w - 10, 50, right_panel_w, h - 60)
        
        y_offset = self.right_panel.y + 10
        for i, key in enumerate(['freq', 'amp', 'power', 'speed', 'density']):
            label, _ = self.labels[key]
            slider = self.sliders[key]
            
            label.set_relative_position((self.right_panel.x, y_offset))
            label.set_dimensions((right_panel_w, 25))
            slider.set_relative_position((self.right_panel.x, y_offset + 30))
            slider.set_dimensions((right_panel_w, 20))
            
            y_offset += 70

    def draw_tabs(self, screen):
        pygame.draw.rect(screen, COLOR_TAB_BG, self.tabs_rect)
        
        sim_rect = pygame.Rect(10, 5, 120, 35)
        sim_color = COLOR_TAB_ACTIVE if self.current_tab == 'simulation' else COLOR_TAB_INACTIVE
        pygame.draw.polygon(screen, sim_color, [(sim_rect.left, sim_rect.bottom), (sim_rect.left+10, sim_rect.top), (sim_rect.right-10, sim_rect.top), (sim_rect.right, sim_rect.bottom)])
        
        sub_rect = pygame.Rect(140, 5, 140, 35)
        sub_color = COLOR_TAB_ACTIVE if self.current_tab == 'sub_circuits' else COLOR_TAB_INACTIVE
        pygame.draw.polygon(screen, sub_color, [(sub_rect.left, sub_rect.bottom), (sub_rect.left+10, sub_rect.top), (sub_rect.right-10, sub_rect.top), (sub_rect.right, sub_rect.bottom)])
        
        main_rect = pygame.Rect(290, 5, 140, 35)
        main_color = COLOR_TAB_ACTIVE if self.current_tab == 'main_circuit' else COLOR_TAB_INACTIVE
        pygame.draw.polygon(screen, main_color, [(main_rect.left, main_rect.bottom), (main_rect.left+10, main_rect.top), (main_rect.right-10, main_rect.top), (main_rect.right, main_rect.bottom)])
        
        font = pygame.font.SysFont(None, 22)
        screen.blit(font.render("Simulation", True, COLOR_TEXT), font.render("Simulation", True, COLOR_TEXT).get_rect(center=sim_rect.center))
        screen.blit(font.render("Sub-Circuits", True, COLOR_TEXT), font.render("Sub-Circuits", True, COLOR_TEXT).get_rect(center=sub_rect.center))
        screen.blit(font.render("Main Circuit", True, COLOR_TEXT), font.render("Main Circuit", True, COLOR_TEXT).get_rect(center=main_rect.center))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            if my <= 40:
                if 10 <= mx <= 130:
                    self.current_tab = 'simulation'
                elif 140 <= mx <= 280:
                    self.current_tab = 'sub_circuits'
                elif 290 <= mx <= 430:
                    self.current_tab = 'main_circuit'
                    
        elif event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            for key, slider in self.sliders.items():
                if event.ui_element == slider:
                    val = slider.get_current_value()
                    label, base_text = self.labels[key]
                    if key == 'density':
                        label.set_text(f"{base_text}: {int(val)}")
                    else:
                        label.set_text(f"{base_text}: {val:.2f}")

    def hide_simulation_ui(self):
        for lbl, _ in self.labels.values(): lbl.hide()
        for sl in self.sliders.values(): sl.hide()
            
    def show_simulation_ui(self):
        for lbl, _ in self.labels.values(): lbl.show()
        for sl in self.sliders.values(): sl.show()

    def get_parameters(self):
        return {
            'freq': self.sliders['freq'].get_current_value(),
            'amp': self.sliders['amp'].get_current_value(),
            'power': self.sliders['power'].get_current_value(),
            'speed': self.sliders['speed'].get_current_value(),
            'density': int(self.sliders['density'].get_current_value())
        }
