import streamlit as st
from openai import OpenAI
from io import BytesIO
from PIL import Image
import base64
import pandas as pd
import json
import re


st.set_page_config(page_title='Blueprint take-off AI', page_icon='👁️')

st.markdown('# CAD Blueprint take-off AI')
st.markdown('This app uses OpenAI to provide a take-off of the quantities from an engineering drawing. It returns the results as a markdown table.')

api_key = st.text_input('OpenAI API Key', '', type='password')

# Get user inputs
img_input = st.file_uploader('Images', accept_multiple_files=True)

# Send API request
if st.button('Send'):
    if not api_key:
        st.warning('API Key required')
        st.stop()
    msg = {'role': 'user', 'content': []}
    msg['content'].append({'type': 'text', 'text': 'Provide a take-off of the quantities from this engineering drawing returning ONLY as a markdown table.'})
    images = []
    for img in img_input:
        if img.name.split('.')[-1].lower() not in ['png', 'jpg', 'jpeg', 'gif', 'webp']:
            st.warning('Only .jpg, .png, .gif, or .webp are supported')
            st.stop()
        encoded_img = base64.b64encode(img.read()).decode('utf-8')
        images.append(img)
        msg['content'].append(
            {
                'type': 'image_url',
                'image_url': {
                    'url': f'data:image/jpeg;base64,{encoded_img}',
                    'detail': 'low'
                }
            }
        )
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model='gpt-4o',
        temperature=0.0,
        max_tokens=300,
        messages=[msg]
    )
    response_msg = str(response.choices[0].message.content)
    # response_msg = 'This is a placeholder response'

    # Display user input and response
    with st.chat_message('user'):
        for i in msg['content']:
            if i['type'] == 'text':
                st.write(i['text'])
            else:
                with st.expander('Attached Image'):
                    img = Image.open(BytesIO(base64.b64decode(i['image_url']['url'][23:])))
                    st.image(img)
    if response_msg:
        with st.chat_message('assistant'):
            st.markdown(response_msg)

            