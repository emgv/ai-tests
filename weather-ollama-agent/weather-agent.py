import asyncio
import os
from decimal import Decimal
from semantic_kernel import Kernel
from semantic_kernel.functions import kernel_function
from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread
from semantic_kernel.connectors.ai.ollama import OllamaChatCompletion
from dotenv import load_dotenv
import requests

async def main():

    load_dotenv()
    
    kernel = Kernel()
    kernel.add_service(
        OllamaChatCompletion(
            host=os.environ["OLLAMA_HOST"],
            ai_model_id=os.environ["OLLAMA_MODEL"])
    )

    agent = ChatCompletionAgent(
        description="Weather forecast assistant that can chat and use tools.",
        instructions="""You are a weather forecast assistant.
                       When a user submits the latitude and longitude you can use the plugin function get_temperature
                       to get the current temperature in Cº.
                       For example: temperature at longitude=70.504719 and latitude=25.053606?
                       you can call the function like so get_temperature(25.053606, 70.504719) """,
        kernel=kernel,
        plugins=[WeatherPlugin()]
    )

    thread = ChatHistoryAgentThread()

    while True:
        user_input = input("Ask the agent: ")
        if user_input=="quit":
            return
        
        print("[== Info ==]: Reading the responses from the agent")

        async for agent_response in agent.invoke(messages=user_input, thread=thread):
            print(agent_response.content)

        print("[== Info ==]: Done")

class WeatherPlugin:
    """A plugin with functions to help on questions about weather"""

    @kernel_function(description="Get the temperature in Celsius given the latitude and longitude as 2 decimal values at 2m above sea level")
    def get_temperature(self, latitude: Decimal, longitude: Decimal) -> str:
        try:
            base_uri = "https://api.open-meteo.com/v1"
            query_params = {
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m"
            }

            print(f"[== Info ==]: Checking with open-meteo the temperature at {latitude} {longitude}")
            response = requests.get(f"{base_uri}/forecast", params=query_params)
            if not response.ok:
                return f"The open-meteo server responded with status code {response.status_code}"
            
            response_json = response.json()
            current = response_json.get("current") or {}
            if not current:
                return "Could not get the current forecast"
            
            temperature_2m = current.get("temperature_2m") or {}
            if not temperature_2m:
                return "Could not get the current forecast for the parameter temperature_2m"
            
            return temperature_2m
        except BaseException as e:
            message = "An error occurred while requesting the weather forecast to open-meteo"
            print(f"{message} {e}")
            return message

if __name__ == "__main__":
    asyncio.run(main())

# open-meto API for weather forecast
# https://api.open-meteo.com/v1/forecast?latitude=70.5047191726878&longitude=25.053606584556558&current=temperature_2m

# what is the temperature at latitude 70.50645 longitude 25.065948?
# {
#   "latitude": 70.50645,
#   "longitude": 25.065948,
#   "generationtime_ms": 0.0576972961425781,
#   "utc_offset_seconds": 0,
#   "timezone": "GMT",
#   "timezone_abbreviation": "GMT",
#   "elevation": 24,
#   "current_units": {
#     "time": "iso8601",
#     "interval": "seconds",
#     "temperature_2m": "°C"
#   },
#   "current": {
#     "time": "2025-11-28T23:45",
#     "interval": 900,
#     "temperature_2m": -3.3
#   }
# }

# https://ollama.com/library/llama3.2
# llama3.2:1b ~ 1GB of RAM

# Create Dockerfile
# FROM ollama/ollama:latest
# ENV OLLAMA_HOST=0.0.0.0
# ENV OLLAMA_MODELS=/root/.ollama
# EXPOSE 11434

# build ollama image
# sudo docker build -t ollama32-1b .

# run ollama container service and install ollama model
# docker run -d -p 11434:11434 -v ./ollama_models:/root/.ollama --name ollama32-1b-server ollama32-1b
# sudo docker exec -it ollama32-1b-server bash -c "ollama pull llama3.2:1b"

# test ollama model on localhost:
# curl http://localhost:11434/api/generate -d '{"model": "llama3.2:1b","prompt": "Why is the sky blue?"}'

# /root/.ollama

# To do fine tuning you can use the unsloth library
# https://github.com/unslothai/unsloth
# Requires GPUs, or train the model using google colaboratory:
# https://www.youtube.com/watch?v=pTaSDVz0gok&t=483s
# https://www.youtube.com/watch?v=pxhkDaKzBaY






