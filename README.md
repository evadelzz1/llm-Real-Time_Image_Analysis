# Facial Detection & Real-Time Image Analysis App

This is a Streamlit application for displaying the webcam feed and performing facial detection using OpenCV. And Analyze with OpenAI.

## Installation

Type.1

    pip install -r requirements.txt

    python vision10.py

Type.2 (streamlit app)

    python -m venv .venv

    source .venv/bin/activate

    python -V

    pip list

    pip install -r requirements.txt

    python -m streamlit run visionAI1.py

## How it Works

The script uses the Streamlit and OpenCV libraries to create the application. Here's an overview of the code's functionality:

1. Video frames are captured from the webcam using `cv2.VideoCapture()`, with the default webcam index (0). The frames are accessed through the created `cap` object.

2. A placeholder is created using `st.empty()` to display the webcam feed.

3. A stop button is added to the app interface using `st.button("Stop")`. Clicking this button will stop the webcam feed and exit the application.

4. The script enters a while loop to continuously read frames from the webcam using `cap.read()`. If a frame is successfully retrieved, it is converted from BGR to RGB format using `cv2.cvtColor()` to match Streamlit's expected image format.

5. The converted frame is displayed in the placeholder using `frame_placeholder.image()`. The `channels="RGB"` argument specifies the color channels of the image.

6. The loop continues until the webcam feed ends (`cap.isOpened()` returns `False`) or the stop button is pressed (`stop_button_pressed` is `True`).

7. Once the loop ends, the webcam capture is released using `cap.release()` and any open OpenCV windows are closed using `cv2.destroyAllWindows()`.
