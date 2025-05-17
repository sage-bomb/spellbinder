import os
import uuid
import datetime
from typing import List, Dict, Optional, Any

from openai import OpenAI
from jinja2 import Template

from util.db import TinyInterface
from llm.prompt_templates import PROMPT_TEMPLATES
from llm.model_resolver import ModelResolver  # 🔧 added


class PromptManager:
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gpt-3.5-turbo",
        temperature: float = 0.3,
        use_db: bool = True,
        db_path: str = "data/prompt_store.json"
    ):
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.model = model
        self.temperature = temperature
        self.use_db = use_db
        self.db = TinyInterface(db_path, "prompts") if use_db else None
        self.model_resolver = ModelResolver(api_key=api_key)  # 🔧 added

    def chat(
        self,
        user_message: str,
        system_message: str = "You are a helpful assistant.",
        history: Optional[List[Dict[str, str]]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        model: Optional[str] = None,
        cost_managment_loging: Optional[bool]=False
    ) -> str:
        messages = [{"role": "system", "content": system_message}]
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": user_message})

        # 🛡 Respect safety flag
        self.model_resolver.block_expensive = not (metadata or {}).get("allow_expensive", False)
        resolved_model = self.model_resolver.resolve(model or self.model)

        try:
            response = self.client.chat.completions.create(
                model=resolved_model,
                messages=messages,
                temperature=self.temperature
            )
            reply = response.choices[0].message.content.strip()

            usage = getattr(response, "usage", None)
            cost = None

            if usage:
                prompt_tokens = usage.prompt_tokens
                completion_tokens = usage.completion_tokens
                total_tokens = usage.total_tokens

                model_cost_per_1k = {
                    "gpt-3.5-turbo": 0.0015,
                    "gpt-3.5-turbo-16k": 0.003,
                    "gpt-4": 0.03,
                    "gpt-4-32k": 0.06,
                    "gpt-4o": 0.005
                }

                per_token_cost = model_cost_per_1k.get(resolved_model, 0.01)
                cost = (total_tokens / 1000) * per_token_cost
                if cost_managment_loging:
                    print(f"💬 Tokens used: prompt={prompt_tokens}, completion={completion_tokens}, total={total_tokens}")
                    print(f"💰 Estimated cost: ${cost:.4f}")

            if self.use_db:
                self._store_prompt(
                    prompt=user_message,
                    response=reply,
                    system=system_message,
                    model=resolved_model,
                    temperature=self.temperature,
                    history=history,
                    metadata=metadata,
                    messages=messages + [{"role": "assistant", "content": reply}],
                    usage=usage.to_dict() if usage else None,
                    estimated_cost=cost
                )

            return reply

        except Exception as e:
            print(f"❌ PromptManager error: {e}")
            return ""

    def run_template(
        self,
        name: str,
        variables: Dict[str, str],
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        if name not in PROMPT_TEMPLATES:
            raise ValueError(f"Prompt template '{name}' not found.")

        config = PROMPT_TEMPLATES[name]
        system = config["system"]
        raw_template = config["template"]
        persona = config.get("persona", "unknown")
        requested_model = config.get("model", self.model)

        # 🛡 safety again
        self.model_resolver.block_expensive = not (metadata or {}).get("allow_expensive", False)
        model = self.model_resolver.resolve(requested_model)

        rendered = Template(raw_template).render(**variables)

        response = self.chat(
            user_message=rendered,
            system_message=system,
            metadata={
                **(metadata or {}),
                "template": name,
                "variables": variables,
                "persona": persona,
                "tags": config.get("tags", []),
                "resolved_model": model
            },
            model=model  # 🚀 resolved model
        )
        return response

    def _store_prompt(
        self,
        prompt: str,
        response: str,
        system: str,
        model: str,
        temperature: float,
        history: Optional[List[Dict[str, str]]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        messages: Optional[List[Dict[str, str]]] = None,
        usage: Optional[Dict[str, Any]] = None,
        estimated_cost: Optional[float] = None
    ):
        entry = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "prompt": prompt,
            "response": response,
            "system": system,
            "model": model,
            "temperature": temperature,
            "messages": messages or []
        }

        if history:
            entry["history"] = history
        if metadata:
            entry["metadata"] = metadata
        if usage:
            entry["usage"] = usage
        if estimated_cost is not None:
            entry["estimated_cost"] = estimated_cost

        self.db.add(entry)
