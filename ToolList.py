from Tools import System
from Tools import DuckDuckGoSearch

TOOL_LIST=[
    # System
    System.get_current_directory,
    System.get_current_date,
    System.get_current_time,

    # DuckDuckGoSearch
    DuckDuckGoSearch.duck_duck_go_search_simple_result,
    DuckDuckGoSearch.duck_duck_go_search_detail_result,
]