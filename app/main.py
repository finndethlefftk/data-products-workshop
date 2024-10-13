from fastapi import UploadFile
import streamlit as st
from openai import OpenAI
import base64
from constants import LLM_MODEL, DEFAULT_PROMPT




class Interface:
    """Class to handle the interface"""
    
    @staticmethod
    def base_ui():
        """Static UI elements"""
        st.set_page_config(page_title="AI Analytics Toolkit", page_icon="🔥", layout="wide")
        st.sidebar.title("AI Toolkit")
        st.sidebar.write("🔥 TK DATA ANALYTICS")
        st.sidebar.caption("Built in Barcelona")
        st.markdown("## Create Tracking Events")
        st.markdown("*From design to tracking events in one click*")


class FileHandler:
    """Class to handle the file"""
    
    def __init__(self):
        pass

    def get_encoded_image(self) -> str | None:
        """Upload an image and encode it to base64"""
        image = st.file_uploader("PNG or JPG")
        if image:
            encoded_image = self.encode_image(image)
            return encoded_image
        else:
            return None
    
    def encode_image(self, image: UploadFile | None) -> str:
        """Encode the image to base64"""
        return base64.b64encode(image.getvalue()).decode('utf-8')



class MessageHandler:
    """Class to create the messages to send to the OpenAI API"""
    
    def __init__(self, base_prompt: str, encoded_image: str, custom_prompt: str | None = None):
        self.base_prompt = base_prompt
        self.encoded_image = encoded_image
        self.custom_prompt = custom_prompt
    
    def get_messages(self) -> list[dict]:
        """Create the messages to send to the OpenAI API"""
        role = "user"
        messages = [
            {
                "role": role,
                "content": [
                    {"type": "text", "text": self.base_prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{self.encoded_image}"}}
                ]
            }
        ]
        
        if self.custom_prompt:
            messages.append({
                "role": role,
                "content": [
                    {"type": "text", "text": self.custom_prompt}
                ]
            })
        
        return messages
    
    def set_custom_prompt(self, custom_prompt: str):
        """Set the custom prompt"""
        self.custom_prompt = custom_prompt


class ResponseHandler:
    """Class to handle the response from the OpenAI API"""
    
    def __init__(self, messages: list[dict]):
        self.messages = messages


    def get_response(self) -> str:
        """Get the response from the OpenAI API"""
        client = OpenAI()
        response = client.chat.completions.create(
            model=LLM_MODEL,
            temperature=0.0,
            messages=self.messages,
            max_tokens=2000,
        )
        result = response.choices[0].message.content
        return result


class App:
    """Class to handle the app"""

    @staticmethod
    def run():
        """Run the app"""
        Interface.base_ui()
    
        file_handler = FileHandler()
        encoded_image = file_handler.get_encoded_image()

        if encoded_image:
            message_handler = MessageHandler(base_prompt=DEFAULT_PROMPT, encoded_image=encoded_image)
            messages = message_handler.get_messages()


        if st.button("Generate Tracking Events", type="primary"):
            if encoded_image:
                response_handler = ResponseHandler(messages=messages)
                with st.spinner("Generating tracking events..."):
                    response = response_handler.get_response()
                    st.success(response)
                    # copy to clipboard
                    with st.expander("Copy to clipboard"):
                        st.code(response, language="markdown")
            else:
                st.warning("Please upload an image first")

        # TODO: Custom prompt


def main():
    """Main function to run the app"""
    App.run()
    

if __name__ == "__main__":
    main()

