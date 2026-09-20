import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from rag.retriever import retrieve_documents
from agent.prompts import RAG_SYSTEM_PROMPT


load_dotenv()


def get_llm():
    model_name = os.getenv(
        "GEMINI_MODEL",
        "gemini-3.6-flash",
    )

    return ChatGoogleGenerativeAI(
        model=model_name,
        temperature=0.2,
        google_api_key=os.getenv("GOOGLE_API_KEY"),
    )


def build_context(documents):
    context_parts = []

    for index, document in enumerate(documents, start=1):
        source_title = document.metadata.get(
            "source_title",
            "Unknown source",
        )

        source_url = document.metadata.get(
            "source_url",
            "",
        )

        context_parts.append(
            f"""
SOURCE {index}
Title: {source_title}
URL: {source_url}

Content:
{document.page_content}
"""
        )

    return "\n".join(context_parts)


def build_sources(documents):
    sources = []
    seen = set()

    for document in documents:
        title = document.metadata.get(
            "source_title",
            "Unknown source",
        )

        url = document.metadata.get(
            "source_url",
            "",
        )

        source_key = (title, url)

        if source_key not in seen:
            seen.add(source_key)
            sources.append(
                f"- {url}"
                if url
                else f"- {title}"
            )

    return "\n".join(sources)


def process_message(user_message: str) -> str:

    # Retrieve Singapore knowledge
    documents = retrieve_documents(
        user_message,
        k=4,
    )

    if not documents:
        return (
            "The knowledge base does not contain enough "
            "information to answer this question."
        )

    # Build grounding context
    context = build_context(documents)

    # Build prompt
    prompt = RAG_SYSTEM_PROMPT.format(
        context=context,
        question=user_message,
    )

    # Call Gemini
    llm = get_llm()

    response = llm.invoke(prompt)
    answer = extract_response_text(response)

    # Build source list
    sources = build_sources(documents)

    return f"""
{answer}

### Sources

{sources}
"""

def extract_response_text(response) -> str:
    content = response.content

    # Normal string response
    if isinstance(content, str):
        return content

    # Gemini may return structured content blocks
    if isinstance(content, list):
        text_parts = []

        for block in content:
            if isinstance(block, dict):
                if block.get("type") == "text":
                    text = block.get("text", "")

                    if text:
                        text_parts.append(text)

            elif isinstance(block, str):
                text_parts.append(block)

        return "\n".join(text_parts)

    return str(content)