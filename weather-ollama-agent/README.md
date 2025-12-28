# Semantic Kernel Agent Framework with the open source model llama3.2:1b (~ 1GB of RAM)

## Configuration
1. Install ollama cli with docker (or install directly from https://ollama.com/download/linux)
   1. Create Dockerfile
       ```
       FROM ollama/ollama:latest
       ENV OLLAMA_HOST=0.0.0.0
       ENV OLLAMA_MODELS=/root/.ollama
       EXPOSE 11434
       ```
   2. Build the image
      ```
      docker build -t ollama32-1b .
      ```
   3. Run ollama container service and install ollama model
      ```
      docker run -d -p 11434:11434 -v ./ollama_models:/root/.ollama --name ollama32-1b-server ollama32-1b
      docker exec -it ollama32-1b-server bash -c "ollama pull llama3.2:1b"
      ```
   4. Test ollama model on localhost
      ```
      curl http://localhost:11434/api/generate -d '{"model": "llama3.2:1b","prompt": "Why is the sky blue?"}'
      ```
2. Configure the .env file
   1. Add the .env file at weather-ollama-agent/.env
   2. Configure properly the variables
      ```
      # Adjust the settings to align with your preferences
      OLLAMA_HOST=http://localhost:11434
      OLLAMA_MODEL=llama3.2:1b
      ```
