import streamlit as st
import os
from llama_index.llms.openai import OpenAI
from llama_index.core.llms import ChatMessage, ImageBlock, TextBlock, MessageRole

# Load API key from environment or Streamlit secrets
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    try:
        OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
    except Exception:
        OPENAI_API_KEY = ""

if not OPENAI_API_KEY:
    st.error("OpenAI API key not found. Please set it in your environment or Streamlit secrets.")
    st.stop()
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# Initialize LLM
openai_llm = OpenAI(model="gpt-4o", max_new_tokens=300)

def multimodal_query(text, image_file=None):
    """Send a multimodal query (text + optional image) to the LLM."""
    blocks = []
    if text:
        blocks.append(TextBlock(text=text))
    if image_file:
        # Save uploaded image to a temp file
        img_path = "uploaded_image.jpg"
        with open(img_path, "wb") as f:
            f.write(image_file.read())
        blocks.append(ImageBlock(path=img_path, image_mimetype=image_file.type))
    msg = ChatMessage(role=MessageRole.USER, blocks=blocks)
    response = openai_llm.chat(messages=[msg])
    return response

# Streamlit UI
st.title("🖼️🤖 Multimodal AI Assistant")
st.write("Ask a question with text and/or image. Powered by GPT-4o.")

with st.form("query_form"):
    user_text = st.text_area("Enter your question:", "")
    user_image = st.file_uploader("Upload an image (optional):", type=["jpg", "jpeg", "png"])
    submitted = st.form_submit_button("Ask")

if submitted:
    with st.spinner("Thinking..."):
        response = multimodal_query(user_text, user_image)
        st.markdown("**Assistant Response:**")
        st.write(response)