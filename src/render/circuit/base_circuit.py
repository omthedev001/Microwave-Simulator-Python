import pygame
import pygame_gui
import math
from config import *

class BaseCircuit:
    def __init__(self, ui_manager, name):
        self.ui_manager = ui_manager
        self.name = name
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.is_active = False
        self.time = 0.0
        self.ui_elements = []
        self.font = pygame.font.SysFont(None, 24)
        self.title_font = pygame.font.SysFont(None, 28)
        
        # Base UI elements
        self.start_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(0, 0, 60, 30),
            text='Start',
            manager=self.ui_manager,
            visible=False
        )
        self.stop_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(0, 0, 60, 30),
            text='Stop',
            manager=self.ui_manager,
            visible=False
        )
        self.ui_elements.extend([self.start_btn, self.stop_btn])
        
    def set_bounds(self, rect):
        self.rect = rect
        self.start_btn.set_relative_position((rect.right - 140, rect.y + 10))
        self.stop_btn.set_relative_position((rect.right - 70, rect.y + 10))
        self._reposition_ui()
        
    def _reposition_ui(self):
        pass
        
    def start(self):
        self.is_active = True
        
    def stop(self):
        self.is_active = False
        
    def update(self, dt):
        if self.is_active:
            self.time += dt
            
    def draw(self, screen):
        # Base drawing
        pygame.draw.rect(screen, COLOR_CAVITY, self.rect)
        title_surf = self.title_font.render(self.name, True, COLOR_TEXT)
        screen.blit(title_surf, (self.rect.x + 10, self.rect.y + 10))
        
        status_text = "ACTIVE" if self.is_active else "STOPPED"
        status_color = (100, 255, 100) if self.is_active else (255, 100, 100)
        status_surf = self.font.render(status_text, True, status_color)
        screen.blit(status_surf, (self.rect.x + 10, self.rect.y + 40))
        
    def show_ui(self):
        for el in self.ui_elements:
            el.show()
            
    def hide_ui(self):
        for el in self.ui_elements:
            el.hide()
            
    def _draw_electrons(self, screen, start, end, speed=1.0, color=COLOR_ELECTRON_LOW):
        # Kept for backwards compatibility if needed, but we will mostly use _draw_wire_path
        dist = math.hypot(end[0] - start[0], end[1] - start[1])
        if dist == 0: return
        num_electrons = max(1, int(dist / 30))
        for i in range(num_electrons):
            progress = (self.time * 2.0 * speed + i / num_electrons) % 1.0
            ex = start[0] + (end[0] - start[0]) * progress
            ey = start[1] + (end[1] - start[1]) * progress
            pygame.draw.circle(screen, color, (int(ex), int(ey)), 4)
            
    def _draw_wire_path(self, screen, path, is_active, color=COLOR_WIRE_ACTIVE, electron_color=COLOR_ELECTRON_LOW, speed=1.0):
        if len(path) < 2: return
        c = color if is_active else COLOR_WIRE
        pygame.draw.lines(screen, c, False, path, 2)
        
        if not is_active: return
        
        total_len = sum(math.hypot(path[i+1][0]-path[i][0], path[i+1][1]-path[i][1]) for i in range(len(path)-1))
        if total_len == 0: return
        
        num_electrons = max(1, int(total_len / 30))
        for i in range(num_electrons):
            progress = (self.time * 2.0 * speed + i / num_electrons) % 1.0
            target_dist = progress * total_len
            
            curr_dist = 0
            for j in range(len(path)-1):
                start = path[j]
                end = path[j+1]
                dist = math.hypot(end[0]-start[0], end[1]-start[1])
                if curr_dist + dist >= target_dist:
                    seg_prog = (target_dist - curr_dist) / dist
                    ex = start[0] + (end[0]-start[0]) * seg_prog
                    ey = start[1] + (end[1]-start[1]) * seg_prog
                    pygame.draw.circle(screen, electron_color, (int(ex), int(ey)), 4)
                    break
                curr_dist += dist

    def _draw_capacitor(self, screen, center, vertical=False, label=""):
        c_x, c_y = center
        c = COLOR_COMPONENT
        if vertical:
            pygame.draw.line(screen, c, (c_x-15, c_y-5), (c_x+15, c_y-5), 3)
            pygame.draw.line(screen, c, (c_x-15, c_y+5), (c_x+15, c_y+5), 3)
            pygame.draw.line(screen, c, (c_x, c_y-20), (c_x, c_y-5), 2)
            pygame.draw.line(screen, c, (c_x, c_y+5), (c_x, c_y+20), 2)
            if label: self._draw_text_center(screen, label, (c_x+30, c_y))
        else:
            pygame.draw.line(screen, c, (c_x-5, c_y-15), (c_x-5, c_y+15), 3)
            pygame.draw.line(screen, c, (c_x+5, c_y-15), (c_x+5, c_y+15), 3)
            pygame.draw.line(screen, c, (c_x-20, c_y), (c_x-5, c_y), 2)
            pygame.draw.line(screen, c, (c_x+5, c_y), (c_x+20, c_y), 2)
            if label: self._draw_text_center(screen, label, (c_x, c_y-25))
            
    def _draw_diode(self, screen, center, vertical=False, label=""):
        c_x, c_y = center
        c = (255, 100, 100)
        if vertical:
            pygame.draw.polygon(screen, c, [(c_x-10, c_y-10), (c_x+10, c_y-10), (c_x, c_y+10)])
            pygame.draw.line(screen, c, (c_x-10, c_y+10), (c_x+10, c_y+10), 3)
            pygame.draw.line(screen, COLOR_COMPONENT, (c_x, c_y-20), (c_x, c_y-10), 2)
            pygame.draw.line(screen, COLOR_COMPONENT, (c_x, c_y+10), (c_x, c_y+20), 2)
            if label: self._draw_text_center(screen, label, (c_x+35, c_y))
        else:
            pygame.draw.polygon(screen, c, [(c_x-10, c_y-10), (c_x-10, c_y+10), (c_x+10, c_y)])
            pygame.draw.line(screen, c, (c_x+10, c_y-10), (c_x+10, c_y+10), 3)
            pygame.draw.line(screen, COLOR_COMPONENT, (c_x-20, c_y), (c_x-10, c_y), 2)
            pygame.draw.line(screen, COLOR_COMPONENT, (c_x+10, c_y), (c_x+20, c_y), 2)
            if label: self._draw_text_center(screen, label, (c_x, c_y-25))
            
    def _draw_switch(self, screen, center, closed=True, label="", vertical=False):
        c_x, c_y = center
        c = (100, 255, 100) if closed else (255, 100, 100)
        if vertical:
            pygame.draw.circle(screen, c, (c_x, c_y-15), 3)
            pygame.draw.circle(screen, c, (c_x, c_y+15), 3)
            if closed:
                pygame.draw.line(screen, c, (c_x, c_y-15), (c_x, c_y+15), 3)
            else:
                pygame.draw.line(screen, c, (c_x, c_y-15), (c_x+15, c_y+10), 3)
            if label: self._draw_text_center(screen, label, (c_x+35, c_y), color=c)
        else:
            pygame.draw.circle(screen, c, (c_x-15, c_y), 3)
            pygame.draw.circle(screen, c, (c_x+15, c_y), 3)
            if closed:
                pygame.draw.line(screen, c, (c_x-15, c_y), (c_x+15, c_y), 3)
            else:
                pygame.draw.line(screen, c, (c_x-15, c_y), (c_x+10, c_y-15), 3)
            if label: self._draw_text_center(screen, label, (c_x, c_y-25), color=c)
        
    def _draw_resistor(self, screen, center, vertical=False, label=""):
        c_x, c_y = center
        c = COLOR_COMPONENT
        pts = []
        if vertical:
            pts = [(c_x, c_y-20), (c_x, c_y-15), (c_x-10, c_y-10), (c_x+10, c_y), (c_x-10, c_y+10), (c_x, c_y+15), (c_x, c_y+20)]
            if label: self._draw_text_center(screen, label, (c_x+30, c_y))
        else:
            pts = [(c_x-20, c_y), (c_x-15, c_y), (c_x-10, c_y-10), (c_x, c_y+10), (c_x+10, c_y-10), (c_x+15, c_y), (c_x+20, c_y)]
            if label: self._draw_text_center(screen, label, (c_x, c_y-25))
        pygame.draw.lines(screen, c, False, pts, 2)
        
    def _draw_inductor(self, screen, center, vertical=False, label=""):
        c_x, c_y = center
        c = COLOR_COMPONENT
        if vertical:
            for i in range(-15, 15, 10):
                rect = pygame.Rect(c_x - 5, c_y + i, 10, 10)
                pygame.draw.arc(screen, c, rect, -math.pi/2, math.pi/2, 2)
            pygame.draw.line(screen, c, (c_x, c_y-25), (c_x, c_y-15), 2)
            pygame.draw.line(screen, c, (c_x, c_y+15), (c_x, c_y+25), 2)
            if label: self._draw_text_center(screen, label, (c_x+30, c_y))
        else:
            for i in range(-15, 15, 10):
                rect = pygame.Rect(c_x + i, c_y - 5, 10, 10)
                pygame.draw.arc(screen, c, rect, 0, math.pi, 2)
            pygame.draw.line(screen, c, (c_x-25, c_y), (c_x-15, c_y), 2)
            pygame.draw.line(screen, c, (c_x+15, c_y), (c_x+25, c_y), 2)
            if label: self._draw_text_center(screen, label, (c_x, c_y-25))
            
    def _draw_text_center(self, screen, text, pos, color=COLOR_TEXT):
        surf = self.font.render(text, True, color)
        rect = surf.get_rect(center=pos)
        screen.blit(surf, rect)
