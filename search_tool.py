from typing import Type

from ddgs import DDGS
from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class SearchInput(BaseModel):
    query: str = Field(
        ...,
        description=(
            "Search query for finding relevant jobs or freelance "
            "opportunities."
        ),
    )


class FreeWebSearchTool(BaseTool):
    name: str = "Free Web Search"
    description: str = (
        "Search the public web for relevant job listings, freelance "
        "opportunities, and company career pages. Returns result "
        "titles, URLs, and descriptions."
    )
    args_schema: Type[BaseModel] = SearchInput

    def _run(self, query: str) -> str:
        try:
            results = []

            with DDGS() as ddgs:
                search_results = ddgs.text(
                    query,
                    max_results=10,
                )

                for item in search_results:
                    title = item.get("title", "No title")
                    url = item.get("href", "")
                    snippet = item.get("body", "")

                    results.append(
                        f"Title: {title}\n"
                        f"URL: {url}\n"
                        f"Description: {snippet}\n"
                    )

            if not results:
                return "No search results found."

            return "\n---\n".join(results)

        except Exception as error:
            return f"Search failed: {error}"
