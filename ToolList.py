from Tools import System
from Tools import DuckDuckGoSearch

TOOL_LIST=[
    # System
    System.get_current_directory,
    System.get_current_date,
    System.get_current_time,

    System.read_file,
    System.write_file,
    System.list_directory,
    System.copy_file,
    System.delete_file,
    System.file_search,
    System.move_file,

    System.take_screenshot,

    # DuckDuckGoSearch
    DuckDuckGoSearch.duck_duck_go_search_with_simple_result,
    DuckDuckGoSearch.duck_duck_go_search_with_detail_result,
    DuckDuckGoSearch.duck_duck_go_search_with_specific_parameter,
]