import json
import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from agent.extractors import extract_currency_request
from agent.prompts import TRAVEL_ASSISTANT_PROMPT
from agent.router import Intent, detect_intent

from rag.retriever import retrieve_documents

from mcp_tools.weather_client import get_weather
from mcp_tools.currency_client import convert_currency


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


def extract_response_text(response) -> str:

    content = response.content

    if isinstance(content, str):
        return content

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


def build_context(documents):

    parts = []

    for index, document in enumerate(
        documents,
        start=1,
    ):

        title = document.metadata.get(
            "source_title",
            "Unknown source",
        )

        url = document.metadata.get(
            "source_url",
            "",
        )

        parts.append(
            f"""
SOURCE {index}

Title: {title}
URL: {url}

Content:
{document.page_content}
"""
        )

    return "\n".join(parts)


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

        key = (title, url)

        if key in seen:
            continue

        seen.add(key)

        if url:
            sources.append(
                f"- {url}"
            )
        else:
            sources.append(
                f"- {title}"
            )

    return "\n".join(sources)


def format_conversation(
    conversation_history,
):

    if not conversation_history:
        return "No previous conversation."

    history = conversation_history[-6:]

    lines = []

    for message in history:

        role = message.get(
            "role",
            "unknown",
        )

        content = message.get(
            "content",
            "",
        )

        # Avoid huge prompts
        content = content[:1500]

        lines.append(
            f"{role.upper()}: {content}"
        )

    return "\n".join(lines)


def process_message(
    user_message: str,
    conversation_history=None,
) -> str:

    intent = detect_intent(
        user_message
    )

    documents = []

    weather_data = None

    currency_data = None

    errors = []


    # ------------------------------------------
    # RAG
    # ------------------------------------------

    if intent in {
        Intent.RAG_ONLY,
        Intent.RAG_AND_WEATHER,
        Intent.RAG_AND_CURRENCY,
        Intent.RAG_WEATHER_CURRENCY,
    }:

        try:
            documents = retrieve_documents(
                user_message,
                k=4,
            )

        except Exception:
            errors.append(
                "Destination knowledge retrieval failed."
            )


    # ------------------------------------------
    # Weather MCP
    # ------------------------------------------

    