from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import CSVLoader
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv

load_dotenv()

class VectorStoreBuilder:
    def __init__(self, csv_path: str, persist_dir: str="chroma_db"):
        self.csv_path = csv_path
        self.persist_dir = persist_dir
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    def build_and_save_vector_store(self):
        # Load CSV data
        loader = CSVLoader(file_path=self.csv_path, encoding='utf-8')
        documents = loader.load()

        # Split text into manageable chunks
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        split_docs = text_splitter.split_documents(documents)

        # Create and persist the vector store
        vector_store = Chroma.from_documents(
            split_docs,
            self.embeddings,
            persist_directory=self.persist_dir
        )
        vector_store.persist()

        print(f"Vector store created and saved to {self.persist_dir}")
        return vector_store
    
    def load_vector_store(self):
        # Load the existing vector store
        vector_store = Chroma(persist_directory=self.persist_dir, embedding_function=self.embeddings)
        print(f"Vector store loaded from {self.persist_dir}")
        return vector_store
    
# if __name__ == "__main__":
#     builder = VectorStoreBuilder(csv_path='data/processed_anime.csv')
#     #builder.build_and_save_vector_store()
#     # Uncomment the line below to load an existing vector store instead
#     vector_store = builder.load_vector_store()