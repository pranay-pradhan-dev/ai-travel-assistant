# AI Travel Planning Assistant

A context-aware AI travel assistant for Singapore that combines:

- Retrieval-Augmented Generation (RAG) for destination knowledge
- Model Context Protocol (MCP) tools for current information
- Gemini Flash for grounded response generation
- Chroma for semantic vector search
- Streamlit for the conversational user interface

The assistant can answer questions about Singapore attractions, transportation,
travel tips, activities and itineraries while retrieving current weather
forecasts and currency conversion information through MCP tools.

---

## Features

### Singapore Destination Knowledge using RAG

The application uses a document-based Singapore travel knowledge base to answer
questions about:

- Major attractions
- Neighbourhoods
- Transportation
- Cultural experiences
- Practical travel guidance
- Food and local experiences
- Indoor and outdoor activities
- Suggested itineraries

Destination facts are retrieved from the knowledge base before being supplied
to the LLM.

The application displays the sources used when generating an answer.

---

### Weather Information using MCP

Current Singapore weather information is retrieved through a dedicated MCP
weather tool.

The MCP server communicates with an external weather service and returns
forecast information including:

- Date
- Maximum temperature
- Minimum temperature
- Precipitation probability
- Weather code

The AI application