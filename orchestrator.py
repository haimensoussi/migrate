import json
from dataclasses import dataclass
from pathlib import Path
from call_llm_action import CallLLMAction

@dataclass
class ExecutionContext:
    messages: list[dict]
    output: str | None = None

class HorizonOrchestrator:
    def __init__(self, action=None):
        config = json.loads((Path(__file__).parent / "assistant.json").read_text(encoding="utf-8"))
        self.prompt = config["system_prompt"]
        self.action = action or CallLLMAction()

    def run(self, history):
        safe_history = [
            {"role": m["role"], "content": m["content"]}
            for m in history if m.get("role") in {"user", "assistant"}
            and isinstance(m.get("content"), str)
        ]
        if not safe_history or safe_history[-1]["role"] != "user":
            raise ValueError("La dernière entrée doit être une question utilisateur")
        context = ExecutionContext(messages=[{"role": "system", "content": self.prompt}] + safe_history[-20:])
        return self.action.execute(context)
