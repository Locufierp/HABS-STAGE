import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch

class EEGGenerator:
    def __init__(self):
        self.preset_settings = {
            'focus':   [0.1, 0.1, 0.5, 0.8, 0.4],
            'alert':   [0.1, 0.1, 0.4, 0.9, 0.3],
            'relaxed': [0.2, 0.2, 0.7, 0.3, 0.2],
            'drowsy':  [0.4, 0.6, 0.2, 0.2, 0.1],
        }

        self.bands = {
            'Delta': (0.5, 4),
            'Theta': (4, 8),
            'Alpha': (8, 13),
            'Beta': (13, 30),
            'Gamma': (30, 100)
        }
    
    def _get_modulation(self, modulation_type, t, total_samples):
        if modulation_type == 'sinusoidal':
            modulating_freq = 0.1
            return (
                (1 + np.sin(2 * np.pi * modulating_freq * t)) / 2,
                (1 + np.cos(2 * np.pi * modulating_freq * t)) / 2,
                (1 + np.sin(2 * np.pi * modulating_freq * t + np.pi / 4)) / 2,
                (1 + np.cos(2 * np.pi * modulating_freq * t + np.pi / 4)) / 2,
                (1 + np.sin(2 * np.pi * modulating_freq * t + np.pi / 2)) / 2
            )
        elif modulation_type == 'random':
            return (
                np.abs(np.random.randn(total_samples)),
                np.abs(np.random.randn(total_samples)),
                np.abs(np.random.randn(total_samples)),
                np.abs(np.random.randn(total_samples)),
                np.abs(np.random.randn(total_samples))
            )
    
    def _generate_band_data(self, band, freqs, power_law, amplitudes, t, num_channels):
        band_data = np.zeros((num_channels, len(t)))
        for i in range(num_channels):
            for f, p in zip(freqs, power_law):
                phase = np.random.uniform(0, 2 * np.pi)
                modulation = self._get_modulation('sinusoidal', t, len(t))[list(self.bands.keys()).index(band)]
                band_data[i] += amplitudes[band] * p * modulation * np.sin(2 * np.pi * f * t + phase)
        return band_data
    
    def _add_artifacts(self, eeg_data, artifact_prob):
        total_samples = eeg_data.shape[1]
        artifact_indices = np.random.choice(total_samples, int(artifact_prob * total_samples), replace=False)
        for channel in range(eeg_data.shape[0]):
            eeg_data[channel, artifact_indices] -= np.random.uniform(10, 20, len(artifact_indices))
        return eeg_data
    
    def _introduce_correlation(self, eeg_data, correlation_strength):
        for channel in range(1, eeg_data.shape[0]):
            eeg_data[channel] += correlation_strength * eeg_data[channel - 1]
        return eeg_data
    
    def generate_dummy_eeg_data(self, params, buffer_duration):
        num_channels = params.get("eeg_channels", 8)
        samples_per_second = params.get("sampling_rate", 256)
        noise_level = params.get("noise", 1)
        artifact_prob = params.get("artifacts", 0.01)
        modulation_type = params.get("modulation_type", 'sinusoidal')
        preset = params.get("preset", None)
        sequence = params.get("sequence", None)
        correlation_strength = params.get("correlation_strength", 0.5)
        power_law_slope = params.get("power_law_slope", 1.0)

        if preset in self.preset_settings:
            delta_amp, theta_amp, alpha_amp, beta_amp, gamma_amp = self.preset_settings[preset]
        else:
            delta_amp = params.get("delta_amp", 0.1)
            theta_amp = params.get("theta_amp", 0.1)
            alpha_amp = params.get("alpha_amp", 0.1)
            beta_amp = params.get("beta_amp", 0.1)
            gamma_amp = params.get("gamma_amp", 0.1)
        
        amplitudes = {
            'Delta': delta_amp,
            'Theta': theta_amp,
            'Alpha': alpha_amp,
            'Beta': beta_amp,
            'Gamma': gamma_amp
        }

        total_samples = samples_per_second * buffer_duration
        t = np.linspace(0, buffer_duration, total_samples, endpoint=False)
        eeg_data = np.zeros((num_channels, total_samples))

        for band, (low, high) in self.bands.items():
            freqs = np.linspace(low, high, int(samples_per_second / 2))
            power_law = freqs ** -power_law_slope
            band_data = self._generate_band_data(band, freqs, power_law, amplitudes, t, num_channels)
            eeg_data += band_data

        eeg_data += noise_level * np.random.randn(num_channels, total_samples)
        eeg_data = self._introduce_correlation(eeg_data, correlation_strength)
        eeg_data = self._add_artifacts(eeg_data, artifact_prob)

        if sequence:
            full_data = []
            for seq in sequence:
                preset, duration = seq
                temp_params = params.copy()
                temp_params['preset'] = preset
                temp_params['epoch_period'] = duration
                temp_params['sequence'] = None
                segment = self.generate_dummy_eeg_data(temp_params, duration)
                full_data.append(segment)
            eeg_data = np.hstack(full_data)

        return eeg_data

    def plot_psd(self, eeg_data, sampling_rate):
        num_channels = eeg_data.shape[0]
        plt.figure(figsize=(12, 8))
        
        for i in range(num_channels):
            f, Pxx = welch(eeg_data[i], fs=sampling_rate, nperseg=1024)
            plt.semilogy(f, Pxx, label=f'Channel {i+1}')
        
        plt.title('Power Spectral Density (PSD) of EEG Data')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Power/Frequency (dB/Hz)')
        plt.legend()
        plt.grid()
        plt.show()
