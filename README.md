# PostureChecker

A simple webcam-based posture detection app

---

## Overview
This project uses pose landmark detection to analyze the user's posture and provide real-time feedback. It is designed to be run in the background to help the user maintain good posture while working for long periods at their computer.

---

## Setup and Usage
This project requires python 3.10.
You can download the latest compatible version here: https://www.python.org/downloads/latest/python3.10/

Or install using brew on macOS:
```bash 
brew install python@3.10
```

Create venv:
```bash 
python3.10 -m venv venv
```

On macOS / Linux: 
```bash
source venv/bin/activate
```

On Windows:
```bash
venv\Scripts\activate
```

Install dependencies:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```