# FastAPI-based LLM Router

This project is a simple and modular FastAPI server designed for routing text generation requests to different large language models (LLMs). It allows flexible selection of models and devices (CPU/GPU) through request parameters.

## Features

- Support for multiple language models (e.g., GPT-2, LLaMA, Mistral)
- Model selection via API request
- Device selection (CPU or GPU)
- Clean and extendable codebase
- Basic authentication
- Logging support
- Jupyter notebook for testing


## Project Structure

```
app/
├── auth.py         # Optional authentication layer
├── generator.py    # Inference logic and model/device selection
├── logger.py       # Logging configuration
├── main.py         # FastAPI application entry point
├── router.py       # Request routing and API endpoints
├── schemas.py      # Pydantic models for input/output validation
├── test.ipynb      # Notebook for manual testing
```

## Background

By default, most VLLM-based setups do not support serving multiple models simultaneously. This project addresses that limitation by wrapping VLLM model instances within a FastAPI server. The server exposes multiple endpoints for different models, handles device assignment, and provides logging and metrics. This makes it easier to manage multiple generation backends in a unified and extensible way.

## Notes

- You can switch between models and devices using parameters in the request body.
- The code is structured to make it easy to extend with new models or routes.
