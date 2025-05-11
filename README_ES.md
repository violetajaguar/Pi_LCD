# Jaguar-Eyes: IMX500 + MediaPipe Neon Trails

Este proyecto permite visualizar una cámara IMX500 en vivo con efectos de "neón" aplicados sobre landmarks de cuerpo usando **MediaPipe Pose**, desplegado tanto por HDMI como en una LCD SPI Waveshare de 2.4″ (controlada por el driver ILI9341).

## 📦 Requisitos

- Raspberry Pi con SPI activado
- Pantalla LCD Waveshare 2.4" (ILI9341)
- Cámara compatible con `libcamera-vid`
- Python 3.x
- Dependencias:
  - `opencv-python`
  - `numpy`
  - `mediapipe`
  - `Pillow`
  - `spidev`

## 🧠 Descripción del sistema

- **Sensor**: `libcamera-vid` captura frames YUV420 a 640x480.
- **Detección de pose**: Se usa `MediaPipe` para encontrar landmarks corporales.
- **Render "Neon"**: Se dibujan puntos magenta sobre un buffer de persistencia visual.
- **Salida**:
  - Pantalla HDMI (preview)
  - LCD SPI de 2.4” vía Pillow + SPI driver de Waveshare

## ⚙️ Estructura técnica

```text
┌────────────┐
│  Cámara    │ ──────▶ YUV420 ──────▶ OpenCV → MediaPipe
└────────────┘                              │
                                             ▼
                              Pose landmarks (x, y)
                                             │
                                             ▼
                             Trail buffer (neón magenta)
                                             │
                                             ▼
                           Frame final con efecto + glow
                           │               ▲
                           ▼               │
                   LCD SPI (Pillow)     HDMI (cv2.imshow)
```

## 🚀 Ejecución

Asegúrate de que el path al driver de la LCD esté correcto:

```python
driver_parent = "/home/jaguaress/LCD_Module_RPI_code/RaspberryPi/python"
```

Y ejecuta:

```bash
python3 jaguar_neon_lcd.py
```

Pulsa `q` en la ventana de HDMI para terminar.

## 📌 Notas técnicas

- Se establece `GPIOZERO_PIN_FACTORY=lgpio` para asegurar compatibilidad con la SPI.
- Se fija `QT_QPA_PLATFORM=xcb` para evitar errores con Wayland.
- El efecto visual "trailing neon" se genera mediante decaimiento exponencial sobre el buffer de trails.

## 🧼 Limpieza

El proceso `libcamera-vid` se termina correctamente al salir. También se libera la pantalla y se cierra la ventana de OpenCV.

---

Creado por [Violeta Jaguar] 🐆