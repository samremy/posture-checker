# Posture Checker

A simple webcam-based posture detection app

---

## Overview
This project uses pose landmark detection to analyze the user's posture and provide real-time feedback. It is designed to be run in the background to help the user maintain good posture while working for long periods at their computer.

---

## Setup

### Requirements
- **Python 3.10** (required)
- A webcam

### Install Python

#### Option 1: Download From python.org
Download Python 3.10 from the official website:  
https://www.python.org/downloads/latest/python3.10/

#### Option 2: Install With Homebrew (macOS)
```bash 
brew install python@3.10
```

### Verify Python Installation

```bash
which python3.10 
python3.10 --version 
```

### Set Up a Virtual Environment

#### Create the Virtual Environment:

```bash
python3.10 -m venv venv
```

#### Activate It:

On macOS / Linux:

```bash
source venv/bin/activate 
```

On Windows:

```bash 
venv\Scripts\activate 
```

### Install Dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

---

## How to Use

### Step 1: Start the Program

```bash
python src/main.py
```

Upon startup, the setup menu will appear.

### Step 2: Position Yourself

Ensure:
- Your shoulders, neck, and head are all fully visible
- You are square to the webcam

You should see pose landmarks overlaid on the webcam feed.

### Step 3: Set Default Position

Sit in a comfortable, upright position and click "Set"

Your default posture is now set, and the program will begin detecting. If you intentionally slouch the program should detect your poor posture. 

### Step 4: Adjust Sensitivity

Use the slider to adjust the sensitivity value. This will differ from user to user. Find a comfortable value that suits you. 

You may repeat Step 3 at any time to set a new default posture.

### Step 5: Start Program

Press "Start"

The program will now begin running and the setup window will minimize. If the program detects poor posture while you are working, a pop-up warning message will appear in the top left coner of your screen. This message disappears when posture is corrected.

### Step 6: End Program

Restore the window and click "End" to close the program.

### Notes

For the best performance, it is recommended to keep the window minimized until you wish to close the program.

Lighting and camera placement can affect detection accuracy.

---

## Acknowledgments

This project uses MediaPipe, licenced under the Apache License 2.0  
https://github.com/google/mediapipe

---