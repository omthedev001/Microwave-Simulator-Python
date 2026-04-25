import pygame
import math
from config import *

class CircuitView:
    def __init__(self, rect):
        self.rect = rect
        self.font = pygame.font.SysFont(None, 24)
        self.title_font = pygame.font.SysFont(None, 36)
        self.time = 0.0
        
    def update(self, dt, params):
        self.time += dt * params['speed']
        self.power = params['power']
        self.voltage = DEFAULT_VOLTAGE
        
    def draw(self, screen):
        # Background
        pygame.draw.rect(screen, COLOR_CAVITY, self.rect)
        pygame.draw.rect(screen, COLOR_TEXT, self.rect, 2)
        
        title = self.title_font.render("Microwave Internal Circuitry", True, COLOR_TEXT)
        screen.blit(title, (self.rect.x + 20, self.rect.y + 20))
        
        c_x = self.rect.centerx
        c_y = self.rect.centery
        
        # Power Source
        p_rect = pygame.Rect(self.rect.x + 100, c_y - 40, 80, 80)
        pygame.draw.circle(screen, (200, 200, 50), p_rect.center, 40, 3)
        self._draw_text_center(screen, f"~ {self.voltage}V", p_rect.center)
        self._draw_text_center(screen, f"Power In: {self.power:.0f}W", (p_rect.centerx, p_rect.bottom + 20))
        
        # Transformer
        t_rect = pygame.Rect(self.rect.x + 350, c_y - 60, 120, 120)
        pygame.draw.rect(screen, (150, 150, 150), t_rect, 3)
        self._draw_text_center(screen, "High Voltage", (t_rect.centerx, t_rect.centery - 20))
        self._draw_text_center(screen, "Transformer", (t_rect.centerx, t_rect.centery + 20))
        
        # Capacitor & Diode
        c_rect = pygame.Rect(self.rect.x + 550, c_y - 120, 80, 50)
        pygame.draw.rect(screen, (100, 200, 255), c_rect, 3)
        self._draw_text_center(screen, "Capacitor", c_rect.center)
        
        d_rect = pygame.Rect(self.rect.x + 550, c_y + 70, 80, 50)
        pygame.draw.polygon(screen, (255, 100, 100), [(d_rect.left, d_rect.top), (d_rect.right, d_rect.centery), (d_rect.left, d_rect.bottom)])
        self._draw_text_center(screen, "Diode", d_rect.center)
        
        # Magnetron
        m_rect = pygame.Rect(self.rect.x + 750, c_y - 80, 160, 160)
        
        # Highlight magnetron based on power
        glow = min(255, max(50, int((self.power / 1500) * 255)))
        pygame.draw.circle(screen, (glow, glow//2, 50), m_rect.center, 80)
        pygame.draw.circle(screen, (255, 150, 50), m_rect.center, 80, 5)
        self._draw_text_center(screen, "Magnetron", m_rect.center)
        
        # Wires
        wires = [
            ((p_rect.right, c_y - 20), (t_rect.left, c_y - 20)),
            ((p_rect.right, c_y + 20), (t_rect.left, c_y + 20)),
            ((t_rect.right, c_y - 40), (c_rect.left, c_rect.centery)),
            ((t_rect.right, c_y + 40), (d_rect.left, d_rect.centery)),
            ((c_rect.right, c_rect.centery), (m_rect.left, m_rect.centery - 40)),
            ((d_rect.right, d_rect.centery), (m_rect.left, m_rect.centery + 40)),
        ]
        
        for start, end in wires:
            pygame.draw.line(screen, COLOR_TEXT, start, end, 3)
            self._draw_electrons(screen, start, end, self.power)

    def _draw_electrons(self, screen, start, end, power):
        dist = math.hypot(end[0] - start[0], end[1] - start[1])
        num_electrons = max(1, int(dist / 40))
        speed_multiplier = max(0.5, power / 800.0)
        
        for i in range(num_electrons):
            progress = (self.time * 2.0 * speed_multiplier + i / num_electrons) % 1.0
            ex = start[0] + (end[0] - start[0]) * progress
            ey = start[1] + (end[1] - start[1]) * progress
            pygame.draw.circle(screen, (100, 255, 100), (int(ex), int(ey)), 4)

    def _draw_text_center(self, screen, text, pos):
        surf = self.font.render(text, True, COLOR_TEXT)
        rect = surf.get_rect(center=pos)
        screen.blit(surf, rect)
