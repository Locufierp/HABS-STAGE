def generate_dummy_eeg_data(self, params, buffer_duration):
        """
        Méthodes de params amener pour simuler les donées EEG
        """
        # Extract parameters from JSON dictionary
        num_channels = params.get("eeg_channels", 8)
        samples_per_second = params.get("sampling_rate", 256)
        epoch_period = buffer_duration
        noise_level = params.get("noise", 1)
        artifact_prob = params.get("artifacts", 0.01)
        modulation_type = params.get("modulation_type", 'sinusoidal')
        # 
        preset = params.get("preset", None)
        sequence = params.get("sequence", None)
        correlation_strength = params.get("correlation_strength", 0.5)  # Strength of correlation between nearby channels
        power_law_slope = params.get("power_law_slope", 1.0)

        # Preset amplitude settings
        preset_settings = {
            #           del  the  alp  bet  gam
            'focus':   [0.1, 0.1, 0.5, 0.8, 0.4],
            'alert':   [0.1, 0.1, 0.4, 0.9, 0.3],
            'relaxed': [0.2, 0.2, 0.7, 0.3, 0.2],
            'drowsy':  [0.4, 0.6, 0.2, 0.2, 0.1],
        }

        if preset in preset_settings:
            delta_amp, theta_amp, alpha_amp, beta_amp, gamma_amp = preset_settings[preset]
        else:
            delta_amp = params.get("delta_amp", 0.1)
            theta_amp = params.get("theta_amp", 0.1)
            alpha_amp = params.get("alpha_amp", 0.1)
            beta_amp = params.get("beta_amp", 0.1)
            gamma_amp = params.get("gamma_amp", 0.1)
        
        total_samples = samples_per_second * epoch_period
        t = np.linspace(0, epoch_period, total_samples, endpoint=False)
        eeg_data = np.zeros((num_channels, total_samples))

        # Frequency bands
        bands = {
            'Delta': (0.5, 4),
            'Theta': (4, 8),
            'Alpha': (8, 13),
            'Beta': (13, 30),
            'Gamma': (30, 100)
        }

        amplitudes = {
            'Delta': delta_amp,
            'Theta': theta_amp,
            'Alpha': alpha_amp,
            'Beta': beta_amp,
            'Gamma': gamma_amp
        }

        # Managing the type of EEG modulation
        if modulation_type == 'sinusoidal':
            modulating_freq = 0.1  # frequency of the amplitude modulation
            delta_mod = (1 + np.sin(2 * np.pi * modulating_freq * t)) / 2  # between 0.5 and 1.5
            theta_mod = (1 + np.cos(2 * np.pi * modulating_freq * t)) / 2
            alpha_mod = (1 + np.sin(2 * np.pi * modulating_freq * t + np.pi / 4)) / 2
            beta_mod = (1 + np.cos(2 * np.pi * modulating_freq * t + np.pi / 4)) / 2
            gamma_mod = (1 + np.sin(2 * np.pi * modulating_freq * t + np.pi / 2)) / 2
        elif modulation_type == 'random':
            delta_mod = np.abs(np.random.randn(total_samples))
            theta_mod = np.abs(np.random.randn(total_samples))
            alpha_mod = np.abs(np.random.randn(total_samples))
            beta_mod = np.abs(np.random.randn(total_samples))
            gamma_mod = np.abs(np.random.randn(total_samples))
        
        for band, (low, high) in bands.items():
            amplitude = amplitudes[band]
            freqs = np.linspace(low, high, int(samples_per_second / 2))
            power_law = freqs ** -power_law_slope

            for i in range(num_channels):
                for f, p in zip(freqs, power_law):
                    phase = np.random.uniform(0, 2 * np.pi)
                    if band == 'Delta':
                        eeg_data[i] += amplitude * p * delta_mod * np.sin(2 * np.pi * f * t + phase)
                    elif band == 'Theta':
                        eeg_data[i] += amplitude * p * theta_mod * np.sin(2 * np.pi * f * t + phase)
                    elif band == 'Alpha':
                        eeg_data[i] += amplitude * p * alpha_mod * np.sin(2 * np.pi * f * t + phase)
                    elif band == 'Beta':
                        eeg_data[i] += amplitude * p * beta_mod * np.sin(2 * np.pi * f * t + phase)
                    elif band == 'Gamma':
                        eeg_data[i] += amplitude * p * gamma_mod * np.sin(2 * np.pi * f * t + phase)

        # Adding random noise
        eeg_data += noise_level * np.random.randn(num_channels, total_samples)

        # Introducing correlation between nearby channels
        for channel in range(1, num_channels):
            eeg_data[channel] += correlation_strength * eeg_data[channel - 1]

        # Introducing artifacts as random peaks
        artifact_indices = np.random.choice(total_samples, int(artifact_prob * total_samples), replace=False)
        for channel in range(0, num_channels):
            eeg_data[channel, artifact_indices] -= np.random.uniform(10, 20, len(artifact_indices))

        # Handle sequence if provided
        if sequence:
            full_data = []
            for seq in sequence:
                preset, duration = seq
                temp_params = params.copy()
                temp_params['preset'] = preset
                temp_params['epoch_period'] = duration
                temp_params['sequence'] = None
                segment = generate_dummy_eeg_data(temp_params)
                full_data.append(segment)
            eeg_data = np.hstack(full_data)

        return eeg_data