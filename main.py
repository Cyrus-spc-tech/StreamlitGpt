import openai
import streamlit as st

st.markdown("<h1 style='color: #46CAF0;'>ProffesserGPT</h1>", unsafe_allow_html=True)

st.divider()

st.markdown("To generate your OpenAI API key, visit [OpenAI API Key Generation](https://platform.openai.com/signup).")

api_key = st.text_input("Enter your OpenAI API key", type="password")
gptmodel = st.sidebar.selectbox("Select OpenAI Model", ["gpt-3.5-turbo", "gpt-4"])
userrole = "user"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(f"<div class='message user'>{message['content']} <span style='color: gray;'>🤖</span></div>", unsafe_allow_html=True)
    else:
        with st.chat_message("assistant"):
            st.markdown(f"<div class='message assistant'>{message['content']} <span style='color: gray;'>👤</span></div>", unsafe_allow_html=True)

prompt = st.text_input("What do you want to learn? > ")
gptbutton = st.button("Send")

st.divider()

if gptbutton:
    if not api_key:
        st.error("Please enter your OpenAI API key.")
    elif not prompt:
        st.error("Please enter a question.")
    else:
        openai.api_key = api_key
        with st.spinner("Generating response..."):
            try:
                
                response = openai.ChatCompletion.create(
                    model=gptmodel,
                    messages=st.session_state.messages + [{"role": userrole, "content": prompt}]
                )
                bot_response = response.choices[0].message['content']
                
                st.session_state.messages.append({"role": userrole, "content": prompt})
                st.session_state.messages.append({"role": "assistant", "content": bot_response})
                
                st.chat_message("user", prompt)
                st.chat_message("assistant", bot_response)
            except Exception as e:
                st.error(f"An error occurred: {e}")


if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.stop() 