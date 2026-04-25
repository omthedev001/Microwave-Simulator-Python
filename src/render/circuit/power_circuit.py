import pygame
import pygame_gui
from render.circuit.base_circuit import BaseCircuit
from config import *

class PowerCircuit(BaseCircuit):
    def __init__(self, ui_manager, name):
        super().__init__(ui_manager, name)
        
        self.voltage_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(0, 0, 100, 20),
            start_value=220.0, value_range=(100.0, 240.0), manager=self.ui_manager, visible=False
        )
        self.ratio_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(0, 0, 100, 20),
            start_value=10.0, value_range=(5.0, 20.0), manager=self.ui_manager, visible=False
        )
        self.ui_elements.extend([self.voltage_slider, self.ratio_slider])
        self.time_active = 0.0
        
    def _reposition_ui(self):
        self.voltage_slider.set_relative_position((self.rect.x + 10, self.rect.bottom - 60))
        self.ratio_slider.set_relative_position((self.rect.x + 10, self.rect.bottom - 30))
        
    def update(self, dt):
        super().update(dt)
        if self.is_active:
            self.time_active += dt
        else:
            self.time_active = 0.0

    def draw(self, screen):
        super().draw(screen)
        c_y = self.rect.centery
        c_x = self.rect.centerx
        
        p_ac = (self.rect.x + 60, c_y)
        pygame.draw.circle(screen, (200, 200, 50), p_ac, 20, 2)
        self._draw_text_center(screen, "~", p_ac)
        self._draw_text_center(screen, f"{int(self.voltage_slider.get_current_value())}V", (p_ac[0], p_ac[1] + 30))
        
        p_fuse = (self.rect.x + 130, c_y - 30)
        self._draw_resistor(screen, p_fuse, label="Fuse")
        
        p_emi = (self.rect.x + 200, c_y)
        self._draw_inductor(screen, (p_emi[0], p_emi[1]-30), label="EMI L1")
        self._draw_inductor(screen, (p_emi[0], p_emi[1]+30), label="EMI L2")
        
        # Soft-start / Inrush circuit
        p_inrush_r = (self.rect.x + 280, c_y - 50)
        p_inrush_sw = (self.rect.x + 280, c_y - 10)
        self._draw_resistor(screen, p_inrush_r, label="Inrush R")
        soft_started = self.is_active and self.time_active > 0.5 # Bypasses resistor after 0.5s
        self._draw_switch(screen, p_inrush_sw, closed=soft_started, label="Soft Relay")
        
        aux_x = self.rect.x + 360
        p_fan = (aux_x, c_y - 80)
        p_lamp = (aux_x, c_y)
        p_turn = (aux_x, c_y + 80)
        
        self._draw_inductor(screen, p_fan, vertical=True, label="Fan")
        self._draw_resistor(screen, p_lamp, vertical=True, label="Lamp")
        self._draw_inductor(screen, p_turn, vertical=True, label="Turn. M")
        
        p_relay = (self.rect.x + 440, c_y - 30)
        self._draw_switch(screen, p_relay, closed=self.is_active, label="Main Relay")
        
        p_trans = (self.rect.x + 520, c_y)
        self._draw_inductor(screen, (p_trans[0], p_trans[1]-20), vertical=True)
        self._draw_inductor(screen, (p_trans[0]+20, p_trans[1]-20), vertical=True)
        pygame.draw.line(screen, COLOR_COMPONENT, (p_trans[0]+10, p_trans[1]-40), (p_trans[0]+10, p_trans[1]+40), 2)
        self._draw_text_center(screen, "HV Trans.", (p_trans[0]+10, p_trans[1]-55))
        
        paths = [
            [(p_ac[0], p_ac[1]-20), (p_ac[0], c_y-30), (p_fuse[0]-20, c_y-30)],
            [(p_fuse[0]+20, c_y-30), (p_emi[0]-25, c_y-30)],
            
            # Split to Inrush and Soft Relay
            [(p_emi[0]+25, c_y-30), (p_emi[0]+40, c_y-30), (p_inrush_r[0]-20, p_inrush_r[1])],
            [(p_emi[0]+40, c_y-30), (p_emi[0]+40, p_inrush_sw[1]), (p_inrush_sw[0]-15, p_inrush_sw[1])],
            
            # Combine after
            [(p_inrush_r[0]+20, p_inrush_r[1]), (p_inrush_sw[0]+30, p_inrush_r[1]), (p_inrush_sw[0]+30, c_y-30)],
            [(p_inrush_sw[0]+15, p_inrush_sw[1]), (p_inrush_sw[0]+30, p_inrush_sw[1]), (p_inrush_sw[0]+30, c_y-30)],
            
            [(p_inrush_sw[0]+30, c_y-30), (p_relay[0]-15, c_y-30)],
            [(p_relay[0]+15, c_y-30), (p_trans[0], c_y-30), (p_trans[0], p_trans[1]-35)],
            
            [(p_ac[0], p_ac[1]+20), (p_ac[0], c_y+30), (p_emi[0]-25, c_y+30)],
            [(p_emi[0]+25, c_y+30), (p_trans[0], c_y+30), (p_trans[0], p_trans[1]+5)],
            
            [(p_emi[0]+25, c_y-30), (aux_x, c_y-30), (aux_x, p_fan[1]-25)],
            [(aux_x, c_y-30), (aux_x, p_lamp[1]-20)],
            [(aux_x, c_y-30), (aux_x, p_turn[1]-25)],
            
            [(p_emi[0]+25, c_y+30), (aux_x, c_y+30), (aux_x, p_fan[1]+25)],
            [(aux_x, c_y+30), (aux_x, p_lamp[1]+20)],
            [(aux_x, c_y+30), (aux_x, p_turn[1]+25)],
        ]
        
        for path in paths:
            self._draw_wire_path(screen, path, self.is_active, speed=1.5)
