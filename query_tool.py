from gpt_index import GPTSimpleVectorIndex
from langchain.agents import Tool
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
        pass
    
    def get_tool(self):
        return Tool(
            name='QueryDocsTool',
            func=self.query_docs,
            description=(
                f'useful for searching through documentation for the {self.package_name} library. ' +
                'accepts a question as input and returns a list of relevant documents'
            )
        )