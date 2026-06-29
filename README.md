# ✋ Gesture Control for macOS

Control your Mac's **volume** and **screen brightness** using hand gestures with **MediaPipe** and **OpenCV**.

## ✨ Features

* 🎵 Left hand controls **Volume**
* 💡 Right hand controls **Brightness**
* ✊ Fist gesture locks controls
* 📷 Real-time hand tracking
* ⚡ Smooth gesture mapping with configurable sensitivity

## 🛠️ Tech Stack

* Python
* OpenCV
* MediaPipe
* NumPy

## 📁 Project Structure

```text
gesture/
├── main.py
├── hand_detector.py
├── controller.py
├── hud.py
├── config.json
└── requirements.txt
```

## 🚀 Installation

```bash
git clone https://github.com/nishthaadatiya/gesture_control.pyproject.git
cd gesture_control.pyproject

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

If you don't have a `requirements.txt`:

```bash
pip install opencv-python mediapipe==0.10.14 numpy screen-brightness-control
```

## ▶️ Run

```bash
python main.py
```

## 🖐️ Controls

| Gesture          | Action     |
| ---------------- | ---------- |
| Left hand pinch  | Volume     |
| Right hand pinch | Brightness |
| Fist             | Lock/Pause |
| Q                | Quit       |

## ⚙️ Configuration

Adjust gesture sensitivity in `config.json`.

## 📌 Notes

* Works on **macOS (Apple Silicon)**.
* Grant **Camera** and **Automation** permissions to Terminal if prompted.
* Uses `mediapipe==0.10.14`.

## 📄 License

Educational project.
