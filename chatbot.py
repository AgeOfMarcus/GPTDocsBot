from langchain.agents import initialize_agent
#from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.utilities import PythonREPL
from argparse import ArgumentParser
import pickle
import os
# local imports
from prompt import DocsBot_PREFIX, DocsBot_FORMAT_INSTRUCTIONS, DocsBot_SUFFIX
from my_tools import QueryTool, PythonTool

def save_chat(memory: ConversationBufferMemory, filename: str):
    with open(filename, 'wb') as f:
        pickle.dump(memory, f)
    
def load_chat(filename: str) -> ConversationBufferMemory:
    with open(filename, 'rb') as f:
        return pickle.load(f)

def parse_args():
    p = ArgumentParser()
    p.add_argument('-i', '--index', type=str, required=True, help='path to the documentation index built with build_index.py')
    p.add_argument('-n', '--name', type=str, required=True, help='name of the package to query (for prompt, e.g. flask)')
    p.add_argument('-c', '--chat_history', type=str, default='hist.pkl', help='chat history file (default: hist.pkl)')
    
    args = p.parse_args()
    if not os.path.exists(args.index):
        p.error(f'index path {args.index} does not exist')
    if not os.path.exists(args.chat_history):
        save_chat(ConversationBufferMemory(), args.chat_history)
    return args

class Chatbot(object):
    def __init__(self, index_file: str, name: str, hist_file: str):
        self.llm = ChatOpenAI(model_name='gpt-4', temperature=0)
        self.query_tool = QueryTool(index_file, name)
        self.python_tool = PythonTool()
        self.tools = [self.python_tool.get_tool(), self.query_tool.get_tool()]
        self.memory = load_chat(hist_file)
        self._hist_file = hist_file
        self.agent = initialize_agent(
            self.tools,
            self.llm,
            memory=self.memory,
            agent='chat-conversational-react-description',
            verbose=True,
            agent_kwargs={
                'prefix': DocsBot_PREFIX,
                'format_instructions': DocsBot_FORMAT_INSTRUCTIONS,
                'suffix': DocsBot_SUFFIX
            }
        )

def main():
    args = parse_args()
    bot = Chatbot(args.index, args.name, args.chat_history)
    print('Entering chat. Use Ctrl+C to save and/or exit.')
    while True:
        try:
            q = input('User > ')
            bot.agent({'input': q, 'chat_history': bot.memory.chat_memory.messages})
        except KeyboardInterrupt:
            save_chat(bot.memory, bot._hist_file)
            if input('exit? (y/n) > ').lower() == 'y':
                break

if __name__ == '__main__':
    main()