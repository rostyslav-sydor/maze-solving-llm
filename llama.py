from llama_index.llms.llama_api import LlamaAPI

api_key = "insert your API Key here"

llm = LlamaAPI(api_key=api_key)

from prompting import *
from os import mkdir, path
from links import links_plain_5x5, links_plain_4x4
from time import sleep

maze_struct = "plain4x4"
base_dir = f"dataset/{maze_struct}"
current_prompt = TokenFewShotPrompt()
direct = f"llama-{current_prompt.kind}"

if not path.exists(f"{base_dir}/{direct}"):
  mkdir(f"{base_dir}/{direct}")

for i in range(100):
  if i % 10 == 9:
    sleep(10)
  tokens = ""
  with open(f"{base_dir}/{current_prompt.dir_name}/maze{i+1}.txt") as f:
    tokens = f.read()
  
  if i == 0:
    print(current_prompt.get_prompt(tokens))
  
  resp = llm.complete(current_prompt.get_prompt(tokens))

  with open(f"{base_dir}/{direct}/maze{i+1}.txt", "w+") as file:
    file.write(resp.text)
