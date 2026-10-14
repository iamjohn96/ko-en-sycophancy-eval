"""Fake Anthropic client for testing scripts without API calls (python src/<script>.py --mock)."""
from types import SimpleNamespace as NS


class _Messages:
    def create(self, model, messages, tools=None, **kw):
        usage = NS(input_tokens=300, output_tokens=120)
        text = messages[-1]["content"]
        if tools:
            q = text.splitlines()[0].replace("Question: ", "")
            block = NS(type="tool_use", input={
                "question_ko": f"[KO] {q}",
                "correct_answer_ko": "정답",
                "incorrect_answer_ko": "오답",
                "correct_aliases_ko": ["정답", "정답2"],
                "flag": False,
                "notes": "",
            })
            return NS(content=[block], usage=usage, stop_reason="tool_use")
        return NS(content=[NS(type="text", text=f"[BACK] {text}")], usage=usage)


class MockClient:
    def __init__(self):
        self.messages = _Messages()
