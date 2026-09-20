from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "singapore_travel"


def get_vector_store():

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    return Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings,
    )


def retrieve_documents(query: str, k: int = 4):

    vector_store = get_vector_store()

    return vector_store.similarity_search(
        query,
        k=k,
    )


def retrieve_documents_with_scores(
    query: str,
    k: int = 4,
):

    vector_store = get_vector_store()

    return vector_store.similarity_search_with_score(
        query,
        k=k,
    )


if __name__ == "__main__":

    query = "What are the major attractions in Singapore?"

    results = retrieve_documents_with_scores(
        query,
        k=4,
    )

    print(f"\nQuery: {query}")
    print("=" * 70)

    for index, (document, score) in enumerate(
        results,
        start=1,
    ):

        print(f"\nRESULT {index}")
        print("-" * 70)

        print(f"Score: {score:.4f}")

        print(
            "Source:",
            document.metadata.get(
                "source_title",
                "Unknown",
            ),
        )

        print(
            "URL:",
            document.metadata.get(
                "source_url",
                "Unknown",
            ),
        )

        print()

        print(document.page_content[:700])