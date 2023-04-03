from gpt_index import GPTSimpleVectorIndex, SimpleDirectoryReader
from argparse import ArgumentParser
import openai
import os

from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

def parse_args():
    p = ArgumentParser()
    p.add_argument('-d', '--directory', help='The directory containing docs to train', required=True)
    p.add_argument('-o', '--output', help='The output file to write the index to', required=True)
    args = p.parse_args()
    if not os.path.exists(args.directory):
        p.error(f'Directory {args.directory} does not exist')
    return args

def main():
    args = parse_args()
    print('Loading docs...')
    docs = SimpleDirectoryReader(args.directory).load_data()
    print('Building index...')
    index = GPTSimpleVectorIndex.from_documents(docs)
    index.save_to_disk(args.output)
    print(f'Index saved to {args.output}')

if __name__ == '__main__':
    main()