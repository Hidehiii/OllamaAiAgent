from langchain.tools import tool
import base64

@tool
def encode_base64_from_image_bytes(
        data: bytes,
        format: str,
        add_prefix: bool = True) -> str:
    """
    Encode image's bytes data to base64 string.
    :param data:  The bytes data to encode.
    :param format:  The image format, e.g., "png", "jpeg".
    :param add_prefix:  Whether to add the data URI prefix.
    :return:  Base64 encoded string.
    """
    encoded_data = base64.b64encode(data).decode('utf-8')
    if add_prefix:
        return f"data:image/{format};base64,{encoded_data}"
    return encoded_data