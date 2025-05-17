from openai import OpenAI
import os
import re

class ModelResolver:
    def __init__(self, api_key: str = None, allowed_prefixes=None, default="gpt-4"):
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.default = default
        self.allowed_prefixes = allowed_prefixes or ["gpt-4o", "gpt-4", "gpt-3.5"]
        self.available_models = self._fetch_models()

        # 🛡️ Safety feature
        self.block_expensive = True
        self.expensive_prefixes = ["gpt-4", "gpt-4o"]

    def _fetch_models(self):
        try:
            models = self.client.models.list()
            return sorted([m.id for m in models.data])
        except Exception as e:
            print(f"⚠️ ModelResolver failed to fetch models: {e}")
            return []

    def resolve(self, requested: str = None) -> str:
        if requested is None:
            requested = self.default

        # ⛔ Block direct request of expensive model?
        if self.block_expensive and any(requested.startswith(p) for p in self.expensive_prefixes):
            print(f"🛑 Requested model '{requested}' is blocked. Falling back.")

        # Handle alias formats like "gpt-4:latest", "gpt-4:preview"
        if ":" in requested:
            base, tag = requested.split(":", 1)
            candidates = [m for m in self.available_models if m.startswith(base)]
            if self.block_expensive:
                candidates = [m for m in candidates if not any(m.startswith(p) for p in self.expensive_prefixes)]

            if tag == "latest":
                if base == "gpt-4":
                    o_match = next((m for m in candidates if "gpt-4o" in m), None)
                    if o_match:
                        return o_match
                return candidates[-1] if candidates else self.default
            elif tag == "preview":
                preview_match = next((m for m in reversed(candidates) if "preview" in m), None)
                if preview_match:
                    return preview_match
            elif tag == "stable":
                stable_match = next((m for m in candidates if re.match(rf"{base}-turbo", m)), None)
                if stable_match:
                    return stable_match

        # Direct match (but skip if blocked)
        if requested in self.available_models and not (
            self.block_expensive and any(requested.startswith(p) for p in self.expensive_prefixes)
        ):
            return requested

        # Prefix fallback
        for prefix in [requested] + self.allowed_prefixes:
            for m in self.available_models:
                if m.startswith(prefix):
                    if self.block_expensive and any(m.startswith(p) for p in self.expensive_prefixes):
                        continue
                    return m

        # Final fallback
        print(f"⚠️ All model options blocked or unavailable. Using default: {self.default}")
        return self.default

    def list_models(self):
        return self.available_models
