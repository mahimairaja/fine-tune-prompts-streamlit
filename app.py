import streamlit as st
from st_copy_to_clipboard import st_copy_to_clipboard
from langchain_openai import ChatOpenAI
from langchain import hub


st.title('Prompt Optimizer 🦜🔗')

openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password')
model_name = st.sidebar.selectbox('Model', ['gpt-4o', 'gpt-3.5-turbo', 'gpt-4-turbo'], placeholder='Choose a model')

def generate_response(old_prompt, task):
    prompt = hub.pull("hardkothari/prompt-maker")
    model = ChatOpenAI(
        model=model_name,
        openai_api_key=openai_api_key
        )
    
    runnable = prompt | model 
    response = runnable.invoke({
            "task": task,
            "lazy_prompt": old_prompt,
        })

    response = response.content
    st.info(response)
    st_copy_to_clipboard(response)

with st.form('my_form'):
    task = st.text_input(label='task', placeholder='Enter the task to be optimized...') 
    prompt = st.text_area(label='prompt', placeholder='Enter the prompt to be optimized...', height=200)
    submitted = st.form_submit_button('Submit')
    if not openai_api_key.startswith('sk-'):
        st.warning('Please enter your OpenAI API key!', icon='⚠')
    if submitted and openai_api_key.startswith('sk-'):
        with st.spinner('Optimizing...'):
            generate_response(prompt, task)
            st.divider
            st.caption('CREDITS: The instruction is contributed by :blue[Hardkothari] - [LangChain Hub](https://smith.langchain.com/hub/hardkothari/prompt-maker)')