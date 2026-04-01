import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Hercule Poirot", page_icon="🕵️‍♂️")
st.title("🕵️‍♂️ The Little Gray Cells of Poirot")

# Setup the API Key
api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # We use gemini-1.5-flash - it is fast and free!
        # We also pass the system instruction correctly here.
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            system_instruction=(
                "You are Hercule Poirot, the famous Belgian detective. "
                "1. Speak with a French flavor (mon ami, n'est-ce pas). "
                "2. You are NOT French, you are Belgian. "
                "3. You are obsessed with order, method, and your mustache. "
                "4. Refer to yourself in the third person as Poirot. "
                "5. Use your 'little gray cells' to analyze human nature."
            )
        )

        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Speak to Poirot..."):
            # Add user message to history
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Generate response using history for context
            # We send the whole history so Poirot remembers the conversation
            chat_session = model.start_chat(
                history=[
                    {"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]}
                    for m in st.session_state.messages[:-1]
                ]
            )
            
            response = chat_session.send_message(prompt)
            
            with st.chat_message("assistant"):
                st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

    except Exception as e:
        st.error(f"Ah, an error has occurred: {e}")
else:
    st.info("Please enter your Google API Key in the sidebar to begin the investigation.")
