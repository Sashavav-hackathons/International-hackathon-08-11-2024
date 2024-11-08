import numpy as np
from langchain_text_splitters import RecursiveCharacterTextSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from openai import OpenAI
import scipy.spatial.distance as ds
import torch.nn as nn
import torch
import chromadb
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import VectorStoreIndex
from llama_index.core import Settings
from transformers import AutoTokenizer, AutoModel


def RecursiveChunker(name: str, chunk_size=200) -> str:
    """
    Deprecated, use create_chunk_db instead
    :param name:
    :param chunk_size:
    :return:
    """
    f = open("../data/" + name, "r", encoding="utf-8")
    s = f.read()
    text_splitter = RecursiveCharacterTextSplitter(
        # Set a really small chunk size, just to show.
        chunk_size=200,
        chunk_overlap=20,
        length_function=len,
        is_separator_regex=False,
    )
    new_path = "../data/chunked_" + name
    docs = text_splitter.split_text(s)
    pf = open(new_path, "w", encoding="utf-8")
    for doc in docs:
        pf.write(doc + "\n" + "-" * 30 + "\n")
    return new_path


def LLMChanker(name: str) -> str:
    """
    Deprecated, use create_chunk_db instead
    :param name:
    :return:
    """
    # Point to the local server
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

    RULES = (
        "Always answer on russian. For each text, that i give you you should respond me with the text, that has only"
        " russian letters, comma and dot sign. You should semantic split this text on parts and return them, "
        "you should not respond with any information that is not included in that text, you should avoid all"
        " unnecessary words and constructions, you should focus only on your task, you will be tipped with 100$"
        " if you make everything like i said")

    def ask_question(question):
        completion = client.chat.completions.create(
            model="model-identifier",
            messages=[
                {"role": "system", "content": RULES},
                {"role": "user", "content": question}
            ],
            temperature=0.7,
        )

        return completion.choices[0].message.content

    f = open("../data/" + name, "r", encoding='utf-8')
    s = f.read()
    s = s.replace("\n", " ")
    new_path = "../data/chunked_" + name
    pf = open(new_path, "w", encoding='utf-8')
    for i in range(100, len(s) - 100, 300):
        answer = ask_question(s[i - 100:i + 400])
        pf.write(answer)
    return new_path


def get_embeddings(texts, model="BAAI/bge-m3"):
    """
    Deprecated, use create_chunk_db instead
    :param texts:
    :param model:
    :return:
    """
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
    # Ensure texts are properly formatted
    texts = [text.replace("\n", " ") for text in texts]
    return client.embeddings.create(input=texts, model=model).data


def search_in_chunks(chunk_vectors: np.array, query: np.array, k=5) -> np.array:
    """
    Deprecated, use find_best_in_db instead
    :param chunk_vectors:
    :param query:
    :param k:
    :return:
    """
    res = np.empty((k, len(query)))
    best_indexes = [-1] * k
    for x in chunk_vectors:
        if len(x) != len(query):
            raise ValueError("Vector lengths do not match")

        # Example usage
        texts = x
        embeddings = get_embeddings(texts)
        input1 = torch.tensor(embeddings[0].embedding)
        texts = query
        embeddings = get_embeddings(texts)

        cos = nn.CosineSimilarity(dim=0, eps=1e-6)
        input2 = torch.tensor(embeddings[0].embedding)
        output = cos(input1, input2)
        if output > min(best_indexes):
            i = best_indexes.index(min(best_indexes))
            best_indexes[i] = output
            res[i] = x
    return res


class Chunker:
    def __init__(self, path: str):
        self.retrieval_engine = None
        self.path = path
        self.data_path = path + "\\rag\\data\\"
        self.prepared_data_path = self.data_path + "prepared"
        self.chroma_db_path = self.data_path + "chroma_db"
        self.chroma_collection_name = "default"
        self.host = "http://localhost:1234/v1"
        self.index = None


    def prepare_data(self):
        # TODO THIS
        return self.path

    def create_chunk_db(self):
        embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-m3")
        Settings.embed_model = embed_model
        documents = SimpleDirectoryReader(self.prepared_data_path).load_data()
        db = chromadb.PersistentClient(path=self.chroma_db_path)
        chroma_collection = db.get_or_create_collection(self.chroma_collection_name)
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        index = VectorStoreIndex.from_documents(
            documents, storage_context=storage_context, show_progress=True
        )
        return index

    def find_best_in_db(self, query: str, k: int) -> list[str]:
        if self.index is None:
            embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-m3")
            Settings.embed_model = embed_model
            db = chromadb.PersistentClient(path=self.chroma_db_path)

            chroma_collection = db.get_or_create_collection(self.chroma_collection_name)
            vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
            storage_context = StorageContext.from_defaults(vector_store=vector_store)
            self.index = VectorStoreIndex.from_vector_store(
                vector_store, storage_context=storage_context, show_progress=True
            )
            # query_engine = index.as_query_engine(llm="BAAI/bge-m3")
            # response = query_engine.query("Кто такой генрих 13?")
            self.retrieval_engine = self.index.as_retriever()
        response = self.retrieval_engine.retrieve(query)
        return list(response[i].text for i in range(len(response)))
