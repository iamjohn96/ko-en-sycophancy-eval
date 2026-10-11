"""D0 smoke test: one call to Haiku 5.5. Costs well under $0.001."""
from dotenv import load_dotenv
import anthropic

load_dotenv(override=True)  # .env wins over any ANTHROPIC_API_KEY already in the shell
client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from .env

msg = client.messages.create(
    model="claude-haiku-5-5",
    max_tokens=50,
    messages=[{"role": "user", "content": "hello"}],
)
print(msg.content[0].text)
print(msg.usage)
