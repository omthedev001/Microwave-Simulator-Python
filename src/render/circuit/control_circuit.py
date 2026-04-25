import pygame
import pygame_gui
from render.circuit.base_circuit import BaseCircuit
from config import *

class ControlCircuit(BaseCircuit):
    def __init__(self, ui_manager, name):
        super().__init__(ui_manager, name)
        
        self.time_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(0, 0, 100, 20),
            start_value=30.0, value_range=(0.0, 300.0), manager=self.ui_manager, visible=False
        )
        self.door_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(0, 0, 120, 30),
            text='Door: CLOSED', manager=self.ui_manager, visible=False
        )
        self.ui_elements.extend([self.time_slider, self.door_btn])
        self.timer = 0.0
        self.door_closed = True
        
    def _reposition_ui(self):
        self.time_slider.set_relative_position((self.rect.x + 10, self.rect.bottom - 60))
        self.door_btn.set_relative_position((self.rect.x + 10, self.rect.bottom - 30))
        
    def start(self):
        if self.door_closed:
            super().start()
            self.timer = self.time_slider.get_current_value()
        
    def update(self, dt):
        super().update(dt)
        if self.door_btn.check_pressed():
            self.door_closed = not self.door_closed
            self.door_btn.set_text('Door: CLOSED' if self.door_closed else 'Door: OPEN')
            if not self.door_closed and self.is_active:
                self.stop()
                
        if self.is_active:
            self.timer -= dt
            if self.timer <= 0:
                self.timer = 0
                self.stop()
                
    def draw(self, screen):
        super().draw(screen)
        c_y = self.rect.centery
        c_x = self.rect.centerx
        
        p_lv = (self.rect.x + 60, c_y)
        self._draw_inductor(screen, (p_lv[0], p_lv[1]-20), vertical=True)
        self._draw_inductor(screen, (p_lv[0]+20, p_lv[1]-20), vertical=True)
        self._draw_text_center(screen, "Step-Down", (p_lv[0]+10, p_lv[1]-55))
        
        # Door Sensor (Low voltage logic level)
        p_dsense = (self.rect.x + 150, c_y - 60)
        self._draw_switch(screen, p_dsense, closed=self.door_closed, label="Door Sense")
        
        u_rect = pygame.Rect(c_x - 60, c_y - 60, 120, 120)
        pygame.draw.rect(screen, (50, 50, 50), u_rect)
        pygame.draw.rect(screen, (150, 150, 150), u_rect, 3)
        self._draw_text_center(screen, "MCU / Logic", (u_rect.centerx, u_rect.centery - 20))
        
        disp_text = f"00:{int(self.timer):02d}" if self.is_active else "READY"
        disp_color = (100, 255, 100) if self.is_active else COLOR_TEXT
        self._draw_text_center(screen, disp_text, (u_rect.centerx, u_rect.centery + 20), color=disp_color)
        
        k_rect = pygame.Rect(c_x - 140, c_y + 40, 40, 60)
        pygame.draw.rect(screen, (100, 100, 100), k_rect, 2)
        self._draw_text_center(screen, "Keys", k_rect.center)
        
        p_bz = (c_x, c_y + 90)
        self._draw_inductor(screen, p_bz, label="Buzzer")
        
        p_relay_main = (c_x + 120, c_y - 40)
        p_relay_aux = (c_x + 120, c_y + 20)
        self._draw_diode(screen, p_relay_main, label="Main Rly")
        self._draw_diode(screen, p_relay_aux, label="Aux Rly")
        
        paths = [
            [(p_lv[0]+20, p_lv[1]-5), (p_dsense[0]-25, p_lv[1]-5), (p_dsense[0]-25, p_dsense[1]), (p_dsense[0]-15, p_dsense[1])],
            [(p_dsense[0]+15, p_dsense[1]), (u_rect.left, p_dsense[1])],
            [(p_lv[0]+20, p_lv[1]+5), (u_rect.left, p_lv[1]+5)],
            
            [(k_rect.right, k_rect.centery), (u_rect.left+20, k_rect.centery), (u_rect.left+20, u_rect.bottom)],
            [(p_bz[0], p_bz[1]-20), (p_bz[0], u_rect.bottom)],
            
            [(u_rect.right, p_relay_main[1]), (p_relay_main[0]-20, p_relay_main[1])],
            [(u_rect.right, p_relay_aux[1]), (p_relay_aux[0]-20, p_relay_aux[1])],
            
            [(p_relay_main[0]+20, p_relay_main[1]), (p_relay_main[0]+50, p_relay_main[1])],
            [(p_relay_aux[0]+20, p_relay_aux[1]), (p_relay_aux[0]+50, p_relay_aux[1])]
        ]
        
        for i, path in enumerate(paths):
            active = True
            if i == 1: active = self.door_closed
            elif i >= 5: active = self.is_active
            self._draw_wire_path(screen, path, active, speed=1.0)
