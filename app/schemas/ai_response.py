from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import date
from decimal import Decimal


class IssuerSchema(BaseModel):
    name: str = Field(..., description="Razón social del emisor")
    ruc: str = Field(..., description="RUC del emisor")
    address: str = Field(..., description="Dirección del emisor")


class ReceiverSchema(BaseModel):
    name: str = Field(..., description="Razón social del receptor")
    ruc: str = Field(..., description="RUC del receptor")
    address: str = Field(..., description="Dirección del receptor")
    client_address: str = Field(..., description="Dirección del cliente")


class InvoiceInfoSchema(BaseModel):
    issue_date: date = Field(..., description="Fecha de emisión en formato YYYY-MM-DD")
    series_number: str = Field(..., description="Serie y número de factura")
    payment_method: str = Field(..., description="Forma de pago")
    currency: str = Field(..., description="Tipo de moneda según la ISO 4217")
    purchase_order: str = Field(..., description="Orden de compra")


class ItemSchema(BaseModel):
    quantity: float = Field(..., description="Cantidad")
    unit_measure: str = Field(..., description="Unidad de medida")
    description: str = Field(..., description="Descripción del ítem")
    unit_value: Decimal = Field(..., description="Valor unitario (monto)")
    icbper: Decimal = Field(..., description="Impuesto ICBPER (monto)")


class DetractionSchema(BaseModel):
    legend: str = Field(..., description="Leyenda de detracción")
    service_type: str = Field(..., description="Tipo de bien o servicio")
    payment_method: str = Field(..., description="Medio de pago")
    bank_account: str = Field(..., description="Número de cuenta bancaria")
    detraction_percentage: Decimal = Field(..., description="Porcentaje de detracción")
    detraction_amount: Decimal = Field(..., description="Monto de detracción")


class InstallmentSchema(BaseModel):
    installment_number: int = Field(..., description="Número de cuota")
    due_date: Optional[date] = Field(None, description="Fecha de vencimiento en formato YYYY-MM-DD")
    amount: Decimal = Field(..., description="Monto de la cuota")


class CreditSchema(BaseModel):
    pending_amount: Decimal = Field(..., description="Monto neto pendiente de pago")
    total_installments: int = Field(..., description="Total de cuotas")
    installments: List[InstallmentSchema] = Field(..., description="Lista de cuotas")


class TotalsSchema(BaseModel):
    total_amount: Decimal = Field(..., description="Monto total (valor numérico)")
    pending_amount: Decimal = Field(..., description="Monto pendiente de pago")
    free_operations: Decimal = Field(..., description="Valor de venta de operaciones gratuitas")


class InvoiceDataSchema(BaseModel):
    """Esquema principal que contiene todos los datos de la factura"""
    issuer: IssuerSchema
    receiver: ReceiverSchema
    invoice_info: InvoiceInfoSchema
    items: List[ItemSchema]
    detraction: DetractionSchema
    credit: CreditSchema
    totals: TotalsSchema


class InvoiceValidationResponse(BaseModel):
    """Schema para la respuesta completa de validación de una factura electrónica"""
    is_valid: bool = Field(..., description="Si el documento es una factura electrónica válida")
    requires_human_review: bool = Field(default=False, description="Indica si el documento requiere revisión humana")
    validation_message: str = Field(..., description="Mensaje explicando la validación")
    confidence_score: float = Field(default=0.0, ge=0.0, le=1.0, description="Score de confianza 0.0-1.0")
    data: InvoiceDataSchema = Field(..., description="Datos extraídos de una factura electrónica peruana")
    missing_fields: List[str] = Field(default_factory=list, description="Campos críticos faltantes")
