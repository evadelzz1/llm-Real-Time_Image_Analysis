import streamlit as st
# import numpy as np

import cv2, time, base64, io
from dotenv import load_dotenv
from PIL import Image

from langchain_openai import ChatOpenAI
from langchain.schema.messages import HumanMessage, SystemMessage

def reset_button():
    st.session_state["switchWebcam"] = False
    return

def imgSize(base64_string):
    file_size = len(base64_string) * 3 / 4 - base64_string.count('=')
    return file_size    # bytess

def main():
    if not load_dotenv():
        st.error(
            "Could not load .env file or it is empty. Please check if it exists and is readable.",
            icon="🚨"
        )
        exit(1)
        
    # Set the title for the Streamlit app
    st.set_page_config(
        page_title="Streamlit WebCam App",
        page_icon="",
        layout="wide"
    )
    st.title("Video Capture with OpenCV (Webcam Display)")
    st.caption("Powered by OpenCV, Streamlit")
    st.divider()
    
    ### Check box to turn on camera
    run = st.checkbox("Turn on camera", value=False, key="switchWebcam")

    # Read frames and encode to base64
    base64Frames = []
            
    col1, col2 = st.columns(2)
    with col1:
        # Use this line to capture video from the webcam
        cap = cv2.VideoCapture(0)

        frame_placeholder = st.empty()

    with col2:
        capture_button_pressed = st.button("Capture")
        reset_button_pressed = st.button("Reset", on_click=reset_button)
            
        while cap.isOpened() and not reset_button_pressed and run:
            ret, frame = cap.read()

            if not ret:
                st.write("The video capture has ended.")
                break

            # decreate frame size
            frame = cv2.resize(frame, dsize=(0,0), fx=0.8, fy=0.8, interpolation=cv2.INTER_LINEAR)
            
            # Convert the frame from BGR to RGB format
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Display the frame using Streamlit's st.image
            frame_placeholder.image(frame, channels="RGB")

            _, buffer = cv2.imencode(".jpg", frame)
            base64Frames.append(base64.b64encode(buffer).decode("utf-8"))

            # Break the loop if the 'q' key is pressed or the user clicks the "Stop" button
            if cv2.waitKey(1) & 0xFF == ord("q") or reset_button_pressed:
                switchWebcam.value = False
                st.info("webcam off")
                break

            if capture_button_pressed:
                size_image = imgSize(base64Frames)
                st.info(f"Captured your face. (frames={len(base64Frames)}), sizes={size_image}")
                
                with st.spinner("Generating your quiz...🤓"):
                    if size_image < 180000:
                        
                        chat = ChatOpenAI(model='gpt-4-vision-preview', max_tokens=256)

                        output = chat.invoke([
                            HumanMessage(
                                content=[
                                    {"type": "text", "text": "What is this image about? Focus on detials and relpy in one line"},
                                    {"type": "image_url", 
                                        "image_url": {
                                            "url": "data:image/png;base64," + base64Frames[0],
                                            "detail": "auto"
                                            }}
                                    ])
                        ])
                        
                        st.info(output)
                
                break
                 
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
    
