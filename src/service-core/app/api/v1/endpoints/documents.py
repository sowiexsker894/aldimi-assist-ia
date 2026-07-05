from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_current_user, get_document_service
from app.api.schemas.document import (
    BoletaSaveRequest,
    DniSaveRequest,
    DocumentAnalyzeRequest,
    DocumentAnalyzeResponse,
    DocumentSaveResponse,
    RecetaSaveRequest,
)
from app.core.auth_exceptions import ForbiddenActionError
from app.core.document_exceptions import (
    DocumentAnalysisRejectedError,
    DocumentSessionError,
    DocumentValidationError,
)
from app.core.exceptions import ExternalServiceUnavailable
from app.domain.entities.user import User
from app.services.document_service import DocumentService

router = APIRouter()


def _save_response(document) -> DocumentSaveResponse:
    return DocumentSaveResponse(
        id=document.id,
        document_type=document.document_type,  # type: ignore[arg-type]
        patient_id=document.patient_id,
        created_at=document.created_at,
    )


@router.post(
    "/analyze",
    response_model=DocumentAnalyzeResponse,
    summary="Analizar documento vía vision-service",
)
def analyze_document(
    body: DocumentAnalyzeRequest,
    user: Annotated[User, Depends(get_current_user)],
    svc: Annotated[DocumentService, Depends(get_document_service)],
) -> DocumentAnalyzeResponse:
    try:
        result = svc.analyze_document(
            user,
            document_type=body.document_type,
            images_base64=body.images_base64,
            patient_id=body.patient_id,
        )
    except DocumentAnalysisRejectedError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "status": "rejected",
                "rejection": {"code": exc.code, "message": exc.message},
            },
        ) from exc
    except ForbiddenActionError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        ) from exc
    except DocumentValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except ExternalServiceUnavailable as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc

    return DocumentAnalyzeResponse(**result)


@router.post(
    "/dni",
    response_model=DocumentSaveResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Guardar DNI y registrar paciente nuevo",
)
def save_dni_document(
    body: DniSaveRequest,
    user: Annotated[User, Depends(get_current_user)],
    svc: Annotated[DocumentService, Depends(get_document_service)],
) -> DocumentSaveResponse:
    try:
        document = svc.save_dni_document(
            user,
            analysis_session_id=body.analysis_session_id,
            confirmed_fields=body.confirmed_fields,
        )
    except ForbiddenActionError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        ) from exc
    except DocumentSessionError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except DocumentValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return _save_response(document)


@router.post(
    "/boleta",
    response_model=DocumentSaveResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Guardar comprobante de depósito (sin paciente)",
)
def save_boleta_document(
    body: BoletaSaveRequest,
    user: Annotated[User, Depends(get_current_user)],
    svc: Annotated[DocumentService, Depends(get_document_service)],
) -> DocumentSaveResponse:
    try:
        document = svc.save_boleta_document(
            user,
            analysis_session_id=body.analysis_session_id,
            confirmed_fields=body.confirmed_fields,
        )
    except ForbiddenActionError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        ) from exc
    except DocumentSessionError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except DocumentValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return _save_response(document)


@router.post(
    "/receta",
    response_model=DocumentSaveResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Guardar receta vinculada a paciente existente",
)
def save_receta_document(
    body: RecetaSaveRequest,
    user: Annotated[User, Depends(get_current_user)],
    svc: Annotated[DocumentService, Depends(get_document_service)],
) -> DocumentSaveResponse:
    try:
        document = svc.save_receta_document(
            user,
            analysis_session_id=body.analysis_session_id,
            patient_id=body.patient_id,
            confirmed_fields=body.confirmed_fields,
        )
    except ForbiddenActionError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        ) from exc
    except DocumentSessionError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except DocumentValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return _save_response(document)
