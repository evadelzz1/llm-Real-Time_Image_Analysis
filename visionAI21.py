import streamlit as st
import cv2, time, base64
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.schema.messages import HumanMessage, SystemMessage

def main():
    if not load_dotenv():
        st.error(
            "Could not load .env file or it is empty. Please check if it exists and is readable.",
            icon="🚨"
        )
        exit(1)

    st.set_page_config(
        page_title="Webcam Apps",
        page_icon="",
        layout="wide"
    )
    
    st.title("Webcam Capture Apps")
    st.write("Capture your aspect from Webcam and explain the picture")
        
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        picture = st.camera_input("Take a picture")
            
    with col2:

        if picture is not None:
            st.image(picture, width=400, caption='captured by webcam')
            
            # To read image file buffer as bytes:
            bytes_data = picture.getvalue()
            base64_image = base64.b64encode(bytes_data).decode('utf-8')
            
            chat = ChatOpenAI(model='gpt-4-vision-preview', max_tokens=256)

            output = chat.invoke([
                HumanMessage(
                    content=[
                        {"type": "text", "text": "What is this image about? Focus on detials and relpy in one line"},
                        {"type": "image_url", 
                        "image_url": {
                            "url": "data:image/png;base64," + base64_image,
                            "detail": "auto"
                            }}
                        ])
            ])
            
            st.session_state.result = output
            
    if st.session_state.result:
        st.info(st.session_state.result )                

if __name__ == "__main__":
    if 'result' not in st.session_state:
        st.session_state.result = ""
        
    main()