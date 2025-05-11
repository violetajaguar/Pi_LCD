#!/usr/bin/python3
"""
Jaguar-Eyes: IMX500 live feed + MediaPipe neon trails
→ HDMI preview + 2.4″ Waveshare ILI9341 LCD
"""

# ---------- fix GPIO Zero pin-factory and Qt backend BEFORE imports ----------
import os
os.environ.setdefault("GPIOZERO_PIN_FACTORY", "lgpio")        # use lgpio first  :contentReference[oaicite:3]{index=3}
os.environ.setdefault("QT_QPA_PLATFORM", "xcb")               # avoid wayland plug-in error  :contentReference[oaicite:4]{index=4}

import sys, pathlib, subprocess, cv2, numpy as np, mediapipe as mp
from PIL import Image
import spidev as SPI

# ---------- Waveshare driver path (parent of lib/) ----------
driver_parent = "/home/jaguaress/LCD_Module_RPI_code/RaspberryPi/python"
sys.path.append(driver_parent)
from lib import LCD_2inch4                                                    # driver OK

# ---------- LCD init (Waveshare demo style) ----------
spi = SPI.SpiDev(0, 0)          # CE0; use (0,1) if your CS wire on pin 26
spi.max_speed_hz = 32_000_000   # drop to 16 MHz if long jumpers
lcd  = LCD_2inch4.LCD_2inch4(spi      = spi,
                             spi_freq = 32_000_000,
                             rst      = 27, dc = 25, bl = 18)
lcd.Init(); lcd.bl_DutyCycle(80); lcd.clear()

# ---------- libcamera-vid raw YUV420 pipe ----------
cmd  = ["libcamera-vid","--inline","--nopreview","-t","0",
        "--codec","yuv420","--width","640","--height","480","-o","-"]
pipe = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=10**8)

# ---------- MediaPipe Pose + neon-trail buffer ----------
pose   = mp.solutions.pose.Pose()
trail  = np.zeros((480,640,3), np.uint8)
BYTES  = 640*480*3//2                      # 460 800

try:
    while True:
        buf = pipe.stdout.read(BYTES)
        if len(buf) != BYTES:
            continue

        yuv   = np.frombuffer(buf, np.uint8).reshape((720,640))
        frame = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR_I420)     # YUV→BGR  :contentReference[oaicite:5]{index=5}

        res = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if res.pose_landmarks:
            for lm in res.pose_landmarks.landmark:
                cv2.circle(trail, (int(lm.x*640), int(lm.y*480)),
                           5, (255,0,255), -1)                # neon magenta dot

        trail[:] = cv2.addWeighted(trail, 0.92,
                                   np.zeros_like(trail), 0.08, 0)  # after-glow

        blended = cv2.addWeighted(frame,0.6,trail,1.2,0)

        # -------- push to LCD --------
        img = Image.fromarray(cv2.cvtColor(blended, cv2.COLOR_BGR2RGB))
        img = img.resize((lcd.width,lcd.height), Image.BILINEAR)
        lcd.ShowImage(img)

        # HDMI preview
        cv2.imshow("Jaguar Eyes – Neon Trails", blended)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    pipe.terminate(); cv2.destroyAllWindows(); lcd.module_exit()
