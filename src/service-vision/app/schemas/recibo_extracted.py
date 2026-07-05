from pydantic import BaseModel, Field


class ReciboItem(BaseModel):
    descripcion: str
    cantidad: str | None = Field(default=None)
    precio_unitario: str | None = Field(default=None)
    importe: str | None = Field(default=None)


class ReciboExtracted(BaseModel):
    tipo_comprobante: str | None = Field(default=None)
    numero_comprobante: str | None = Field(default=None)
    fecha_emision: str | None = Field(default=None)
    emisor_razon_social: str | None = Field(default=None)
    emisor_ruc: str | None = Field(default=None)
    cliente_nombre: str | None = Field(default=None)
    moneda: str | None = Field(default=None)
    subtotal: str | None = Field(default=None)
    igv: str | None = Field(default=None)
    total: str | None = Field(default=None)
    items: list[ReciboItem] | None = Field(default=None)
    metodo_pago: str | None = Field(default=None)
    observaciones: str | None = Field(default=None)
