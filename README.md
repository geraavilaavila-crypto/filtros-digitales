# filtros-digitales
Actividad 3 señales y sistemas filtros digitales en Python

## Objetivo
Diseñar filtros digitales pasa-bajas, pasa-altas y pasa-banda para analizar señales con ruido.

## ¿Qué hace el código?
1. **Crea una señal de prueba:** 5 Hz + 50 Hz + 200 Hz + ruido blanco
2. **Diseña filtros Butterworth IIR:** pasa-bajas (20 Hz), pasa-altas (100 Hz), pasa-banda (30-70 Hz)
3. **Diseña FIR con ventana Hamming** y **Chebyshev Tipo I** para comparar
4. **Grafica** la señal antes y después del filtrado y la respuesta en frecuencia

## ¿Cómo correrlo?
```bash
pip install numpy scipy matplotlib
python filtros.py

## Resultados
- Pasa-bajas: eliminó el ruido y dejó solo 5 Hz
- Pasa-banda: dejó solo 50 Hz
- Pasa-altas: dejó 200 Hz pero también dejó pasar el ruido, por eso es menos efectivo contra ruido blanco
- FIR Hamming: la transición más abrupta
- Chebyshev: transición intermedia con rizado
