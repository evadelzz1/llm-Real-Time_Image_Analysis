import cv2
import streamlit as st
import numpy as np
import tempfile

# https://github.com/niconielsen32/StreamlitOpenCV/blob/main/WebcamLiveStream.py
# https://github.com/petermartens98/Streamlit-OpenCV-Webcam-Display-Web-App/blob/main/main.py

# call back function -> runs BEFORE the rest of the app
def reset_button():
    st.session_state["switchWebcam"] = False
    return

def encode_image(image_url):
    with open(image_url, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def xxx():
    st.info(1)
    
def main():
    # Set the title for the Streamlit app
    st.set_page_config(page_title="Streamlit WebCam App")

    st.title("Video Capture with OpenCV (Webcam Display)")
    st.caption("Powered by OpenCV, Streamlit")

    ### Check box to turn on camera
    run = st.checkbox("Turn on camera", value=False, key="switchWebcam")

    # Use this line to capture video from the webcam
    cap = cv2.VideoCapture(0)

    frame_placeholder = st.empty()

    # Add a "Stop" button and store its state in a variable
    stop_button_pressed = st.button("Stop", on_click=xxx)

    reset_button_pressed = st.button("Reset", on_click=reset_button)


        # capture_button_pressed =  st.button("Capture")

        # if capture_button_pressed:
        #     filename = "image.png"
        #     cv2.imwrite(filename, frame)
        #     base64_image = encode_image(filename)
            

    while cap.isOpened() and not stop_button_pressed and run:
        ret, frame = cap.read()

        if ret:
        
            # You can process the frame here if needed
            # e.g., apply filters, transformations, or object detection

            # Convert the frame from BGR to RGB format
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Display the frame using Streamlit's st.image
            frame_placeholder.image(frame, channels="RGB")

            # Break the loop if the 'q' key is pressed or the user clicks the "Stop" button
            if cv2.waitKey(1) & 0xFF == ord("q") or stop_button_pressed:
                cv2.imwrite('photo.jpg', frame)
                break


        else:
            st.write("Error reading frame")
            break
        
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()