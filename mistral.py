from openai import OpenAI

client = OpenAI(
        api_key="insert your API Key here",
        base_url="https://api.deepinfra.com/v1/openai")
from prompting import *
from os import mkdir, path
from links import links_plain_5x5, links_plain_4x4

maze_struct = "plain4x4"
base_dir = f"dataset/{maze_struct}"
current_prompt = ASCIIZeroShotPrompt()
direct = f"mixtral-{current_prompt.kind}"

if not path.exists(f"{base_dir}/{direct}"):
  mkdir(f"{base_dir}/{direct}")

for i in range(100):
  tokens = ""
  with open(f"{base_dir}/{current_prompt.dir_name}/maze{i+1}.txt") as f:
    tokens = f.read()

  print(i)
  if i == 0:
    print(current_prompt.get_prompt(tokens))

  response = client.chat.completions.create(
    model="HuggingFaceH4/zephyr-orpo-141b-A35b-v0.1",
    messages=[{"role": "user", "content": current_prompt.get_prompt(tokens)}],
  )

  with open(f"{base_dir}/{direct}/maze{i+1}.txt", "w+", encoding='utf-8') as file:
    file.write(response.choices[0].message.content)

