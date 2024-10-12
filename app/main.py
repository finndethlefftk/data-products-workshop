from fastapi import UploadFile
import streamlit as st
from openai import OpenAI
import base64
import requests

def base_ui():
    st.set_page_config(page_title="AI Analytics Toolkit", page_icon="🔥")
    st.sidebar.title("AI Toolkit")
    st.sidebar.write("🔥 TK DATA ANALYTICS")
    st.sidebar.caption("Built in Barcelona")
    st.markdown("## Create Tracking Events")
    st.markdown("*From design to tracking events in one click*")


def image_uploader() -> UploadFile | None:
    result = st.file_uploader("PNG or JPG")
    return result


# Function to encode the image
def encode_image(image: UploadFile) -> str:
    return base64.b64encode(image.getvalue()).decode('utf-8')


def generate_tracking_events(image: UploadFile | None):
    if st.button("Generate Tracking Events", type="primary"):
        if image:
            with st.spinner("Generating tracking events..."):
                encoded_image = encode_image(image)
                response = get_response(encoded_image)
            return st.success(response)
        else:
            st.warning("Please upload an image first")


def get_response(encoded_image: str):
    client = OpenAI()
    response = client.chat.completions.create(
    model="gpt-4o",
    temperature=0.0,
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Describe the design of the image in detail"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{encoded_image}"
                    }
                },
            ],
        }
    ],
        max_tokens=300,
    )
    return response.choices[0].message.content


def main():
    base_ui()
    image = image_uploader()
    generate_tracking_events(image)
        



if __name__ == "__main__":
    main()



