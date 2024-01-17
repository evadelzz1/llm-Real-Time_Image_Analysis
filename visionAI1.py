"""
A user-friendly script designed to interface with the OpenAI GPT-4 Vision API.
It provides an efficient way to analyze images using AI, 
with capabilities extending to real-time analysis via webcam integration.
This code file is structured to be easily understandable and modifiable, 
catering to both beginners and experienced programmers. 
Its primary function is to capture images, convert them into a suitable format, 
and leverage GPT-4's advanced algorithms for detailed image analysis. 
Perfect for projects in AI-driven image recognition and data processing
"""
import cv2, time, base64
from dotenv import load_dotenv

# from langchain.chat_models import ChatOpenAI
from langchain.schema.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

def encode_image(image_url):
    with open(image_url, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


if not load_dotenv():
    st.error(
        "Could not load .env file or it is empty. Please check if it exists and is readable.",
        icon="🚨"
    )
    exit(1)

cap = cv2.VideoCapture(0) # 0 stands for very first webcam attach

while True:
    ret, frame = cap.read()

    if ret:
        cv2.imshow('camera', frame)

        if cv2.waitKey(1) != -1:
            filename = "webcam_capture.png"
            cv2.imwrite(filename, frame)
            
            base64_image = encode_image(filename)

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

            print(output)
            time.sleep(2) # 2 seconds delay
    
            # break
    else:
        print("Error reading frame")
        break

cap.release() # release webcam
cv2.destroyAllWindows() # close all openCV windows