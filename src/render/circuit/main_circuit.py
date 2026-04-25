import pygame
import pygame_gui
from render.circuit.base_circuit import BaseCircuit
from config import *

class MainCircuit(BaseCircuit):
    def __init__(self, ui_manager, name):
        super().__init__(ui_manager, name)
        
        self.power_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(0, 0, 150, 20),
            start_value=1000.0, value_range=(100.0, 1500.0), manager=self.ui_manager, visible=False
        )
        self.time_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(0, 0, 150, 20),
            start_value=60.0, value_range=(0.0, 300.0), manager=self.ui_manager, visible=False
        )
        self.temp_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(0, 0, 150, 20),
            start_value=25.0, value_range=(20.0, 150.0), manager=self.ui_manager, visible=False
        )
        self.door_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(0, 0, 120, 30),
            text='Door: CLOSED', manager=self.ui_manager, visible=False
        )
        
        self.ui_elements.extend([self.power_slider, self.time_slider, self.temp_slider, self.door_btn])
        self.door_closed = True
        self.timer = 0.0
        self.time_active = 0.0
        self.temp_limit = 120.0

    def _reposition_ui(self):
        self.power_slider.set_relative_position((self.rect.x + 10, self.rect.bottom - 40))
        self.time_slider.set_relative_position((self.rect.x + 180, self.rect.bottom - 40))
        self.temp_slider.set_relative_position((self.rect.x + 350, self.rect.bottom - 40))
        self.door_btn.set_relative_position((self.rect.right - 280, self.rect.y + 10))
        
    def start(self):
        temp = self.temp_slider.get_current_value()
        if self.door_closed and temp < self.temp_limit:
            super().start()
            self.timer = self.time_slider.get_current_value()
            self.time_active = 0.0
        
    def update(self, dt):
        super().update(dt)
        
        temp = self.temp_slider.get_current_value()
        thermal_trip = temp >= self.temp_limit
        
        if self.door_btn.check_pressed():
            self.door_closed = not self.door_closed
            self.door_btn.set_text('Door: CLOSED' if self.door_closed else 'Door: OPEN')
            
        if self.is_active:
            self.time_active += dt
            if not self.door_closed or thermal_trip:
                self.stop()
            else:
                self.timer -= dt
                if self.timer <= 0:
                    self.timer = 0
                    self.stop()
        else:
            self.time_active = 0.0

    def draw(self, screen):
        super().draw(screen)
        
        w, h = self.rect.width, self.rect.height
        
        zones = [
            ("AC Mains & Filters", pygame.Rect(self.rect.x+20, self.rect.y+60, w*0.2, h*0.35)),
            ("Aux (Fan, Lamp, Motor)", pygame.Rect(self.rect.x+20, self.rect.y+60 + h*0.35 + 20, w*0.2, h*0.4)),
            ("Interlocks & Soft-Start", pygame.Rect(self.rect.x+20 + w*0.2 + 20, self.rect.y+60, w*0.2, h*0.4)),
            ("Control Board (PCB)", pygame.Rect(self.rect.x+20 + w*0.2 + 20, self.rect.y+60 + h*0.4 + 20, w*0.2, h*0.35)),
            ("High Voltage Section", pygame.Rect(self.rect.x+20 + w*0.4 + 40, self.rect.y+60, w*0.45, h*0.8))
        ]
        
        for name, zrect in zones:
            pygame.draw.rect(screen, (40, 40, 45), zrect)
            pygame.draw.rect(screen, (80, 80, 90), zrect, 1)
            self._draw_text_center(screen, name, (zrect.centerx, zrect.top + 15), color=(150, 150, 180))

        z_ac = zones[0][1]
        p_ac = (z_ac.left + 40, z_ac.centery)
        p_fuse = (z_ac.centerx, p_ac[1] - 40)
        p_filter1 = (z_ac.right - 40, p_ac[1] - 40)
        p_filter2 = (z_ac.right - 40, p_ac[1] + 40)
        
        z_aux = zones[1][1]
        p_fan = (z_aux.centerx, z_aux.top + 50)
        p_lamp = (z_aux.centerx, z_aux.centery)
        p_turn = (z_aux.centerx, z_aux.bottom - 50)
        
        z_safe = zones[2][1]
        p_tco = (z_safe.left + 30, z_safe.top + 40)
        p_pri_sw = (z_safe.centerx, z_safe.top + 50)
        p_sec_sw = (z_safe.centerx, z_safe.bottom - 20)
        p_mon_sw = (z_safe.right - 40, z_safe.centery + 20)
        
        p_inrush_r = (z_safe.centerx, z_safe.top + 100)
        p_inrush_sw = (z_safe.centerx + 40, z_safe.top + 100)
        
        z_ctl = zones[3][1]
        p_mcu = (z_ctl.centerx, z_ctl.centery)
        p_dsense = (z_ctl.left + 40, z_ctl.centery - 40)
        p_relay = (z_ctl.centerx, z_ctl.top + 30)
        p_relay_aux = (z_ctl.centerx, z_ctl.bottom - 30)
        
        z_hv = zones[4][1]
        p_trans1 = (z_hv.left + 60, z_hv.centery - 40)
        p_trans2 = (z_hv.left + 60, z_hv.centery + 40)
        p_hv_fuse = (z_hv.centerx - 40, z_hv.top + 100)
        p_cap = (z_hv.centerx + 40, z_hv.top + 100)
        p_bleed = (z_hv.centerx + 40, z_hv.top + 50)
        p_diode = (z_hv.centerx + 40, z_hv.bottom - 100)
        p_mag = (z_hv.right - 80, z_hv.centery)

        # Draw components
        self._draw_text_center(screen, "220V AC", (p_ac[0], p_ac[1] - 30))
        pygame.draw.circle(screen, (200, 200, 50), p_ac, 20, 2)
        
        self._draw_resistor(screen, p_fuse, label="Main Fuse")
        self._draw_inductor(screen, p_filter1, label="EMI L1")
        self._draw_inductor(screen, p_filter2, label="EMI L2")

        self._draw_inductor(screen, p_fan, vertical=True, label="Fan")
        self._draw_resistor(screen, p_lamp, vertical=True, label="Lamp")
        self._draw_inductor(screen, p_turn, vertical=True, label="Motor")

        temp = self.temp_slider.get_current_value()
        tco_closed = temp < self.temp_limit
        if not tco_closed:
            self._draw_text_center(screen, "THERMAL TRIP!", (self.rect.centerx, self.rect.y + 30), color=(255,50,50))

        self._draw_switch(screen, p_tco, closed=tco_closed, label="Cavity TCO")
        self._draw_switch(screen, p_pri_sw, closed=self.door_closed, label="Pri. SW")
        self._draw_switch(screen, p_sec_sw, closed=self.door_closed, label="Sec. SW")
        self._draw_switch(screen, p_mon_sw, closed=not self.door_closed, vertical=True, label="Mon. SW")
        
        self._draw_resistor(screen, p_inrush_r, label="Inrush R")
        soft_started = self.is_active and self.time_active > 0.5
        self._draw_switch(screen, p_inrush_sw, closed=soft_started, vertical=True, label="Soft Rly")

        self._draw_switch(screen, p_dsense, closed=self.door_closed, label="Door Sense")
        mcu_rect = pygame.Rect(0, 0, 100, 80)
        mcu_rect.center = p_mcu
        pygame.draw.rect(screen, (150,150,150), mcu_rect, 2)
        self._draw_text_center(screen, "MCU", p_mcu)
        disp_text = f"00:{int(self.timer):02d}" if self.is_active else "READY"
        self._draw_text_center(screen, disp_text, (p_mcu[0], p_mcu[1] + 25), color=(100,255,100) if self.is_active else COLOR_TEXT)
        
        self._draw_switch(screen, p_relay, closed=self.is_active, label="Main Relay")
        self._draw_switch(screen, p_relay_aux, closed=self.is_active, label="Aux Relay")

        self._draw_inductor(screen, p_trans1, vertical=True)
        self._draw_inductor(screen, p_trans2, vertical=True)
        pygame.draw.line(screen, COLOR_COMPONENT, (p_trans1[0]+15, p_trans1[1]-20), (p_trans1[0]+15, p_trans2[1]+20), 2)
        self._draw_text_center(screen, "HV Transformer", (p_trans1[0], p_trans1[1]-40))
        
        self._draw_resistor(screen, p_hv_fuse, label="HV Fuse")
        self._draw_capacitor(screen, p_cap, label="HV Cap")
        self._draw_resistor(screen, p_bleed, label="Bleed 10M")
        self._draw_diode(screen, p_diode, vertical=True, label="HV Diode")
        pygame.draw.line(screen, COLOR_TEXT, (p_diode[0]-15, p_diode[1]+25), (p_diode[0]+15, p_diode[1]+25), 3)
        
        mag_rect = pygame.Rect(0, 0, 120, 120)
        mag_rect.center = p_mag
        if self.is_active:
            glow = min(255, max(50, int((self.power_slider.get_current_value() / 1500) * 255)))
            pygame.draw.circle(screen, (glow, 50, 50), p_mag, 50)
        pygame.draw.circle(screen, (255, 150, 50), p_mag, 60, 4)
        self._draw_text_center(screen, "Magnetron", p_mag)
        
        # Wiring Paths
        path_l_main = [(p_ac[0], p_ac[1]-20), (p_ac[0], p_fuse[1]), (p_fuse[0]-20, p_fuse[1])]
        path_fuse_emi = [(p_fuse[0]+20, p_fuse[1]), (p_filter1[0]-25, p_filter1[1])]
        path_emi_tco = [(p_filter1[0]+25, p_filter1[1]), (p_tco[0]-15, p_tco[1])]
        path_tco_pri = [(p_tco[0]+15, p_tco[1]), (p_pri_sw[0], p_tco[1]), (p_pri_sw[0], p_pri_sw[1]-15)]
        
        path_pri_inrush = [(p_pri_sw[0], p_pri_sw[1]+15), (p_inrush_r[0]-20, p_inrush_r[1])]
        path_pri_soft = [(p_pri_sw[0], p_pri_sw[1]+15), (p_inrush_sw[0], p_pri_sw[1]+15), (p_inrush_sw[0], p_inrush_sw[1]-15)]
        path_inrush_rel = [(p_inrush_r[0]+20, p_inrush_r[1]), (p_relay[0]-15, p_relay[1])]
        path_soft_rel = [(p_inrush_sw[0], p_inrush_sw[1]+15), (p_inrush_sw[0], p_relay[1]), (p_relay[0]-15, p_relay[1])]
        
        path_rel_trans = [(p_relay[0]+15, p_relay[1]), (p_trans1[0], p_relay[1]), (p_trans1[0], p_trans1[1]-25)]
        
        path_n_emi = [(p_ac[0], p_ac[1]+20), (p_ac[0], p_filter2[1]), (p_filter2[0]-25, p_filter2[1])]
        path_emi_sec = [(p_filter2[0]+25, p_filter2[1]), (p_sec_sw[0], p_filter2[1]), (p_sec_sw[0], p_sec_sw[1]-15)]
        path_sec_trans = [(p_sec_sw[0], p_sec_sw[1]+15), (p_trans2[0], p_sec_sw[1]+15), (p_trans2[0], p_trans2[1]+25)]
        
        path_mon_live = [(p_pri_sw[0], p_pri_sw[1]+15), (p_mon_sw[0], p_pri_sw[1]+15), (p_mon_sw[0], p_mon_sw[1]-15)]
        path_mon_neut = [(p_mon_sw[0], p_mon_sw[1]+15), (p_mon_sw[0], p_sec_sw[1]+15), (p_sec_sw[0], p_sec_sw[1]+15)]

        # Control and Aux
        path_mcu_dsense = [(p_filter1[0]+25, p_filter1[1]), (p_dsense[0]-15, p_filter1[1]), (p_dsense[0]-15, p_dsense[1])]
        path_dsense_mcu = [(p_dsense[0]+15, p_dsense[1]), (mcu_rect.left, p_dsense[1])]
        path_mcu_rel1 = [(mcu_rect.right, p_relay[1]), (p_relay[0], p_relay[1]-15)]
        path_mcu_rel2 = [(mcu_rect.right, p_relay_aux[1]), (p_relay_aux[0], p_relay_aux[1]-15)]
        
        # Auxiliaries powered via Aux Relay
        path_aux_l = [(p_filter1[0]+25, p_filter1[1]), (p_relay_aux[0]-15, p_relay_aux[1])]
        path_aux_out = [(p_relay_aux[0]+15, p_relay_aux[1]), (p_fan[0], p_relay_aux[1]), (p_fan[0], p_fan[1]-20)]
        path_aux_fan_l = [(p_fan[0], p_fan[1]+20), (p_lamp[0], p_lamp[1]-20)]
        path_aux_lamp_l = [(p_lamp[0], p_lamp[1]+20), (p_turn[0], p_turn[1]-20)]
        path_aux_n = [(p_turn[0], p_turn[1]+20), (p_turn[0], p_filter2[1]), (p_filter2[0]+25, p_filter2[1])]

        # HV Paths
        path_hv_fuse = [(p_trans1[0]+20, p_trans1[1]), (p_hv_fuse[0]-20, p_trans1[1])]
        path_fuse_cap = [(p_hv_fuse[0]+20, p_hv_fuse[1]), (p_cap[0]-20, p_hv_fuse[1])]
        
        path_cap_bleed_top = [(p_cap[0]-20, p_cap[1]), (p_cap[0]-20, p_bleed[1]), (p_bleed[0]-20, p_bleed[1])]
        path_cap_bleed_bot = [(p_bleed[0]+20, p_bleed[1]), (p_cap[0]+20, p_bleed[1]), (p_cap[0]+20, p_cap[1])]
        
        path_cap_dio = [(p_cap[0]+20, p_cap[1]), (p_diode[0], p_cap[1]), (p_diode[0], p_diode[1]-20)]
        path_cap_mag = [(p_diode[0], p_cap[1]), (mag_rect.left, p_cap[1])]
        path_fil1 = [(p_trans2[0]+20, p_trans2[1]-5), (mag_rect.left-20, p_trans2[1]-5), (mag_rect.left-20, p_mag[1]+20), (mag_rect.left, p_mag[1]+20)]
        path_fil2 = [(p_trans2[0]+20, p_trans2[1]+5), (mag_rect.left-10, p_trans2[1]+5), (mag_rect.left-10, p_mag[1]+40), (mag_rect.left, p_mag[1]+40)]

        # Drawing
        self._draw_wire_path(screen, path_l_main, True, speed=1.5)
        self._draw_wire_path(screen, path_fuse_emi, True, speed=1.5)
        self._draw_wire_path(screen, path_emi_tco, True, speed=1.5)
        self._draw_wire_path(screen, path_tco_pri, tco_closed, speed=1.5)
        
        pri_active = tco_closed and self.door_closed
        self._draw_wire_path(screen, path_pri_inrush, pri_active, speed=1.5)
        self._draw_wire_path(screen, path_pri_soft, pri_active, speed=1.5)
        self._draw_wire_path(screen, path_inrush_rel, pri_active, speed=1.5)
        self._draw_wire_path(screen, path_soft_rel, pri_active and soft_started, speed=1.5)
        
        self._draw_wire_path(screen, path_rel_trans, pri_active and self.is_active, speed=1.5)
        
        self._draw_wire_path(screen, path_n_emi, True, speed=1.5)
        self._draw_wire_path(screen, path_emi_sec, True, speed=1.5)
        self._draw_wire_path(screen, path_sec_trans, self.door_closed, speed=1.5)
        
        self._draw_wire_path(screen, path_mon_live, pri_active, speed=1.5)
        self._draw_wire_path(screen, path_mon_neut, True, speed=1.5)
        
        # MCU Paths
        self._draw_wire_path(screen, path_mcu_dsense, True, speed=1.0)
        self._draw_wire_path(screen, path_dsense_mcu, self.door_closed, speed=1.0)
        self._draw_wire_path(screen, path_mcu_rel1, self.is_active, speed=1.0)
        self._draw_wire_path(screen, path_mcu_rel2, self.is_active, speed=1.0)
        
        aux_active = self.is_active
        self._draw_wire_path(screen, path_aux_l, True, speed=1.0)
        self._draw_wire_path(screen, path_aux_out, aux_active, speed=1.0)
        self._draw_wire_path(screen, path_aux_fan_l, aux_active, speed=1.0)
        self._draw_wire_path(screen, path_aux_lamp_l, aux_active, speed=1.0)
        self._draw_wire_path(screen, path_aux_n, aux_active, speed=1.0)
        
        hv_active = pri_active and self.is_active and self.door_closed
        hc = COLOR_ELECTRON_HIGH
        self._draw_wire_path(screen, path_hv_fuse, hv_active, color=COLOR_WIRE_ACTIVE, electron_color=hc, speed=2.0)
        self._draw_wire_path(screen, path_fuse_cap, hv_active, color=COLOR_WIRE_ACTIVE, electron_color=hc, speed=2.0)
        self._draw_wire_path(screen, path_cap_bleed_top, hv_active, color=COLOR_WIRE_ACTIVE, electron_color=hc, speed=2.0)
        self._draw_wire_path(screen, path_cap_bleed_bot, hv_active, color=COLOR_WIRE_ACTIVE, electron_color=hc, speed=2.0)
        self._draw_wire_path(screen, path_cap_dio, hv_active, color=COLOR_WIRE_ACTIVE, electron_color=hc, speed=2.0)
        self._draw_wire_path(screen, path_cap_mag, hv_active, color=COLOR_WIRE_ACTIVE, electron_color=hc, speed=2.0)
        self._draw_wire_path(screen, path_fil1, hv_active, color=COLOR_WIRE_ACTIVE, electron_color=hc, speed=2.0)
        self._draw_wire_path(screen, path_fil2, hv_active, color=COLOR_WIRE_ACTIVE, electron_color=hc, speed=2.0)
