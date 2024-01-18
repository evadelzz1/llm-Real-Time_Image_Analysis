import streamlit as st
import numpy as np
# import tempfile
import cv2, time, base64
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.schema.messages import HumanMessage, SystemMessage

# https://github.com/niconielsen32/StreamlitOpenCV/blob/main/WebcamLiveStream.py
# https://github.com/petermartens98/Streamlit-OpenCV-Webcam-Display-Web-App/blob/main/main.py
# https://m.blog.naver.com/dldudcks1779/222064172394
# https://inhovation97.tistory.com/51

def reset_button():
    st.session_state["switchWebcam"] = False
    return

def convertToJpeg(img):
    result, encoded = cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 100])
    return cv2.imdecode(encoded, 1)

def convertToPng(img):
    result, encoded = cv2.imencode('.png', img, [cv2.IMWRITE_PNG_COMPRESSION, 50])
    return cv2.imdecode(encoded, 1)

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

    ### Check box to turn on camera
    run = st.checkbox("Turn on camera", value=False, key="switchWebcam")

    col1, col2 = st.columns(2)
    with col1:
        # Use this line to capture video from the webcam
        cap = cv2.VideoCapture(0)

        frame_placeholder = st.empty()

    with col2:
        # Add a "Stop" button and store its state in a variable
        stop_button_pressed = st.button("Stop", on_click=reset_button)
        capture_button_pressed = st.button("Capture")

        while cap.isOpened() and not stop_button_pressed and run:
            ret, frame = cap.read()

            if not ret:
                st.write("The video capture has ended.")
                break

            # You can process the frame here if needed
            # e.g., apply filters, transformations, or object detection

            # Convert the frame from BGR to RGB format
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Display the frame using Streamlit's st.image
            frame_placeholder.image(frame, channels="RGB")

            # Break the loop if the 'q' key is pressed or the user clicks the "Stop" button
            if cv2.waitKey(1) & 0xFF == ord("q") or stop_button_pressed:
                switchWebcam.value = False
                st.info("webcam off")
                break

            if capture_button_pressed:
                st.info("Captured your face")
                # resize_frame = cv2.resize(frame, (640, 480), interpolation=cv2.INTER_CUBIC)
                # bytes_data = resize_frame
                
                bytes_data = convertToPng(frame)
                base64_image = base64.b64encode(bytes_data).decode('utf-8')
                st.info(type(base64_image))
                # chat = ChatOpenAI(model='gpt-4-vision-preview', max_tokens=256)

                # output = chat.invoke([
                #     HumanMessage(
                #         content=[
                #             {"type": "text", "text": "What is this image about? Focus on detials and relpy in one line"},
                #             {"type": "image_url", 
                #             "image_url": {
                #                 "url": "data:image/png;base64," + base64_image,
                #                 "detail": "auto"
                #                 }}
                #             ])
                # ])
                
                # st.info(output)
                
                break
                 
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
    
