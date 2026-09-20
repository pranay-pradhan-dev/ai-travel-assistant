from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


DATA_DIR = Path("data/singapore")
CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "singapore_travel"


SOURCE_METADATA = {
    "singapore_wikivoyage.pdf": {
        "source_title": "Wikivoyage Singapore Travel Guide",
        "source_url": "https://en.wikivoyage.org/wiki/Singapore",
    },
    "singapore_essential_information.pdf": {
        "source_title": "Visit Singapore - Essential Travel Information",
        "source_url": "https://www.visitsingapore.com/travel-tips/essential-travel-information/",
    },
    "singapore_itineraries.pdf": {
        "source_title": "Singapore Trip Planner - Headout",
        "source_url": "https://www.headout.com/blog/trip-planner-singapore-itineraries/",
    },
}


def load_documents():
    documents = []

    for pdf_path in DATA_DIR.glob("*.pdf"):

        print(f"Loading: {pdf_path.name}")

        loader = PyPDFLoader(str(pdf_path))
        pages = loader.load()

        metadata = SOURCE_METADATA.get(
            pdf_path.name,
            {
                "source_title": pdf_path.stem,
                "source_url": "",
            },
        )

        for page in pages:
            page.metadata.update(metadata)

        documents.extend(pages)

    return documents


def split_documents(documents):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
    )

    chunks = text_splitter.split_documents(documents)

    return chunks


def create_vector_store(chunks):

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_DIR,
    )

    return vector_store


def main():

    print("Starting Singapore knowledge-base ingestion...")

    documents = load_documents()

    if not documents:
        print(
            "No PDF documents found in "
            "data/singapore/"
        )
        return

    print(f"Loaded {len(documents)} document pages.")

    chunks = split_documents(documents)

    print(f"Created {len(chunks)} chunks.")

    create_vector_store(chunks)

    print("Vector store created successfully.")
    print(f"Location: {CHROMA_DIR}")


if __name__ == "__main__":
    main()