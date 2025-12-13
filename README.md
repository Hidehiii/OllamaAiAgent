# OllamaAiAgent
An local ai agent run on local device with ollama server

## Setup
make sure you have download and install ollama on your pc.

After that, you also need to download the LLM, here is the list:

```
ollama pull llama3.2:3b

ollama pull deepseek-r1:8b

ollama pull granite3-dense

ollama pull granite3.2-vision

ollama pull llama3-groq-tool-use

ollama pull phi4-mini
```

To run this project, please run ollama server first.

And run the  ```main.py```

## Customize

You can download additional LLM to the ollama and use it.

You just need to add new description of the LLM to the ```config.json```, follow the others in the ```models``` key. And add your LLM's initialization to the ```select_agent()``` function in the file ```AgentLoader.py```