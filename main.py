import streamlit as st
from llm_utils import process_text_query, process_image_query
from ui import render_text_input, render_image_upload

def main():
    st.title("Multimodal AI Assistant")
    
    st.header("Ask me anything!")
    
    # Text query input
    text_query = render_text_input()
    
    if text_query:
        response_text = process_text_query(text_query)
        st.subheader("Response:")
        st.write(response_text)
    
    # Image query input
    image_query = render_image_upload()
    
    if image_query:
        response_image = process_image_query(image_query)
        st.subheader("Image Response:")
        st.image(response_image, caption="Processed Image")

if __name__ == "__main__":
    main()