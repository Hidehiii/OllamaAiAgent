from langgraph.types import StreamMode

def convert_agent_stream_output_to_readable_text(node, content, stream_mode : StreamMode):
    if stream_mode == "messages":
        if len(content) == 0:
            return "\n"
        elif len(content) == 1 and node == "model":
            data = content[0]
            if data["type"] == "tool_call_chunk":
                if data["name"] is not None:
                    return f"using tools: " + data["name"]
                if data["args"] != "":
                    return data["args"]
                raise ValueError("Tool call chunk must have either name or args.")
            elif data["type"] == "text":
                return data["text"]
            else:
                raise ValueError(f"Unknown content type: {data['type']}")
        elif len(content) == 1 and node == "tools":
            data = content[0]
            if data["type"] == "text":
                return "tools return value: " + data["text"] + "\n"
            else:
                raise ValueError(f"Unknown content type: {data['type']}")
        else:
            raise ValueError("Agent stream output must have only one element.")
    else:
        raise ValueError(f"Unsupported stream mode: {stream_mode}")

def print_agent_stream_response(agent_response, stream_mode : StreamMode):
    print("======================AI Response======================")
    if stream_mode == "messages":
        for token, meta in agent_response:
            print(convert_agent_stream_output_to_readable_text(meta['langgraph_node'], token.content_blocks, stream_mode), end="")
    else:
        raise ValueError(f"Unsupported stream mode: {stream_mode}")