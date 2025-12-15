# OllamaAiAgent
An local ai agent run on local device with ollama server

## Setup
make sure you have download and install ollama on your pc.

After that, you also need to download the LLMs in the ```config.json```:

To run this project, please run ollama server first.

There two ways to run this:

1. command line app: You just need to run the ```CommandLineApp.py``` and done.

2. langgraph chat ui: You should install the dependencies in the ```requirements.txt```, chang the ```model_name``` value in the ```LanggraphChatUi.py```, run the command ```langgraph dev``` in the command line and the path is the root dictory.

## Customize

You can download additional LLM to the ollama and use it.

You just need to add new description of the LLM to the ```config.json```, follow the others in the ```models``` key. 