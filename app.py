import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Hercule Poirot", page_icon="🕵️‍♂️")
st.title("🕵️‍♂️ The Little Gray Cells of Poirot")

# Sidebar for the API Key
api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # Poirot's internal instructions
        instructions = (
            "You are Hercule Poirot, the famous Belgian detective. "
            "You speak with French phrases (mon ami, d'accord). "
            "You are Belgian, not French. You value order, method, and your mustache. "
            "Refer to yourself in the third person as Poirot."
        )

        # Logic to find the best available model
        if "model_name" not in st.session_state:
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            # Try to find the best one, otherwise take the first available
            if 'models/gemini-1.5-flash' in available_models:
                st.session_state.model_name = 'gemini-1.5-flash'
            elif 'models/gemini-pro' in available_models:
                st.session_state.model_name = 'gemini-pro'
            else:
                st.session_state.model_name = available_models[0].replace('models/', '')

        model = genai.GenerativeModel(
            model_name=st.session_state.model_name,
            system_instruction=instructions
        )

        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Speak to Poirot..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Generate response
            chat = model.start_chat(history=[])
            response = chat.send_message(prompt)
            
            with st.chat_message("assistant"):
                st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

    except Exception as e:
        st.error(f"Ah, the gray cells are troubled: {e}")
        st.info("Tip: Ensure your API Key is correct and that you have enabled the Gemini API in Google AI Studio.")
else:
    st.info("Please enter your Google API Key in the sidebar to begin.")
