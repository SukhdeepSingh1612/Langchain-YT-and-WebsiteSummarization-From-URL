import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain_core.documents import Document
from langchain_groq import ChatGroq
import validators
from yt_dlp import YoutubeDL
import requests
import traceback

# Streamlit UI setup
st.set_page_config(page_title="YT/Website Summarizer", layout="wide")
st.title("Langchain: Summarize Text From YouTube or Website")

st.subheader("Summarize URL Content")

# Sidebar for API key
with st.sidebar:
    groq_api_key = st.text_input("Groq API Key", value="", type="password")

# Prompt template
prompt_template = """
Provide a summary of the following content in 300 words:
Content : {text}
"""
prompt = PromptTemplate(template=prompt_template, input_variables=["text"])

# Get URL input
url = st.text_input("Enter YouTube or Website URL")

# Helper to get YouTube transcript
def get_youtube_transcript(url):
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['en'],
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        subtitles = info.get("automatic_captions", {}).get("en", [])
        if not subtitles:
            return None
        subtitle_url = subtitles[0]["url"]
        vtt_data = requests.get(subtitle_url).text
        return vtt_data

# Summarize button
if st.button("Summarize the Content from YT or Website"):
    if not groq_api_key.strip() or not url.strip():
        st.error("Please enter the required fields.")
    elif not validators.url(url):
        st.error("Invalid URL.")
    else:
        try:
            llm = ChatGroq(model="gemma2-9b-it", groq_api_key=groq_api_key)

            with st.spinner("Summarizing..."):
                if "youtube.com" in url or "youtu.be" in url:
                    text = get_youtube_transcript(url)
                    if not text:
                        st.error("No subtitles found for this video.")
                        st.stop()
                else:
                    from langchain_community.document_loaders import UnstructuredURLLoader
                    loader = UnstructuredURLLoader(urls=[url], ssl_verify=False)
                    docs = loader.load()
                    text = docs[0].page_content

                docs = [Document(page_content=text)]
                chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
                output = chain.run(docs)

                st.success(output)

        except Exception as e:
            st.error("An error occurred:\n" + traceback.format_exc())
