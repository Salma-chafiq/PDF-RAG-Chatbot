import streamlit as st

# Importation des modules nécessaires de LangChain
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ollama import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

# Définition du template pour le prompt d'interaction avec le modèle
# Ce template guide le modèle pour répondre aux questions en se basant sur le contexte extrait
# La réponse doit être concise, en trois phrases maximum.
template = """
You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. 
If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
Question: {question} 
Context: {context} 
Answer:
"""

# Répertoire où les fichiers PDF téléchargés seront enregistrés
pdfs_directory = 'pdfs/'

# Initialisation des embeddings et du store de vecteurs pour le stockage des documents indexés
embeddings = OllamaEmbeddings(model="llama3.2:latest")
vector_store = InMemoryVectorStore(embeddings)

# Initialisation du modèle LLaMA pour répondre aux questions
model = OllamaLLM(model="llama3.2:latest")

# Fonction pour enregistrer le fichier PDF téléchargé dans le répertoire désigné
def upload_pdf(file):
    with open(pdfs_directory + file.name, "wb") as f:
        f.write(file.getbuffer())

# Fonction pour charger un fichier PDF et extraire son contenu sous forme de documents
def load_pdf(file_path):
    loader = PDFPlumberLoader(file_path)
    documents = loader.load()
    return documents

# Fonction pour découper le texte en segments plus petits, facilitant leur traitement par l'IA
def split_text(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,  # Taille des segments de texte
        chunk_overlap=200,  # Chevauchement pour conserver du contexte entre les segments
        add_start_index=True
    )
    return text_splitter.split_documents(documents)

# Fonction pour indexer les documents dans le store de vecteurs
def index_docs(documents):
    vector_store.add_documents(documents)

# Fonction pour récupérer les documents les plus pertinents en fonction d'une requête utilisateur
def retrieve_docs(query):
    return vector_store.similarity_search(query)

# Fonction pour générer une réponse à une question en utilisant le modèle et le contexte extrait
def answer_question(question, documents):
    context = "\n\n".join([doc.page_content for doc in documents])
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model  # Création d'une chaîne combinant le prompt et le modèle
    return chain.invoke({"question": question, "context": context})

# Interface Streamlit pour l'upload du fichier PDF
uploaded_file = st.file_uploader(
    "Upload PDF",  # Texte d'instruction pour l'utilisateur
    type="pdf",  # Type de fichier accepté
    accept_multiple_files=False  # Un seul fichier à la fois
)

# Si un fichier est téléchargé, il est traité pour être utilisé dans la recherche de réponses
if uploaded_file:
    upload_pdf(uploaded_file)  # Enregistrement du fichier sur le serveur
    documents = load_pdf(pdfs_directory + uploaded_file.name)  # Chargement et extraction du texte
    chunked_documents = split_text(documents)  # Découpage du texte en segments
    index_docs(chunked_documents)  # Indexation des segments pour la recherche

    # Interface utilisateur pour entrer une question
    question = st.chat_input()

    if question:
        st.chat_message("user").write(question)  # Affichage de la question posée par l'utilisateur
        related_documents = retrieve_docs(question)  # Récupération des documents pertinents
        answer = answer_question(question, related_documents)  # Génération de la réponse
        st.chat_message("assistant").write(answer)  # Affichage de la réponse du chatbot
