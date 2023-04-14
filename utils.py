from PyPDF2 import PdfReader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import ElasticVectorSearch, Pinecone, Weaviate, FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
import os

# query = "What did Mackenna J stated?"
#"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"
def set_key(key):
    os.environ["OPENAI_API_KEY"] = key

def bot(path, query):
    # set_key(key)
    embeddings = OpenAIEmbeddings()
    reader = PdfReader(path)
    raw_text = ''
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            raw_text += text
    text_splitter = CharacterTextSplitter(        
        separator = "\n",
        chunk_size = 1000,
        chunk_overlap  = 200,
        length_function = len,
    )
    texts = text_splitter.split_text(raw_text)
    docsearch = FAISS.from_texts(texts, embeddings)
    chain = load_qa_chain(OpenAI(), chain_type="stuff")
    docs = docsearch.similarity_search(query)
    answer = chain.run(input_documents=docs, question=query)
    return answer
