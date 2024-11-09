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


class Chunker:
    def __init__(self, path: str):
        self.retrieval_engine = None
        self.path = path
        self.data_path = path + "rag/data/"
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

        def make_item(item):
            s = (f"Из файла с названием {item.metadata['file_name']} со страницы {item.metadata['page_label']}, "
                 f"созданный {item.metadata['creation_date']}")
            s += f"\nИнформация: {item.text}"
            return s

        return list(make_item(response[i]) for i in range(len(response)))
