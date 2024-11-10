import chromadb
from get_project_root import root_path
from llama_index.core import Settings
from llama_index.core import SimpleDirectoryReader
from llama_index.core import StorageContext
from llama_index.core import VectorStoreIndex
from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.core.schema import NodeWithScore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore


class Chunker:
    def __init__(self, path: str = root_path(ignore_cwd=False)):
        self.db = None
        self.vector_store = None
        self.chroma_collection = None
        self.storage_context = None
        self.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-m3")
        self.retrieval_engine = None
        self.path = path
        self.data_path = path + "\\rag\\data\\"
        self.prepared_data_path = self.data_path + "prepared"
        self.new_data_path = self.data_path + "new_files"
        self.chroma_db_path = self.data_path + "chroma_db"
        self.chroma_collection_name = "default"
        self.host = "http://localhost:1234/v1"
        self.index = None

    def init_db(self, k: int):
        if self.index is None:
            Settings.embed_model = self.embed_model
            self.db = chromadb.PersistentClient(path=self.chroma_db_path)

            self.chroma_collection = self.db.get_or_create_collection(self.chroma_collection_name)
            self.vector_store = ChromaVectorStore(chroma_collection=self.chroma_collection)
            self.storage_context = StorageContext.from_defaults(vector_store=self.vector_store)
            self.index = VectorStoreIndex.from_vector_store(
                self.vector_store, storage_context=self.storage_context, show_progress=True
            )
            # query_engine = index.as_query_engine(llm="BAAI/bge-m3")
            # response = query_engine.query("Кто такой генрих 13?")
            self.retrieval_engine = self.index.as_retriever(
                similarity_top_k=k,
                choice_batch_size=2,
            )

    def add_file(self, path: str):
        embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-m3")
        Settings.embed_model = embed_model
        documents = SimpleDirectoryReader(self.new_data_path).load_data()
        db = chromadb.PersistentClient(path=self.chroma_db_path)
        chroma_collection = db.get_or_create_collection(self.chroma_collection_name)
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        VectorStoreIndex.from_documents(
            documents=documents,
            storage_context=storage_context,
            show_progress=True
        )

    def create_chunk_db(self):
        embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-m3")
        Settings.embed_model = embed_model
        semantic_embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-m3")
        semantic_splitter = SemanticSplitterNodeParser(
            buffer_size=2,
            embed_model=semantic_embed_model
        )
        documents = SimpleDirectoryReader(self.prepared_data_path).load_data()
        nodes = semantic_splitter.get_nodes_from_documents(documents)

        # Connect to the database
        db = chromadb.PersistentClient(path=self.chroma_db_path)
        chroma_collection = db.get_or_create_collection(self.chroma_collection_name)
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        # Create the index using the semantically chunked nodes
        index = VectorStoreIndex(
            nodes,
            storage_context=storage_context,
            show_progress=True
            # insert_batch_size=1024
        )

        return index

    def find_best_in_db(self, query: str, k: int, min_score: int = 0.3) -> list[str]:
        self.init_db(k)
        response = self.retrieval_engine.retrieve(query)

        def make_item(item : NodeWithScore) -> str:
            # print(item.score, end=" ")
            if item.score < min_score:
                return ""
            if item.metadata.__contains__("page_label"):
                s = (f"Файл {item.metadata['file_name']}, страница {item.metadata['page_label']} | "
                     f"Дата создания: {item.metadata['creation_date']}")
            else:
                s = (f"Файл {item.metadata['file_name']} | "
                     f"Дата создания: {item.metadata['creation_date']}")
            s += f"\nСодержание файла: {item.text}"
            return s

        return list(make_item(response[i]) for i in range(len(response)))
