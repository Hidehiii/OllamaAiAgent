from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun, DuckDuckGoSearchResults
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper

@tool
def duck_duck_go_search_with_simple_result(query: str) -> str:
    """
    Perform a simple DuckDuckGo search and return the results.
    :param query: The search query.
    :return: The search results as a string.
    """
    search_tool = DuckDuckGoSearchRun()
    results = search_tool.invoke(query)
    return results

@tool
def duck_duck_go_search_with_detail_result(query: str) -> str:
    """
    Perform a detailed DuckDuckGo search and return the results with more details.
    :param query: The search query.
    :return: The detailed search results as a string.
    """
    search_tool = DuckDuckGoSearchResults()
    results = search_tool.invoke(query)
    return results

@tool
def duck_duck_go_search_with_specific_parameter(query: str, region: str, time: str, source: str) -> str:
    """
    Perform a DuckDuckGo search with specific parameters and return the results.
    :param query: The search query.
    :param region: The region for the search (e.g., "us-en").
    :param time: The time filter for the search (e.g., "d" for day, "w" for week).
    :param source: The source type for the search (e.g., "web", "news").
    :return: The search results as a string.
    """
    search_wrapper = DuckDuckGoSearchAPIWrapper(region=region, time=time, source=source)
    search_tool = DuckDuckGoSearchResults(search_wrapper=search_wrapper, source=source)
    results = search_tool.invoke(query)
    return results