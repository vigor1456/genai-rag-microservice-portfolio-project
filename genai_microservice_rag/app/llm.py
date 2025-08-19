from app.config import settings

class DummyLLM:
    def generate(self, prompt: str) -> str:
        return (
            "This is a demo response generated without external LLMs.\n\n"
            "It would normally synthesize an answer from retrieved sources.\n"
            "Prompt preview: " + prompt[:300] + ("..." if len(prompt) > 300 else "")
        )

def _openai_client():
    from openai import OpenAI
    return OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else OpenAI()

def _azure_client():
    from openai import AzureOpenAI
    return AzureOpenAI(
        api_key=settings.azure_openai_api_key,
        azure_endpoint=settings.azure_openai_endpoint,
        api_version="2024-05-01-preview",
    )

class LLM:
    def __init__(self):
        self.provider = settings.llm_provider.lower()

    def generate(self, prompt: str) -> str:
        if self.provider == "openai":
            client = _openai_client()
            model = settings.openai_model
            resp = client.chat.completions.create(
                model=model,
                messages=[{"role":"system","content":"Answer using provided context. Cite sources by filename."},
                          {"role":"user","content":prompt}],
                temperature=0.2,
            )
            return resp.choices[0].message.content
        elif self.provider == "azure":
            client = _azure_client()
            resp = client.chat.completions.create(
                model=settings.azure_openai_deployment,
                messages=[{"role":"system","content":"Answer using provided context. Cite sources by filename."},
                          {"role":"user","content":prompt}],
                temperature=0.2,
            )
            return resp.choices[0].message.content
        else:
            return DummyLLM().generate(prompt)
