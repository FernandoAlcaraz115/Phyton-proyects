import numpy as np
import matplotlib.pyplot as plt

# Constante de decaimiento
k = -0.00012097

# Rango de tiempo (de 0 a 20,000 años)
t = np.linspace(0, 20000, 1000)

# Función de decaimiento
A_ratio = np.exp(k * t)

# Punto de interés: t = 15,960 años
t_point = 15960
A_point = np.exp(k * t_point)

# Crear la gráfica
plt.figure(figsize=(10, 6))
plt.plot(t, A_ratio, label=r"$\frac{A(t)}{A_0} = e^{-0.00012097t}$")
plt.scatter(t_point, A_point, color='red', label=f"t = {t_point} años, A(t)/A0 = {A_point:.3f}")
plt.axhline(y=0.145, color='gray', linestyle='--', label="14.5% de C-14 restante")
plt.axvline(x=t_point, color='gray', linestyle='--')

# Etiquetas y título
plt.title("Decaimiento del carbono-14")
plt.xlabel("Tiempo (años)")
plt.ylabel(r"$\frac{A(t)}{A_0}$")
plt.legend()
plt.grid(True)
plt.show()