import pygame
import numpy as np
from config import *

class MicrowaveView:
    def __init__(self, rect):
        self.rect = rect
        self.font = pygame.font.SysFont(None, 24)
        
    def get_color(self, temp):
        if temp < 20: temp = 20
        if temp > 500: temp = 500
        
        if temp < 260:
            ratio = (temp - 20) / 240.0
            r = int(COLOR_HEAT_LOW[0] * (1 - ratio) + COLOR_HEAT_MED[0] * ratio)
            g = int(COLOR_HEAT_LOW[1] * (1 - ratio) + COLOR_HEAT_MED[1] * ratio)
            b = int(COLOR_HEAT_LOW[2] * (1 - ratio) + COLOR_HEAT_MED[2] * ratio)
        else:
            ratio = (temp - 260) / 240.0
            r = int(COLOR_HEAT_MED[0] * (1 - ratio) + COLOR_HEAT_HIGH[0] * ratio)
            g = int(COLOR_HEAT_MED[1] * (1 - ratio) + COLOR_HEAT_HIGH[1] * ratio)
            b = int(COLOR_HEAT_MED[2] * (1 - ratio) + COLOR_HEAT_HIGH[2] * ratio)
        return (r, g, b)

    def draw(self, screen, particle_engine, wave_model):
        # Draw Cavity Background
        pygame.draw.rect(screen, COLOR_CAVITY, self.rect)
        pygame.draw.rect(screen, COLOR_TEXT, self.rect, 2)
        
        # Draw Wave visual
        pts = []
        for x in range(self.rect.left, self.rect.right, 5):
            y_offset = wave_model.get_field(np.array([x]), wave_model.time)[0]
            pts.append((x, self.rect.centery - y_offset * 0.5))
            
        if len(pts) > 1:
            pygame.draw.lines(screen, (50, 100, 150), False, pts, 2)
        
        # Draw Particles
        for i in range(particle_engine.num_particles):
            pos = particle_engine.positions[i]
            temp = particle_engine.temperatures[i]
            angle = particle_engine.angles[i]
            
            color = self.get_color(temp)
            
            px, py = int(pos[0]), int(pos[1])
            dx = int(np.cos(angle) * 8)
            dy = int(np.sin(angle) * 8)
            
            pygame.draw.circle(screen, color, (px, py), 6)
            pygame.draw.line(screen, (255,255,255), (px, py), (px+dx, py+dy), 2)

        # Draw Heatmap Overlay
        overlay = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        avg_temp = np.mean(particle_engine.temperatures)
        alpha = int(min(255, max(0, (avg_temp - 20) * 2)))
        overlay.fill((255, 50, 0, alpha // 4))
        screen.blit(overlay, self.rect.topleft)
        
        # Info Text
        text = self.font.render(f"Avg Temp: {avg_temp:.1f} °C", True, COLOR_TEXT)
        screen.blit(text, (self.rect.x + 10, self.rect.y + 10))
