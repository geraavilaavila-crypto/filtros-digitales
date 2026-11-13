import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
# Frecuencia de muestreo: 1000 Hz
fs = 1000
t = np.arange(0, 1.0, 1/fs)  # 1 segundo de señal
# Señal compuesta: 5 Hz + 50 Hz + 200 Hz
x_limpia = np.sin(2*np.pi*5*t) + 0.5*np.sin(2*np.pi*50*t) + 0.3*np.sin(2*np.pi*200*t)
# Ruido blanco
np.random.seed(0)
ruido = 0.4 * np.random.randn(len(t))
x_ruidosa = x_limpia + ruido
# --- 4. Graficar antes del filtrado ---
plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.plot(t, x_limpia)
plt.title('Señal compuesta limpia: 5 Hz + 50 Hz + 200 Hz')
plt.xlabel('Tiempo [s]')
plt.ylabel('Amplitud')
plt.grid(True)
plt.subplot(2, 1, 2)
plt.plot(t, x_ruidosa, color='orange', alpha=0.8)
plt.title('Señal compuesta + Ruido blanco')
plt.xlabel('Tiempo [s]')
plt.ylabel('Amplitud')
plt.grid(True)
plt.tight_layout()
plt.show()

# =====================================================
# PASO 2: Diseño de filtros IIR - Butterworth
# =====================================================
# --- Pasa-bajas: corte en 20 Hz, orden 4 ---
# Todo lo menor a 20 Hz pasa, lo demás se atenúa
sos_lp = signal.butter(4, 20, btype='lowpass', fs=fs, output='sos')
y_lp = signal.sosfiltfilt(sos_lp, x_ruidosa)
# --- Pasa-altas: corte en 100 Hz, orden 4 ---
# Todo lo mayor a 100 Hz pasa
sos_hp = signal.butter(4, 100, btype='highpass', fs=fs, output='sos')
y_hp = signal.sosfiltfilt(sos_hp, x_ruidosa)
# --- Pasa-banda: de 30 a 70 Hz, orden 4 ---
# Solo pasa lo que está entre 30 y 70 Hz, o sea el de 50 Hz
sos_bp = signal.butter(4, [30, 70], btype='bandpass', fs=fs, output='sos')
y_bp = signal.sosfiltfilt(sos_bp, x_ruidosa)
# --- Graficar resultados ---
plt.figure(figsize=(10, 8))
plt.subplot(3, 1, 1)
plt.plot(t, y_lp, color='green')
plt.title('Pasa-bajas Butterworth (corte 20 Hz) - Solo queda 5 Hz')
plt.ylabel('Amplitud'); plt.grid(True)
plt.subplot(3, 1, 2)
plt.plot(t, y_hp, color='red')
plt.title('Pasa-altas Butterworth (corte 100 Hz) - Solo queda 200 Hz')
plt.ylabel('Amplitud'); plt.grid(True)
plt.subplot(3, 1, 3)
plt.plot(t, y_bp, color='purple')
plt.title('Pasa-banda Butterworth (30-70 Hz) - Solo queda 50 Hz')
plt.xlabel('Tiempo [s]'); plt.ylabel('Amplitud'); plt.grid(True)
plt.tight_layout()
plt.show()
# =====================================================
# PASO 3: FIR con ventana + Chebyshev + Respuesta en frecuencia
# =====================================================

# --- 3A. FIR Pasa-bajas con ventana Hamming ---
# FIR = usa solo entradas pasadas, no tiene retroalimentación
# numtaps = 101 es el orden del filtro, entre más alto, más filoso el corte
fir_lp = signal.firwin(101, cutoff=20, window='hamming', fs=fs)
y_fir = signal.lfilter(fir_lp, 1.0, x_ruidosa)

# --- 3B. Chebyshev Tipo I Pasa-bajas ---
# Chebyshev I = más filoso que Butterworth, pero tiene rizado en la banda de paso
# rp = 1 dB de rizado permitido
sos_cheby = signal.cheby1(4, 1, 20, btype='lowpass', fs=fs, output='sos')
y_cheby = signal.sosfiltfilt(sos_cheby, x_ruidosa)

# --- Graficar FIR vs Chebyshev vs Butterworth ---
plt.figure(figsize=(10, 6))
plt.plot(t, y_lp, label='Butterworth (Paso 2)', alpha=0.7)
plt.plot(t, y_fir, label='FIR Hamming', alpha=0.7)
plt.plot(t, y_cheby, label='Chebyshev I', alpha=0.7)
plt.title('Comparación Pasa-bajas: Butterworth vs FIR vs Chebyshev')
plt.xlabel('Tiempo [s]'); plt.ylabel('Amplitud')
plt.legend(); plt.grid(True)
plt.tight_layout()
plt.show()

# --- 3C. Respuesta en frecuencia ---
# Esto es el Bode del filtro, para ver qué frecuencias deja pasar
w_lp, h_lp = signal.sosfreqz(sos_lp, worN=8000, fs=fs)
w_fir, h_fir = signal.freqz(fir_lp, worN=8000, fs=fs)
w_ch, h_ch = signal.sosfreqz(sos_cheby, worN=8000, fs=fs)

plt.figure(figsize=(10, 5))
plt.plot(w_lp, 20*np.log10(abs(h_lp)), label='Butterworth')
plt.plot(w_fir, 20*np.log10(abs(h_fir)), label='FIR Hamming')
plt.plot(w_ch, 20*np.log10(abs(h_ch)), label='Chebyshev I')
plt.title('Respuesta en frecuencia - Pasa-bajas 20 Hz')
plt.xlabel('Frecuencia [Hz]'); plt.ylabel('Magnitud [dB]')
plt.ylim(-80, 5); plt.xlim(0, 200)
plt.legend(); plt.grid(True)
plt.tight_layout()
plt.show()

print("Listo, Paso 3 completado")