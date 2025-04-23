from typing import TypedDict
import pydantic
from pydantic import BaseModel, Field


class ModelArguments(TypedDict):
    """
    Arguments for the model.
    """
    max_tokens: int = Field(100, description="Maximum number of tokens to generate.")
    temperature: float = Field(0.7, description="Sampling temperature for generation.")
    top_p: float = Field(1.0, description="Top-p sampling for generation.")
    top_k: int = Field(50, description="Top-k sampling for generation.")

class Model(BaseModel):
    """
    Model configuration.
    """
    model_id: str = Field(..., description="The ID of the model used for gateaway routing.")
    model_name: str = Field(..., description="The name of the model.")
    args: ModelArguments = Field(..., description="Arguments for the model.")

class GenerateRequest(BaseModel):
    """
    Request model for generating a response.
    """
    prompt: str = Field(..., description="The prompt to generate a response for.")

class GeneratePayload(BaseModel):
    request: GenerateRequest
    model: Model

class GenerationResponse(BaseModel):
    """
    Response model for the generated response.
    """
    model_name: str = Field(..., description="The name of the model used for generation and vLLM.")
    prompt: str = Field(..., description="The prompt used for generation.")
    output: str = Field(..., description="The generated output.")

class GenerateResponse(BaseModel):
    """
    Response model for the generation endpoint.
    """
    session_id: str = Field(..., description="The session ID for the generation request.")
    generations: GenerationResponse = Field(..., description="List of generated responses.")

class VoteRequest(BaseModel):
    """
    Request model for voting on a generation.
    """
    session_id: str = Field(..., description="The session ID for the generation request.")
    selected_model: str = Field(..., description="The ID of the selected model.")