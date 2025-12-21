from Tools import System
from Tools import DuckDuckGoSearch
from Tools import Algorithm

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

    System.read_file_binary,
    System.read_image_file_as_base64,

    System.take_screenshot,

    # DuckDuckGoSearch
    DuckDuckGoSearch.duck_duck_go_search_with_simple_result,
    DuckDuckGoSearch.duck_duck_go_search_with_detail_result,
    DuckDuckGoSearch.duck_duck_go_search_with_specific_parameter,

    # Algorithm
    Algorithm.encode_base64_from_image_bytes,
]