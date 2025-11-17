import numpy as np
import matplotlib.pyplot as plt

# Konstanten
kappa0 = 23.6e6       # Leitfähigkeit in S/m
gamma = 1.5e14        # Dämpfungskonstante im Drude-Modell
mu = 4 * np.pi * 1e-7 # magnetische Permeabilität (H/m)

# Frequenzbereich (logarithmisch)
omega = np.logspace(9, 17, 500)

# Eindringtiefe bei konstanter Leitfähigkeit
delta_const = np.sqrt(2 / (mu * kappa0 * omega))

# Reeller Teil der Drude-Leitfähigkeit
kappa_real = kappa0 / (1 + (omega / gamma)**2)

# Eindringtiefe im Drude-Modell
delta_drude = np.sqrt(2 / (mu * kappa_real * omega))

# Plot
plt.figure(figsize=(8, 5))
plt.loglog(omega, delta_const, label="Konstante Leitfähigkeit")
plt.loglog(omega, delta_drude, label="Drude-Modell")

plt.xlabel(r'$\omega$ (rad/s)')
plt.ylabel(r'$\delta(\omega)$ (m)')
plt.title('Eindringtiefe δ(ω) – Konstante Leitfähigkeit vs. Drude-Modell')
plt.legend()
plt.grid(True, which="both", linestyle="--")
plt.show()
