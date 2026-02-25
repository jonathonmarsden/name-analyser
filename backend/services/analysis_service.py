"""LLM-backed analysis service with strict schema validation and retries."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple

import logging
from openai import AsyncOpenAI
logger = logging.getLogger(__name__)

from .language_detector import LanguageDetector


@dataclass
class AnalysisOutput:
    name_with_diacritics: str
    inferred_language: str
    ipa: str
    macquarie: str
    guidance: str
    confidence: float
    ambiguity: Optional[dict]
    cultural_notes: str
    quality: str
    source: str


LLM_SCHEMA: Dict[str, Any] = {
    "name": "NamePronunciation",
    "schema": {
        "type": "object",
        "properties": {
            "language": {"type": "string"},
            "ipa": {"type": "string"},
            "macquarie": {"type": "string"},
            "pronunciation_guidance": {"type": "string"},
            "confidence": {"type": "number"},
            "ambiguity": {"type": ["object", "null"]},
            "cultural_notes": {"type": "string"}
        },
        "required": [
            "language",
            "ipa",
            "macquarie",
            "pronunciation_guidance",
            "confidence",
            "ambiguity",
            "cultural_notes"
        ],
        "additionalProperties": False
    },
    "strict": True
}


class AnalysisService:
    """Primary analysis pipeline using GPT-4.1 with bounded retries."""

    def __init__(self, language_detector: LanguageDetector) -> None:
        self.language_detector = language_detector
        self.primary_model = os.getenv("PRIMARY_LLM_MODEL", "gpt-4.1")
        self.secondary_model = os.getenv("SECONDARY_LLM_MODEL", "gpt-4.1-mini")
        self.timeout_seconds = float(os.getenv("LLM_TIMEOUT_SECONDS", "4"))
        self.max_retries = int(os.getenv("LLM_RETRIES", "1"))
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = AsyncOpenAI(api_key=api_key) if api_key else None

    async def analyse(self, name: str) -> AnalysisOutput:
        language_hint, script_conf = self.language_detector.detect(name)

        if not self.client:
            return self._fallback_output(name, language_hint, script_conf, "OPENAI_API_KEY not configured")

        models = [self.primary_model, self.secondary_model]
        for model in [m for m in models if m]:
            for attempt in range(self.max_retries + 1):
                result = await self._call_llm(model, name, language_hint)
                if result:
                    output = self._normalize_output(name, language_hint, result)
                    if self._quality_gate(output):
                        output.quality = "high"
                        output.source = "llm-primary" if model == self.primary_model else "llm-secondary"
                        return output
                logger.warning("LLM output failed quality gate for %s (attempt %s)", model, attempt + 1)

        return self._fallback_output(name, language_hint, script_conf, "Model output invalid after retries")

    async def _call_llm(self, model: str, name: str, language_hint: str) -> Optional[Dict[str, Any]]:
        system_prompt = (
            "You are a professional linguist. Return valid JSON only, matching the schema. "
            "No markdown, no extra text."
        )
        user_prompt = (
            f"Name: {name}\n"
            f"Script hint: {language_hint}\n\n"
            "Return JSON with language, ipa, macquarie, pronunciation_guidance, confidence, ambiguity, cultural_notes."
        )

        try:
            response = await self.client.responses.create(
                model=model,
                input=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={
                    "type": "json_schema",
                    "json_schema": LLM_SCHEMA
                },
                temperature=0.2,
                max_output_tokens=450,
                timeout=self.timeout_seconds
            )

            text = getattr(response, "output_text", None)
            if not text and getattr(response, "output", None):
                try:
                    text = response.output[0].content[0].text
                except Exception:
                    text = None
            if not text:
                return None

            payload = json.loads(text)
            return payload
        except Exception as exc:
            logger.warning("LLM call failed for %s: %s", model, exc)
            return None

    def _normalize_output(self, name: str, language_hint: str, payload: Dict[str, Any]) -> AnalysisOutput:
        language = str(payload.get("language") or language_hint).strip()
        ipa = str(payload.get("ipa") or "").strip()
        macquarie = str(payload.get("macquarie") or "").strip()
        guidance = str(payload.get("pronunciation_guidance") or "").strip()
        confidence = payload.get("confidence")
        try:
            confidence_val = float(confidence)
        except Exception:
            confidence_val = 0.6
        confidence_val = min(max(confidence_val, 0.0), 1.0)

        ambiguity = payload.get("ambiguity")
        cultural_notes = str(payload.get("cultural_notes") or "").strip()

        return AnalysisOutput(
            name_with_diacritics=name,
            inferred_language=language,
            ipa=ipa,
            macquarie=macquarie,
            guidance=guidance,
            confidence=confidence_val,
            ambiguity=ambiguity,
            cultural_notes=cultural_notes,
            quality="medium",
            source="llm"
        )

    def _quality_gate(self, output: AnalysisOutput) -> bool:
        return bool(output.ipa and output.macquarie and output.guidance)

    def _fallback_output(
        self,
        name: str,
        language_hint: str,
        script_conf: float,
        reason: str
    ) -> AnalysisOutput:
        simplified = "-".join(part for part in name.split() if part).lower()
        ipa = f"/{simplified}/" if simplified else "/na/"
        return AnalysisOutput(
            name_with_diacritics=name,
            inferred_language=language_hint or "Unknown",
            ipa=ipa,
            macquarie=name,
            guidance="Pronounce slowly and confirm preferred pronunciation with the person.",
            confidence=min(script_conf, 0.5),
            ambiguity=None,
            cultural_notes=f"Fallback output used: {reason}.",
            quality="fallback",
            source="heuristic"
        )
