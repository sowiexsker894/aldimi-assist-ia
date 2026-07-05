from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_nlp_http_client, get_vision_http_client
from app.core.exceptions import ExternalServiceUnavailable
from app.infrastructure.clients.nlp_http_client import NlpHttpClient
from app.infrastructure.clients.vision_http_client import VisionHttpClient

router = APIRouter()


@router.get("/nlp")
def probe_nlp(
    nlp: Annotated[NlpHttpClient, Depends(get_nlp_http_client)],
) -> dict[str, str | bool]:
    try:
        detail = nlp.ask_regulation("ping")
        return {"service": "nlp", "ok": True, "detail": detail}
    except ExternalServiceUnavailable as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"service": exc.service, "message": str(exc)},
        ) from exc


@router.get("/vision")
def probe_vision(
    vision: Annotated[VisionHttpClient, Depends(get_vision_http_client)],
) -> dict[str, str | bool]:
    try:
        detail = vision.ping()
        return {"service": "vision", "ok": True, "detail": str(detail)}
    except ExternalServiceUnavailable as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"service": exc.service, "message": str(exc)},
        ) from exc
