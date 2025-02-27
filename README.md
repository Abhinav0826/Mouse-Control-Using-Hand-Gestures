# Mouse Control Using Hand Gestures

A Machine Learning-based project that enables mouse control using hand gestures. This system allows users to move the mouse, perform left-click, right-click, double-click, and take screenshots using hand gestures detected through a webcam.


## Features

-  Move the mouse cursor using hand gestures
- Left-click, right-click, and double-click with finger gestures
- Take screenshots using a specific hand gesture
- Sales Insights: Identified top-selling products and seasonal demand spikes.
- Uses MediaPipe, OpenCV, and PyAutoGUI for smooth hand tracking

## Demo Video



## How It Works  

**Hand Landmarks Detection:** Uses MediaPipe to detect **21 hand landmarks** in real-time.  

**Mouse Control:** The index finger position determines cursor movement.  

**Clicking Actions:**  
- **Left Click:** (Thumb open, index finger closed, middle finger open)  
- **Right Click:** (Thumb open, index finger open, middle finger closed)  
- **Double Click:** (Thumb open, index and middle fingers closed)  
- **Screenshot:** (Thumb, index, and middle fingers closed)  


## Tech Stack

- Python
- OpenCV (cv2)
- Mediapipe
- PyAutoGui
- Pynput

## Future Improvements  
 
- Improve accuracy for different lighting conditions
- Implement multi-hand tracking
- Enhance gesture recognition using deep learning models  

