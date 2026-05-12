import base64
import binascii
import re

import cv2
import numpy as np


_DATA_URL_RE = re.compile(
    r"^data:(?P<mime>[\w/+.-]+);base64,(?P<b64>[A-Za-z0-9+/=]+)$", re.ASCII
)


def strip_data_url_prefix(value: str) -> str:
    text = value.strip()
    m = _DATA_URL_RE.match(text.replace("\n", "").replace("\r", ""))
    if m:
        return m.group("b64")
    return text.replace("\n", "").replace("\r", "")


def preprocess_to_jpeg_data_url(
    image_base64: str,
    *,
    jpeg_quality: int,
    max_width: int,
) -> tuple[str, int]:
    """Decodifica imagen, limpia con OpenCV y devuelve data URL JPEG + tamaño en bytes del JPEG."""
    raw_b64 = strip_data_url_prefix(image_base64)
    try:
        raw_bytes = base64.b64decode(raw_b64, validate=True)
    except (ValueError, binascii.Error) as exc:
        raise ValueError("Base64 de imagen inválido") from exc

    arr = np.frombuffer(raw_bytes, dtype=np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("No se pudo decodificar la imagen (formato no soportado o corrupto)")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    denoised = cv2.fastNlMeansDenoising(
        enhanced, h=10, templateWindowSize=7, searchWindowSize=21
    )

    h, w = denoised.shape[:2]
    if w > max_width and max_width > 0:
        scale = max_width / float(w)
        new_w = int(w * scale)
        new_h = int(h * scale)
        denoised = cv2.resize(
            denoised, (new_w, new_h), interpolation=cv2.INTER_AREA
        )

    ok, buf = cv2.imencode(
        ".jpg",
        denoised,
        [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality],
    )
    if not ok or buf is None:
        raise ValueError("Error al codificar JPEG tras preprocesado")

    jpeg_bytes = buf.tobytes()
    b64_out = base64.b64encode(jpeg_bytes).decode("ascii")
    return f"data:image/jpeg;base64,{b64_out}", len(jpeg_bytes)
