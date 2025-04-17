# Air-Canvas
A real-time computer vision project that allows users to draw in the air using hand gestures. Built using Python, OpenCV, and MediaPipe, this interactive tool detects finger movements through your webcam and turns them into digital strokes on a canvas — without touching the screen!


#  Air Canvas – Virtual Hand Gesture Drawing App

A real-time computer vision project that allows users to draw in the air using hand gestures. Built using Python, OpenCV, and MediaPipe, this interactive tool detects finger movements through your webcam and turns them into digital strokes on a canvas — without touching the screen!

##  Features

-  Draw using your **index finger** gesture  
-  Change drawing color using **two fingers (index + middle)**  
-  Undo the last stroke using **three fingers (index + middle + ring)**  
-  Save your drawing as a PNG image  
-  Clear the canvas anytime with a key press  
-  Real-time webcam-based hand tracking  

##  Technologies Used

- **Python 3**  
- **OpenCV** – For video capture, drawing, and GUI  
- **MediaPipe** – For fast and accurate hand landmark detection  
- **NumPy** – For creating and managing the drawing canvas  

##  How It Works

1. Webcam captures video in real-time.  
2. MediaPipe detects hand and identifies 21 key landmarks.  
3. Finger gestures are interpreted:  
   - 1 finger → Draw  
   - 2 fingers → Change color  
   - 3 fingers → Undo  
4. Lines are drawn on a NumPy canvas and overlaid on the webcam feed.  
5. Keyboard options allow clearing or saving the canvas.  

## 🖥️ Setup & Run

```bash
# Clone the repository
git clone https://github.com/your-username/air-canvas.git
cd air-canvas

# Install dependencies
pip install opencv-python mediapipe numpy

# Run the application
python Air_canvas.py
