from pathlib import Path
from typing import Any

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer


EMOTIONS = [
    "Anticipation",
    "Surprise",
    "Anger",
    "Disgust",
    "Trust",
    "Sadness",
    "Fear",
    "Joy",
]

RISK_EMOTIONS = {"Sadness", "Fear", "Anger", "Disgust"}


class EmotionService:
    def __init__(
        self,
        model_dir: str,
        model_prefix: str = "bert_",
        tokenizer_name: str = "bert-base-multilingual-cased",
        threshold: float = 0.50,
        max_length: int = 256,
    ) -> None:
        self.model_dir = Path(model_dir)
        self.model_prefix = model_prefix
        self.tokenizer_name = tokenizer_name
        self.threshold = threshold
        self.max_length = max_length
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.models: dict[str, Any] = {}
        self.tokenizers: dict[str, Any] = {}

        self._load_models()

    def _load_models(self) -> None:
        if not self.model_dir.exists():
            raise RuntimeError(f"No existe la carpeta de modelos: {self.model_dir}")

        base_tokenizer = AutoTokenizer.from_pretrained(self.tokenizer_name)

        for emotion in EMOTIONS:
            folder = self.model_dir / f"{self.model_prefix}{emotion}"

            if not folder.exists():
                print(f"⚠️ No existe modelo para {emotion}: {folder}")
                continue

            model = AutoModelForSequenceClassification.from_pretrained(str(folder))
            model.to(self.device)
            model.eval()

            self.models[emotion] = model
            self.tokenizers[emotion] = base_tokenizer

            print(f"✅ Modelo emocional cargado: {emotion}")

        if not self.models:
            raise RuntimeError(f"No se cargó ningún modelo desde {self.model_dir}")

    def analyze(self, text: str, threshold: float | None = None) -> dict[str, Any]:
        clean_text = text.strip()

        if not clean_text:
            raise ValueError("El texto no puede estar vacío.")

        used_threshold = self.threshold if threshold is None else threshold
        results: list[dict[str, Any]] = []

        for emotion, model in self.models.items():
            tokenizer = self.tokenizers[emotion]

            inputs = tokenizer(
                clean_text,
                return_tensors="pt",
                truncation=True,
                padding=True,
                max_length=self.max_length,
            )

            inputs = {key: value.to(self.device) for key, value in inputs.items()}

            with torch.no_grad():
                logits = model(**inputs).logits

                if logits.shape[-1] == 1:
                    probability = torch.sigmoid(logits[0][0]).item()
                else:
                    probability = torch.softmax(logits, dim=-1)[0][1].item()

            results.append(
                {
                    "emotion": emotion,
                    "probability": round(float(probability), 4),
                    "percent": round(float(probability) * 100, 2),
                    "present": bool(probability >= used_threshold),
                }
            )

        results.sort(key=lambda item: item["probability"], reverse=True)

        risk_score = 0.0
        for item in results:
            if item["emotion"] in RISK_EMOTIONS:
                risk_score = max(risk_score, item["probability"])

        alert_flag = risk_score >= used_threshold
        top = results[0] if results else None

        return {
            "text": clean_text,
            "threshold": used_threshold,
            "loaded_models": len(self.models),
            "top_emotion": top["emotion"] if top else None,
            "top_probability": top["probability"] if top else None,
            "risk_score": round(risk_score, 4),
            "alert_flag": bool(alert_flag),
            "sentiment_label": "alerta" if alert_flag else "sin_alerta",
            "emotions": results,
        }