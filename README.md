# **ScreenMouseAI**

ScreenMouseAI is an automation tool that captures your screen, analyzes it using Google Gemini AI, and moves your mouse according to the detected answers.
It is designed for quizzes, visual tests, UI automation, or any task where an AI-generated answer must be converted into mouse movement.

---

## 🚀 Features

* Full-screen capture using **mss**
* Image analysis powered by **Google Gemini**
* Mouse control: move, scroll, navigate in 4 directions
* Smooth curved mouse movement (Bezier)
* Hotkey-based activation (**F9**)
* Safe exit mechanism (**ESC → F9**)
* Supports Windows / Linux / macOS
* Works with:

  * Multiple-choice answers (A, B, C, D, E, F)
  * TRUE/FALSE questions
  * Multi-answer formats like: `a,c,d`

---

## 📦 Project Structure

```
ScreenMouseAI/
│
├── main.py             # Main script
├── config.py           # Configuration, environment variables, AI prompt
├── .env                # Gemini API key (not in repo)
├── pyproject.toml      # Dependencies (managed by uv)
├── uv.lock
├── .gitignore
├── .python-version
└── README.md
```

---

## 🔧 Installation

### 1. Clone the repository

```bash
git clone https://github.com/username/ScreenMouseAI.git
cd ScreenMouseAI
```

### 2. Create a virtual environment

```bash
uv venv
# For Linux
source .venv/bin/activate

# For Windows
.venv/Scripts/activate
```

### 3. Install dependencies

```bash
uv sync
```

---

## 🔑 Environment Setup

Create a `.env` file in the project root:

```
GEMINI_API_KEY=your_key_here
```

The key is automatically loaded by `config.py`:

```python
from dotenv import load_dotenv
load_dotenv()
```

---

## ▶️ Running the Application

Start the script:

```bash
python main.py
```

You’ll see:

```
Script ready (True=Up, False=Down). Press F9.
```

### ⌨️ Hotkeys

| Key          | Action                                             |
| ------------ | -------------------------------------------------- |
| **F9**       | Capture screen → send to AI → perform mouse action |
| **ESC**      | Enter exit confirmation mode                       |
| **ESC → F9** | Quit the program                                   |

---

## 🧠 Answer Interpretation Logic

Gemini should return answers line by line.

### ✔ Supported formats:

#### Multiple-choice:

```
a
b
c,d
f
```

#### True/False:

```
TRUE
FALSE
```

### ✔ Mouse actions mapping

| Answer    | Action      |
| --------- | ----------- |
| **A**     | Move Up     |
| **B**     | Move Right  |
| **C**     | Move Down   |
| **D**     | Move Left   |
| **E**     | Scroll Down |
| **F**     | Scroll Up   |
| **TRUE**  | Move Up     |
| **FALSE** | Move Down   |

---

## 🐁 Smooth Mouse Movement

Mouse movement uses a quadratic Bezier curve to simulate natural, human-like motion:

```python
move_mouse_smoothly_curved(dx, dy)
```

Configurable via:

* `MOVE_DURATION`
* `CURVE_STRENGTH`
* `MOVE_PIXELS`

---

## ⚙️ Configuration (config.py)

Available settings:

```python
GEMINI_API_KEY
MODEL_VERSION
MOVE_PIXELS
PAUSE_BETWEEN_QUESTIONS
PAUSE_BETWEEN_ACTIONS
MOVE_DURATION
CURVE_STRENGTH
FORCE_RESET_TIMEOUT
PROMPT
```

---

## ⚠️ Linux Users (Wayland)

Wayland breaks mouse automation.
The script automatically warns you:

```
!!! WARNING: Wayland detected !!! Switch to Xorg.
```

Switch to **Xorg** for full functionality.

---

## 📄 License

MIT License

---

## 👤 Author

**Nurdaulet** — Software Engineer
Project: **ScreenMouseAI**

