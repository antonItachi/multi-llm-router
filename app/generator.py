import httpx
from httpx import AsyncClient
from app.schemas import GenerationResponse, Model, GenerateRequest
from app.auth import init_authorization


async def generate(model_url: str, prompt: GenerateRequest, model: Model, client: AsyncClient, headers: dict) -> GenerationResponse:
    """
    Generate a response using the specified model and prompt.
    """
    
    model_name = model.model_name
    prompt = prompt.prompt

    response = await client.post(
        f"{model_url}/v1/completions",
        headers=headers,
        json={
            "model": model_name,
            "prompt": prompt,
            **model.args,
        },
        timeout=60,
    )

    return response