import pygame
import pygame_gui
from render.circuit.base_circuit import BaseCircuit
from config import *

class HeatingCircuit(BaseCircuit):
    def __init__(self, ui_manager, name):
        super().__init__(ui_manager, name)
        
        self.eff_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(0, 0, 100, 20),
            start_value=65.0, value_range=(50.0, 90.0), manager=self.ui_manager, visible=False
        )
        self.power_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(0, 0, 100, 20),
            start_value=800.0, value_range=(100.0, 1500.0), manager=self.ui_manager, visible=False
        )
        self.ui_elements.extend([self.eff_slider, self.power_slider])
        
    def _reposition_ui(self):
        self.eff_slider.set_relative_position((self.rect.x + 10, self.rect.bottom - 60))
        self.power_slider.set_relative_position((self.rect.x + 10, self.rect.bottom - 30))
        
    def draw(self, screen):
        super().draw(screen)
        c_y = self.rect.centery
        c_x = self.rect.centerx
        
        p_in = (self.rect.x + 40, c_y - 40)
        p_fil1 = (self.rect.x + 40, c_y + 40)
        p_fil2 = (self.rect.x + 40, c_y + 80)
        
        self._draw_text_center(screen, "HV Sec. ->", (p_in[0] + 30, p_in[1] - 15))
        self._draw_text_center(screen, "Filament ->", (p_fil1[0] + 30, p_fil1[1] - 15))
        
        p_hv_fuse = (self.rect.x + 140, c_y - 40)
        self._draw_resistor(screen, p_hv_fuse, label="HV Fuse 0.8A")
        
        p_cap = (self.rect.x + 240, c_y - 40)
        self._draw_capacitor(screen, p_cap, label="HV Cap")
        
        p_bleed = (self.rect.x + 240, c_y - 90)
        self._draw_resistor(screen, p_bleed, label="Bleed 10M")
        
        p_diode = (self.rect.x + 320, c_y + 20)
        self._draw_diode(screen, p_diode, vertical=True, label="HV Diode")
        pygame.draw.line(screen, COLOR_TEXT, (p_diode[0]-15, p_diode[1]+25), (p_diode[0]+15, p_diode[1]+25), 3) # GND
        
        m_rect = pygame.Rect(self.rect.x + 400, c_y - 60, 120, 120)
        if self.is_active:
            glow = min(255, max(50, int((self.power_slider.get_current_value() / 1500) * 255)))
            pygame.draw.circle(screen, (glow, 50, 50), m_rect.center, 60)
        pygame.draw.circle(screen, (255, 150, 50), m_rect.center, 60, 4)
        self._draw_text_center(screen, "Magnetron", m_rect.center)
        
        paths = [
            [(p_in[0], p_in[1]), (p_hv_fuse[0]-20, p_hv_fuse[1])],
            [(p_hv_fuse[0]+20, p_hv_fuse[1]), (p_cap[0]-20, p_cap[1])],
            
            # Bleed parallel
            [(p_cap[0]-20, p_cap[1]), (p_cap[0]-20, p_bleed[1]), (p_bleed[0]-20, p_bleed[1])],
            [(p_bleed[0]+20, p_bleed[1]), (p_cap[0]+20, p_bleed[1]), (p_cap[0]+20, p_cap[1])],
            
            [(p_cap[0]+20, p_cap[1]), (p_diode[0], p_cap[1]), (p_diode[0], p_diode[1]-20)],
            [(p_diode[0], p_cap[1]), (m_rect.left, p_cap[1])],
            [(p_fil1[0], p_fil1[1]), (m_rect.left-20, p_fil1[1]), (m_rect.left-20, m_rect.centery+20), (m_rect.left, m_rect.centery+20)],
            [(p_fil2[0], p_fil2[1]), (m_rect.left-10, p_fil2[1]), (m_rect.left-10, m_rect.centery+40), (m_rect.left, m_rect.centery+40)],
        ]
        
        for path in paths:
            self._draw_wire_path(screen, path, self.is_active, color=COLOR_WIRE_ACTIVE, electron_color=COLOR_ELECTRON_HIGH, speed=2.0)
