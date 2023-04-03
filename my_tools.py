from gpt_index import GPTSimpleVectorIndex
from langchain.agents import Tool
from langchain.utilities import PythonREPL
import openai
import os

from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

class QueryTool(object):
    def __init__(self, index_path: str, package_name: str):
        self.index = GPTSimpleVectorIndex.load_from_disk(index_path)
        self.package_name = package_name
    
    def query_docs(self, query: str) -> list:
        context = []
        query = self.index.query(query)
        for node in query.source_nodes:
            context.append(f'Context {node.doc_id}: {node.source_text}')
        return context
    
    def get_tool(self):
        return Tool(
            name='QueryDocsTool',
            func=self.query_docs,
            description=(
                f'useful for searching through documentation for the {self.package_name} library. ' +
                'accepts a question as input and returns a list of relevant documents'
            )
        )

class PythonTool(object):
    def __init__(self):
        self.python_repl = PythonREPL()
    
    def get_tool(self):
        return Tool(
            "PythonREPL",
            PythonREPL().run,
            """A Python shell. Use this to execute python commands. Input should be a valid python command.
            If you expect output it should be printed out.
            Code should be wrapped in a try/catch block so that errors can be printed.""",
        )