import numpy as np

class WaveModel:
    def __init__(self, freq, amplitude):
        self.freq = freq
        self.amplitude = amplitude
        self.phase = 0.0
        self.wavelength = 300.0 / freq
        self.time = 0.0
        
        self.field_history = []
        
    def update(self, dt, params):
        self.freq = params['freq']
        self.amplitude = params['amp']
        self.wavelength = 500.0 / self.freq
        
        dt_scaled = dt * params['speed']
        self.time += dt_scaled
        
        center_x = 300 + 340
        field_val = self.get_field(np.array([center_x]), self.time)[0]
        
        self.field_history.append((self.time, field_val))
        if len(self.field_history) > 200:
            self.field_history.pop(0)

    def get_field(self, x, t):
        k = 2.0 * np.pi / self.wavelength
        x_local = x - 300
        
        spatial_part = np.sin(k * x_local)
        temporal_part = np.cos(self.freq * np.pi * 2.0 * t)
        
        return self.amplitude * spatial_part * temporal_part
