# Jaguar-Eyes: IMX500 + MediaPipe Neon Trails

This project enables real-time visualization of an IMX500 camera feed with glowing neon effects applied to body landmarks detected using **MediaPipe Pose**. The processed video is displayed both via HDMI and on a 2.4″ SPI Waveshare LCD (ILI9341 driver).

## 📦 Requirements

- Raspberry Pi with SPI enabled
- Waveshare 2.4" LCD (ILI9341)
- Camera compatible with `libcamera-vid`
- Python 3.x
- Dependencies:
  - `opencv-python`
  - `numpy`
  - `mediapipe`
  - `Pillow`
  - `spidev`

## 🧠 System Description

- **Sensor**: Captures YUV420 frames at 640x480 using `libcamera-vid`.
- **Pose Detection**: Detects pose landmarks using `MediaPipe`.
- **Neon Rendering**: Draws magenta dots on a persistence buffer to simulate neon trails.
- **Output**:
  - HDMI (for preview)
  - LCD SPI display (using Pillow and the Waveshare driver)

## ⚙️ Technical Architecture

```text
┌────────────┐
│  Camera    │ ──────▶ YUV420 ──────▶ OpenCV → MediaPipe
└────────────┘                              │
                                             ▼
                              Pose landmarks (x, y)
                                             │
                                             ▼
                             Trail buffer (neon magenta)
                                             │
                                             ▼
                           Final frame with glow effect
                           │               ▲
                           ▼               │
                   LCD SPI (Pillow)     HDMI (cv2.imshow)
```

## 🚀 Running the Script

Ensure the driver path is correctly set:

```python
driver_parent = "/home/jaguaress/LCD_Module_RPI_code/RaspberryPi/python"
```

Then run:

```bash
python3 jaguar_neon_lcd.py
```

Press `q` in the HDMI preview window to quit.

## 📌 Technical Notes

- `GPIOZERO_PIN_FACTORY=lgpio` is used for proper SPI pin factory setup.
- `QT_QPA_PLATFORM=xcb` avoids Wayland plugin errors.
- The neon effect uses exponential decay on the trail buffer for visual persistence.

## 🧼 Cleanup

The `libcamera-vid` process is terminated properly on exit. LCD and OpenCV windows are also cleaned up.

---

Created by [Violeta Jaguar] 🐆