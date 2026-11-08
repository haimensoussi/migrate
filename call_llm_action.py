from llm_client import DatabricksLLMClient

class CallLLMAction:
    def __init__(self, llm=None):
        self.llm = llm or DatabricksLLMClient()

    def execute(self, context):
        context.output = self.llm.generate(context.messages)
        return context.output
