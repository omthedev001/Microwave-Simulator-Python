import pygame
import pygame_gui
from render.circuit.base_circuit import BaseCircuit
from config import *

class ProtectionCircuit(BaseCircuit):
    def __init__(self, ui_manager, name):
        super().__init__(ui_manager, name)
        
        self.door_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(0, 0, 120, 30),
            text='Door: CLOSED', manager=self.ui_manager, visible=False
        )
        self.temp_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(0, 0, 100, 20),
            start_value=80.0, value_range=(50.0, 150.0), manager=self.ui_manager, visible=False
        )
        self.ui_elements.extend([self.door_btn, self.temp_slider])
        self.door_closed = True
        
    def _reposition_ui(self):
        self.door_btn.set_relative_position((self.rect.x + 10, self.rect.bottom - 70))
        self.temp_slider.set_relative_position((self.rect.x + 10, self.rect.bottom - 30))
        
    def update(self, dt):
        super().update(dt)
        if self.door_btn.check_pressed():
            self.door_closed = not self.door_closed
            self.door_btn.set_text('Door: CLOSED' if self.door_closed else 'Door: OPEN')
            
        if not self.door_closed and self.is_active:
            self.stop()
            
    def draw(self, screen):
        super().draw(screen)
        c_y = self.rect.centery
        
        p_l = (self.rect.x + 40, c_y - 40)
        p_n = (self.rect.x + 40, c_y + 40)
        
        self._draw_text_center(screen, "Live In", (p_l[0], p_l[1]-20))
        self._draw_text_center(screen, "Neutral In", (p_n[0], p_n[1]+20))
        
        p_tco1 = (self.rect.x + 120, c_y - 40)
        p_tco2 = (self.rect.x + 200, c_y - 40)
        
        # TCOs can be drawn as normally closed switches with a label
        self._draw_switch(screen, p_tco1, closed=True, label="Mag TCO")
        self._draw_switch(screen, p_tco2, closed=True, label="Cav TCO")
        
        p_sw1 = (self.rect.x + 300, c_y - 40)
        p_sw2 = (self.rect.x + 300, c_y + 40)
        p_mon = (self.rect.x + 380, c_y)
        
        self._draw_switch(screen, p_sw1, closed=self.door_closed, label="Pri. SW")
        self._draw_switch(screen, p_sw2, closed=self.door_closed, label="Sec. SW")
        self._draw_switch(screen, p_mon, closed=not self.door_closed, vertical=True, label="Mon. SW")
        
        paths = [
            [(p_l[0], p_l[1]), (p_tco1[0]-15, p_tco1[1])],
            [(p_tco1[0]+15, p_tco1[1]), (p_tco2[0]-15, p_tco2[1])],
            [(p_tco2[0]+15, p_tco2[1]), (p_sw1[0]-15, p_sw1[1])],
            [(p_n[0], p_n[1]), (p_sw2[0]-15, p_sw2[1])],
            
            # Monitor circuit
            [(p_sw1[0]+15, p_sw1[1]), (p_mon[0], p_sw1[1]), (p_mon[0], p_mon[1]-15)],
            [(p_mon[0], p_mon[1]+15), (p_mon[0], p_sw2[1]), (p_sw2[0]+15, p_sw2[1])],
        ]
        
        for path in paths:
            color = COLOR_WIRE_ACTIVE if (self.is_active and self.door_closed) else COLOR_WIRE
            self._draw_wire_path(screen, path, (self.is_active and self.door_closed), color=color, speed=0.5)
