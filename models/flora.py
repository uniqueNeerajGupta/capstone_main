import streamlit as st
import time
import os
import pandas as pd
from PIL import Image
import pytesseract

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# -------------------------------------------------
# SYSTEM CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="GARMANDI | Neural Link",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------------------------------------
# ENV (SET OUTSIDE IN PROD)
# -------------------------------------------------
os.environ["OPENAI_API_KEY"] = "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"

# -------------------------------------------------
# JARVIS / FLORA UI CSS
# -------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Source+Code+Pro:wght@300&display=swap');

[data-testid="stAppViewContainer"] {
    background-color: #000;
    background-image:
        radial-gradient(circle at 50% 50%, #0a1f1a 0%, #000 100%),
        url('https://www.transparenttextures.com/patterns/carbon-fibre.png');
}

[data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed;
    inset: 0;
    background:
        linear-gradient(rgba(18,16,16,0) 50%, rgba(0,0,0,0.25) 50%),
        linear-gradient(90deg, rgba(255,0,0,0.06), rgba(0,255,0,0.02), rgba(0,0,255,0.06));
    background-size: 100% 2px, 3px 100%;
    pointer-events: none;
}

.terminal-card {
    background: rgba(0,20,20,0.6);
    border: 1px solid #D4AF37;
    padding: 15px;
    font-family: 'Source Code Pro', monospace;
    color: #D4AF37;
    font-size: 0.7rem;
    box-shadow: 0 0 15px rgba(212,175,55,0.15);
}

.glitch-text {
    font-family: 'Orbitron', sans-serif;
    color: white;
    text-align: center;
    letter-spacing: 15px;
    animation: glitch 1s infinite;
}

.stChatInputContainer {
    border: 1px solid #D4AF37 !important;
    background: rgba(0,0,0,0.85) !important;
}

header, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# HELPERS (UNCHANGED LOGIC)
# -------------------------------------------------
def load_csv(file):
    df = pd.read_csv(file)
    return [" | ".join(map(str, row.values)) for _, row in df.iterrows()]

def load_pdf(file):
    loader = PyPDFLoader(file)
    return [doc.page_content for doc in loader.load()]

def load_image(file):
    img = Image.open(file)
    return pytesseract.image_to_string(img)

def create_vectorstore(texts):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.create_documents(texts)
    embeddings = OpenAIEmbeddings()
    return FAISS.from_documents(docs, embeddings)

def rag_chat(query, vectordb):
    retriever = vectordb.as_retriever(search_kwargs={"k": 3})
    docs = retriever.get_relevant_documents(query)
    context = "\n".join(d.page_content for d in docs)

    llm = ChatOpenAI(model="gpt-4.1")

    prompt = f"""
You are GARMANDI's neural real-estate intelligence.
Answer ONLY from context.
If insufficient data, say you don't know.

Context:
{context}

Query:
{query}
"""
    return llm.invoke(prompt).content

def normal_chat(query):
    llm = ChatOpenAI(model="gpt-4.1")
    return llm.invoke(query).content

# -------------------------------------------------
# TOP HEADER
# -------------------------------------------------
st.markdown(
    '<p style="color:#D4AF37;text-align:center;font-family:Source Code Pro;font-size:0.6rem;letter-spacing:5px;">[ SECURE QUANTUM TUNNEL ACTIVE ]</p>',
    unsafe_allow_html=True
)
st.markdown('<h1 class="glitch-text">FLORA-01</h1>', unsafe_allow_html=True)

# -------------------------------------------------
# MAIN LAYOUT
# -------------------------------------------------
left_col, mid_col, right_col = st.columns([1, 2.5, 1])

# ---------------- LEFT SYSTEM PANEL ----------------
with left_col:
    st.markdown('<p style="color:#D4AF37;font-size:0.6rem;">// SYSTEM_HEALTH</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="terminal-card">
        CPU_LOAD: 22.4%<br>
        VECTOR_DB: ONLINE<br>
        RAM: STABLE<br>
        REGION: MUMBAI_DC
    </div>
    """, unsafe_allow_html=True)

# ---------------- CENTER CHAT ----------------
with mid_col:

    st.image(
        "https://img.freepik.com/free-photo/view-futuristic-robot-working-office_23-2150841517.jpg",
        width=180
    )

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Neural link established. Awaiting command."}
        ]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(
                f"<span style='font-family:Source Code Pro;color:white;'>{msg['content']}</span>",
                unsafe_allow_html=True
            )

    prompt = st.chat_input("ENTER COMMAND_")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.spinner("EXECUTING NEURAL QUERY..."):
            time.sleep(1)
            if "vectordb" in st.session_state:
                response = rag_chat(prompt, st.session_state.vectordb)
            else:
                response = normal_chat(prompt)

        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

# ---------------- RIGHT UPLOAD PANEL ----------------
with right_col:
    st.markdown('<p style="color:#D4AF37;font-size:0.6rem;">// UPLINK_CORE</p>', unsafe_allow_html=True)

    uploaded_files = st.file_uploader(
        "DROP_FILE",
        type=["csv", "pdf", "png", "jpg"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )

    if uploaded_files:
        all_texts = []
        for file in uploaded_files:
            if file.name.endswith(".csv"):
                all_texts.extend(load_csv(file))
            elif file.name.endswith(".pdf"):
                all_texts.extend(load_pdf(file))
            else:
                all_texts.append(load_image(file))

        st.session_state.vectordb = create_vectorstore(all_texts)
        st.markdown(
            '<p style="color:#00ff00;font-size:0.6rem;">[ DATA_STREAM_SYNCED ]</p>',
            unsafe_allow_html=True
        )

    st.markdown("""
    <div style="border:1px solid #555;padding:10px;font-size:0.5rem;color:#555;font-family:Source Code Pro;">
        GARMANDI_OS v4.2<br>
        BUILD: 2026.01.08<br>
        STATUS: OPERATIONAL
    </div>
    """, unsafe_allow_html=True)
