from fastapi import Header, HTTPException, status

async def init_authorization(api_key: str):
    """
    Validate the API key for authorization.
    """
    if api_key is not None:
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
    else:
        headers = {}
    
    return headers
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{model.api_url}/v1/engines/{model.model_id}/completions",
            headers=headers,
        )
        
        if response.status_code == status.HTTP_401_UNAUTHORIZED:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API key",
            )
        elif response.status_code != status.HTTP_200_OK:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to validate API key",
            )