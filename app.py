import validators,streamlit as st
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader
import traceback


## Streamlit App
st.set_page_config(page_title="Langchain: Summarize Text From YT or Website", layout="wide")
st.title("Langchain: Summarize Text From YT or Website")

st.subheader("Summarize URL")


## Get the Groq  API Key and url(YT or website) to be summarized
with st.sidebar:
    groq_api_key = st.text_input("Groq API Key", value="",type="password")
    # Initialize the LLM




prompt_template  = """
Provide a summary of the following content in 300 words:
Content : {text}
""" 

prompt = PromptTemplate(template=prompt_template, input_variables=["text"])
    
url = st.text_input("URL",label_visibility="collapsed")


if st.button("Summarize the Content from YT or Website"):
    if not groq_api_key.strip() or not url.strip():
        st.error("Please enter the information.")
    elif not validators.url(url):
        st.error("Please enter a valid URL.")
    else:
        try:
            llm = ChatGroq(model="Gemma2-7b-It",groq_api_key=groq_api_key)

            with st.spinner("Summarizing..."):
                # Load the content from the URL
                if "youtube.com" in url or "youtu.be" in url:
                    loader = YoutubeLoader.from_youtube_url(url, add_video_info=True)
                else:
                    loader = UnstructuredURLLoader(urls=[url], ssl_verify=False, headers={"User-Agent": "Mozilla/5.0, AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"})
                docs = loader.load()

                # Create a summarization chain
                chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)

                # Run the summarization
                output_summary = chain.run(docs)

                st.success(output_summary)
        except Exception as e:
            st.error(f"An error occurred:\n{traceback.format_exc()}")


    
