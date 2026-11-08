import os

class DatabricksLLMClient:
    def __init__(self, client=None, endpoint=None):
        if client is None:
            from databricks.sdk import WorkspaceClient
            client = WorkspaceClient()
        self.client = client
        self.endpoint = endpoint or os.environ["LLM_ENDPOINT"]

    def generate(self, messages):
        response = self.client.serving_endpoints.query(
            name=self.endpoint,
            messages=messages,
        )
        choices = getattr(response, "choices", None)
        if not choices:
            raise RuntimeError("L'endpoint n'a renvoyé aucun choix")
        content = choices[0].message.content
        if not isinstance(content, str):
            raise RuntimeError("Format de réponse LLM non pris en charge")
        return content
