import pygame
from config import *

class GraphView:
    def __init__(self, rect):
        self.rect = rect
        self.font = pygame.font.SysFont(None, 20)
        
    def _draw_graph(self, screen, title, y_offset, data, color, min_y, max_y):
        graph_rect = pygame.Rect(self.rect.x, self.rect.y + y_offset, self.rect.width, 180)
        pygame.draw.rect(screen, COLOR_GRAPH_BG, graph_rect)
        pygame.draw.rect(screen, COLOR_TEXT, graph_rect, 1)
        
        title_surf = self.font.render(title, True, COLOR_TEXT)
        screen.blit(title_surf, (graph_rect.x + 5, graph_rect.y + 5))
        
        if len(data) > 1:
            points = []
            min_t = data[0][0]
            max_t = data[-1][0]
            
            for t, val in data:
                if max_t > min_t:
                    nx = (t - min_t) / (max_t - min_t)
                else:
                    nx = 0.5
                px = graph_rect.left + nx * graph_rect.width
                
                if max_y > min_y:
                    ny = (val - min_y) / (max_y - min_y)
                else:
                    ny = 0.5
                ny = max(0, min(1, ny))
                py = graph_rect.bottom - ny * graph_rect.height
                
                points.append((px, py))
                
            pygame.draw.lines(screen, color, False, points, 2)

    def draw(self, screen, particle_engine, wave_model):
        pygame.draw.rect(screen, COLOR_PANEL, self.rect)
        
        # 1. Waveform Graph
        self._draw_graph(screen, "E-Field at Center", 10, wave_model.field_history, (0, 255, 255), -200, 200)
        
        # 2. Temperature vs Time
        self._draw_graph(screen, "Avg Temperature (°C)", 210, particle_engine.avg_temp_history, (255, 100, 50), 20, 100)
        
        # 3. Energy Absorption
        self._draw_graph(screen, "Power Absorbed (Arb. Units)", 410, particle_engine.power_absorbed_history, (150, 255, 100), 0, 1000)
