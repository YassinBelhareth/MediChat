import streamlit as st
from model import conversation_chain

# Page configuration
st.set_page_config(page_title="MediChat", layout="centered")

# Initialize message history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Function to handle sending
def handle_send():
    if st.session_state.user_input.strip():  # Checks that input is not empty
        response = conversation_chain.run(st.session_state.user_input)
        st.session_state.chat_history.append({"question": st.session_state.user_input, "response": response})
        st.session_state.user_input = ""  # Resets the input field after sending

# Display message history
st.title("MediChat: An AI-Powered Medical Consultation Assistant")
st.write("### Chat History")
for chat in st.session_state.chat_history:
    st.markdown(f"**You:** {chat['question']}")
    st.markdown(f"**MediChat:** {chat['response']}")
    st.markdown("---")

# Input field and send button
with st.container():
    col1, col2 = st.columns([4, 1])  # Split into two columns
    with col1:
        st.text_input(
            "Your message:",
            placeholder="Type your message here...",
            label_visibility="collapsed",
            key="user_input",
            on_change=handle_send,
        )
    with col2:
        if st.button("Send"):
            handle_send()
