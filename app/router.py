from fastapi import APIRouter, Request
from app.schemas import GenerateRequest, GenerateResponse, VoteRequest, GeneratePayload, GenerationResponse
from app.generator import generate
import logging
import uuid
from httpx import AsyncClient
from fastapi import Header, HTTPException, Body
import yaml

router = APIRouter()
logger = logging.getLogger(__name__)

_sessions = {}

with open("config.yaml") as f:
    model_config = yaml.safe_load(f)["models"]

def get_model_url(model_id: str) -> str:
    if model_id not in model_config:
        raise HTTPException(status_code=404, detail="Model not found")
    return model_config[model_id]["url"]


@router.post("/generate", response_model=GenerateResponse)
async def generate_api(payload: GeneratePayload = Body(...), authorization: str = Header(None)):
    """
    Endpoint to generate a response based on the provided prompt.
    """
    authorization = {
        "Authorization": "Bearer token-abc123"
    }

    gen_prompt = payload.request
    model = payload.model
    model_id = payload.model.model_id

    model_url = get_model_url(model_id)

    async with AsyncClient() as client:
        response = await generate(model_url=model_url, prompt=gen_prompt, model=model, client=client, headers=authorization)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="vLLM backend error")

    outputs = GenerationResponse(
        model_name=model.model_name,
        output=response.json()["choices"][0]["text"],
        prompt=gen_prompt.prompt
    )
    # Simulate generation time
    session_id = str(uuid.uuid4())

    logger.info(f"Received prompt: {gen_prompt.prompt} for session: {session_id}, with outputs: {outputs}")
    _sessions[session_id] = outputs

    return GenerateResponse(
        session_id=session_id,
        generations=outputs,
    )
    
@router.post("/vote")
async def vote(vote_request: VoteRequest):
    """
    Endpoint to vote on a generated response.
    """
    logger.info(f"Vote received: session={vote_request.session_id}, model={vote_request.selected_model}")
    # Storing into DB
    return {"status": "vote received"}

@router.get("/results/{session_id}")
async def get_results(session_id: str):
    """
    Endpoint to get the results of a voting session.
    """
    logger.info(f"Results requested for session: {session_id}")

    results = _sessions[session_id]
    return {"session_id": session_id, "results": results}

@router.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    logger.info("Health check")
    return {"status": "200 OK", "message": "Service is running"}

@router.get("/models")
async def get_models(session_id: str):
    """
    Endpoint to get the list of available models.
    """
    logger.info(f"Models requested for session: {session_id}")
    # Mock models
    models = [f"model-{i}" for i in range(4)]
    return {"models": models}