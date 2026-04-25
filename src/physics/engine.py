import numpy as np
import pygame
from config import *

class ParticleEngine:
    def __init__(self, num_particles):
        self.num_particles = num_particles
        self.cavity_rect = pygame.Rect(300, 60, 680, 640)
        self._init_particles()
        
    def _init_particles(self, new_count=None):
        if new_count is not None:
            self.num_particles = new_count
            
        # x, y positions
        self.positions = np.random.rand(self.num_particles, 2)
        self.positions[:, 0] = self.positions[:, 0] * self.cavity_rect.width + self.cavity_rect.x
        self.positions[:, 1] = self.positions[:, 1] * self.cavity_rect.height + self.cavity_rect.y
        
        # velocities vx, vy
        self.velocities = (np.random.rand(self.num_particles, 2) - 0.5) * 50.0
        
        # Temperature (starts at 20 C)
        self.temperatures = np.ones(self.num_particles) * 20.0
        
        # Dipole angle (0 to 2pi)
        self.angles = np.random.rand(self.num_particles) * 2 * np.pi
        
        # History for graphs
        self.avg_temp_history = []
        self.power_absorbed_history = []
        self.time_elapsed = 0.0

    def set_bounds(self, rect):
        self.cavity_rect = rect
        self.positions[:, 0] = np.clip(self.positions[:, 0], rect.left, rect.right)
        self.positions[:, 1] = np.clip(self.positions[:, 1], rect.top, rect.bottom)

    def update(self, dt, wave_model, params):
        if abs(self.num_particles - params['density']) > 10:
            self._init_particles(params['density'])
            
        speed_mult = params['speed']
        dt_scaled = dt * speed_mult
        self.time_elapsed += dt_scaled

        # 1. Brownian Motion
        self.positions += self.velocities * dt_scaled
        
        # Random velocity perturbations
        self.velocities += (np.random.rand(self.num_particles, 2) - 0.5) * 20.0 * dt_scaled
        self.velocities *= 0.99 # Friction
        
        # Boundary collisions
        out_left = self.positions[:, 0] < self.cavity_rect.left
        out_right = self.positions[:, 0] > self.cavity_rect.right
        out_top = self.positions[:, 1] < self.cavity_rect.top
        out_bottom = self.positions[:, 1] > self.cavity_rect.bottom
        
        self.positions[out_left, 0] = self.cavity_rect.left
        self.velocities[out_left, 0] *= -1
        self.positions[out_right, 0] = self.cavity_rect.right
        self.velocities[out_right, 0] *= -1
        self.positions[out_top, 1] = self.cavity_rect.top
        self.velocities[out_top, 1] *= -1
        self.positions[out_bottom, 1] = self.cavity_rect.bottom
        self.velocities[out_bottom, 1] *= -1

        # 2. Microwave Interaction
        e_field_y = wave_model.get_field(self.positions[:, 0], self.time_elapsed)
        
        target_angles = np.where(e_field_y > 0, np.pi/2, -np.pi/2)
        angle_diff = target_angles - self.angles
        angle_diff = (angle_diff + np.pi) % (2 * np.pi) - np.pi
        
        field_strength = np.abs(e_field_y) / (params['amp'] + 1e-6)
        
        self.angles += angle_diff * 5.0 * dt_scaled * field_strength
        self.angles += (np.random.rand(self.num_particles) - 0.5) * 2.0 * dt_scaled
        
        # 3. Heating
        heating_factor = params['power'] / 800.0
        energy_absorbed = np.abs(angle_diff) * field_strength * dt_scaled * 15.0 * heating_factor
        self.temperatures += energy_absorbed
        
        # Cooling
        self.temperatures -= (self.temperatures - 20.0) * 0.05 * dt_scaled
        
        # Temp cap
        self.temperatures = np.clip(self.temperatures, 20.0, 500.0)
        
        # 4. Particle Collisions
        radius = 6.0
        diam_sq = (radius * 2.0)**2
        diff = self.positions[:, np.newaxis, :] - self.positions[np.newaxis, :, :]
        dist_sq = np.sum(diff**2, axis=-1)
        np.fill_diagonal(dist_sq, np.inf)
        
        colliding = dist_sq < diam_sq
        if np.any(colliding):
            dist = np.sqrt(dist_sq)
            overlap = np.maximum(0, (2.0 * radius) - dist)
            direction = diff / (dist[..., np.newaxis] + 1e-6)
            repulsion = np.sum(direction * overlap[..., np.newaxis], axis=1) * 200.0
            self.velocities += repulsion * dt_scaled
        
        # Record stats
        self.avg_temp_history.append((self.time_elapsed, np.mean(self.temperatures)))
        if len(self.avg_temp_history) > 200:
            self.avg_temp_history.pop(0)
            
        total_power = np.sum(energy_absorbed)
        self.power_absorbed_history.append((self.time_elapsed, total_power))
        if len(self.power_absorbed_history) > 200:
            self.power_absorbed_history.pop(0)
