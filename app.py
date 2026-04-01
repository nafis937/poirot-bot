import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Hercule Poirot", page_icon="🕵️‍♂️")
st.title("🕵️‍♂️ The Little Gray Cells of Poirot")

# Setup the API Key
api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')

    # The Poirot Instructions
    system_instruction = (
        "You are Hercule Poirot, the Belgian detective. You use French phrases like 'mon ami', "
        "you are obsessed with order, method, and your mustache. You refer to yourself in the third person. "
        "You solve problems using psychology and your little gray cells."
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Speak to Poirot..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response
        full_prompt = f"{system_instruction}\n\nUser: {prompt}"
        response = model.generate_content(full_prompt)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
else:
    st.info("Please enter your Google API Key in the sidebar to begin the investigation.")
