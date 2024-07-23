import numpy as np
import matplotlib.pyplot as plt

# Définir la fonction pour générer des ondes alpha avec bruit
def generate_alpha_wave(frequency, amplitude, sampling_rate, duration, noise_level=0):
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
    alpha_wave = amplitude * np.sin(2 * np.pi * frequency * t)
    if noise_level > 0:
        alpha_wave += noise_level * np.random.randn(len(t))
    return t, alpha_wave

# Paramètres
sampling_rate = 256  # Échantillons par seconde
duration = 10  # Durée en secondes
frequency = 10  # Fréquence des ondes alpha en Hz
amplitude_alpha1 = 0.5  # Amplitude de alpha1
amplitude_alpha2 = 0.1  # Amplitude de alpha2
noise_level = 0.2  # Niveau de bruit

# Générer les ondes alpha sans bruit
t, alpha1_no_noise = generate_alpha_wave(frequency, amplitude_alpha1, sampling_rate, duration)
_, alpha2_no_noise = generate_alpha_wave(frequency, amplitude_alpha2, sampling_rate, duration)

# Générer les ondes alpha avec bruit
_, alpha1_with_noise = generate_alpha_wave(frequency, amplitude_alpha1, sampling_rate, duration, noise_level)
_, alpha2_with_noise = generate_alpha_wave(frequency, amplitude_alpha2, sampling_rate, duration, noise_level)

# Conditions
condition1 = amplitude_alpha1 > 0.1
condition2 = amplitude_alpha2 > 0.9

# Afficher les résultats
plt.figure(figsize=(12, 8))

# Alpha1 sans bruit
plt.subplot(2, 2, 1)
plt.plot(t, alpha1_no_noise)
plt.title(f'Alpha1 sans bruit (Amplitude = {amplitude_alpha1})')

# Alpha2 sans bruit
plt.subplot(2, 2, 2)
plt.plot(t, alpha2_no_noise)
plt.title(f'Alpha2 sans bruit (Amplitude = {amplitude_alpha2})')

# Alpha1 avec bruit
plt.subplot(2, 2, 3)
plt.plot(t, alpha1_with_noise)
plt.title(f'Alpha1 avec bruit (Amplitude = {amplitude_alpha1}, Bruit = {noise_level})')

# Alpha2 avec bruit
plt.subplot(2, 2, 4)
plt.plot(t, alpha2_with_noise)
plt.title(f'Alpha2 avec bruit (Amplitude = {amplitude_alpha2}, Bruit = {noise_level})')

plt.tight_layout()
plt.show()

# Comparaison des conditions
print(f"Condition 1 (Alpha1 > 0.1): {condition1}")
print(f"Condition 2 (Alpha2 > 0.9): {condition2}")

# Vérification des résultats avec et sans bruit
alpha1_meets_condition1 = np.max(np.abs(alpha1_no_noise)) > 0.1
alpha2_meets_condition2 = np.max(np.abs(alpha2_no_noise)) > 0.9

alpha1_with_noise_meets_condition1 = np.max(np.abs(alpha1_with_noise)) > 0.1
alpha2_with_noise_meets_condition2 = np.max(np.abs(alpha2_with_noise)) > 0.9

print("\nSans bruit:")
print(f"Alpha1 respecte la condition 1: {alpha1_meets_condition1}")
print(f"Alpha2 respecte la condition 2: {alpha2_meets_condition2}")

print("\nAvec bruit:")
print(f"Alpha1 respecte la condition 1: {alpha1_with_noise_meets_condition1}")
print(f"Alpha2 respecte la condition 2: {alpha2_with_noise_meets_condition2}")
