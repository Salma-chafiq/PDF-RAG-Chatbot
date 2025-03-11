<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>README</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 20px;
        }
        code {
            background-color: #f4f4f4;
            padding: 5px;
            border-radius: 5px;
        }
        pre {
            background-color: #f4f4f4;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
        }
        img {
            max-width: 100%;
            height: auto;
        }
    </style>
</head>
<body>
    <h1>PDF RAG Chatbot</h1>
    <p>Un chatbot utilisant LangChain et Streamlit pour interroger des fichiers PDF.</p>
    
    <h2>Installation</h2>
    <p>Créer un environnement virtuel et installer les dépendances :</p>
    <pre><code>python -m venv venv</code></pre>
    <pre><code>venv\Scripts\activate</code></pre>
    <pre><code>pip install -r requirements.txt</code></pre>
    
    <h2>Exécution</h2>
    <p>Lancer l'application Streamlit :</p>
    <pre><code>streamlit run pdf_rag.py</code></pre>
    
    <h2>Capture d'écran</h2>
    <p>Interface du chatbot :</p>
    <img src="imgs/image.png" alt="Capture d'écran du chatbot">
</body>
</html>
