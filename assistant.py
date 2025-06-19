import streamlit as st
import os
from llama_index.llms.openai import OpenAI
from llama_index.core.llms import ChatMessage, ImageBlock, TextBlock, MessageRole
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()
# Loading API key from environment or Streamlit secrets


try:
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
except KeyError:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

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
        # Ensure the directory exists
        os.makedirs("image", exist_ok=True)
        img_path = "image/uploaded_image.jpg"
        with open(img_path, "wb") as f:
            f.write(image_file.read())
        blocks.append(ImageBlock(path=img_path, image_mimetype=image_file.type))
    msg = ChatMessage(role=MessageRole.USER, blocks=blocks)
    response = openai_llm.chat(messages=[msg])
    return response

# Streamlit UI
st.markdown(
    """
    <style>
    .stApp {
        background-color: #FFF9DB; /* Pale yellow */
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <style>
    div.stButton > button {
        background-color: #FFD600;   /* Pale yellow */
        color: #333333;              /* Text color */
        border-radius: 8px;
        border: 1px solid #FFD600;
        font-weight: bold;
    }
    div.stButton > button:hover {
        background-color: #FFEA70;   /* Lighter yellow on hover */
        color: #000000;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.title("🤹🏻‍♀️ Hiya! I'm your assistant!")
#st.write("📎📷 You can ask me any questions you have! I can also help you with any questions about your photo! Upload your image and write your question in the box!")
st.markdown("#### 📎 You can ask me any questions you have.", unsafe_allow_html=True)
st.markdown("#### 📷 I can also help you with any questions about your photo.", unsafe_allow_html=True)



with st.form("query_form"):
    user_text = st.text_area("**✍🏽 Write your question here:**", "")
    submitted = st.form_submit_button("Ask")

user_image = st.file_uploader("**🎞️ Upload your image here and write your question in the box above:**", type=["jpg", "jpeg", "png"])
if user_image is not None:
    st.image(user_image, caption="Uploaded Image", use_container_width = True)

if submitted:
    with st.spinner("Give me a second... My brain is processing yoru question!"):
        response = multimodal_query(user_text, user_image)
        # Extracting the assistant's message
        try:
            assistant_text = response.message.content
        except Exception:
            assistant_text = str(response)
    st.markdown("**Assistant Response:**")
    st.write(assistant_text)