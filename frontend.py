import streamlit as st
from main import openai_functions_chain
import openai
openai.api_key = "Your OpenAI API Key"
st.title("Sales_Person Info : Q&A System")

question = st.text_input("Question: ")

if question:
    query,answer = openai_functions_chain(question)
    st.text("SQL Query:")
    st.write(query)
    st.text("Answer:")
    st.write(answer)









