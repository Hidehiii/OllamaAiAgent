# OllamaAiAgent
An local ai agent run on local device with ollama server

## Setup
make sure you have download and install ollama on your pc.

After that, you also need to download the LLMs in the ```config.json```:

To run this project, please run ollama server first.

There two ways to run this:

1. command line app: You just need to run the ```CommandLineApp.py``` and done.

2. langgraph chat ui: You should install the dependencies in the ```requirements.txt```, chang the ```model_name``` value in the ```LanggraphChatUi.py```, run the command ```langgraph dev``` in the command line and the path is the root dictory.

### Issues
#### There are some issues when using langgraph chat ui:
When you upload an image to langgraph chat ui and send it to you agent, it will trigger an error ```"Error: Unsupported message content type. Must either have type 'text' or type 'image_url' with a string 'image_url' field."``` 

This is because the image data block the ui send to you model is not corret, it miss something.

To fix this, you need to download the chat ui repository, go to ```agent-chat-ui/src/lib/multimodal-utils.ts```find the code block in function ```fileToContentBlock```:

``` 
if (supportedImageTypes.includes(file.type)) {
    return {
      type: "image",
      mimeType: file.type,
      data,
      metadata: { name: file.name },
    };
}
```

add some key-value pair:

```
if (supportedImageTypes.includes(file.type)) {
    return {
        type: "image",
        mimeType: file.type,
        base64: data,
        data: data,
        mime_type: file.type,
        metadata: { name: file.name },
    };
}
```

after that, run it follow the guidance in ```https://docs.langchain.com/oss/python/langchain/ui```

## Customize

You can download additional LLM to the ollama and use it.

You just need to add new description of the LLM to the ```config.json```, follow the others in the ```models``` key. 