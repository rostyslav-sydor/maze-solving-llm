from openai import OpenAI
from prompting import *
from os import mkdir, path
from links import links_plain_5x5, links_plain_4x4


maze_struct = "plain4x4"
base_dir = f"dataset/{maze_struct}"
current_prompt = ASCIIZeroShotPrompt()
direct = f"gpt3.5-{current_prompt.kind}"

if not path.exists(f"{base_dir}/{direct}"):
  mkdir(f"{base_dir}/{direct}")

client = OpenAI(api_key="insert your API Key here")

for i in range(100):
  tokens = ""
  with open(f"{base_dir}/{current_prompt.dir_name}/maze{i+1}.txt") as f:
    tokens = f.read()
  
  if i == 0:
    print(current_prompt.get_prompt(tokens))
  
  completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {
        "role": "user",
        "content": [
          {"type": "text", "text": current_prompt.get_prompt(tokens)},
          # {
          #   "type": "image_url",
          #   "image_url": {
          #     "url": links_plain_4x4[i],
          #     "detail": "low"
          #   },
          # },
        ],
      }
    ],
  )
  with open(f"{base_dir}/{direct}/maze{i+1}.txt", "w+", encoding='utf-8') as file:
    file.write(completion.choices[0].message.content)

#   print(completion.choices[0].message.content)


# for i in range(100):
#   tokens = ""
#   with open(f"{base_dir}/tokens/maze{i+1}.txt") as f:
#     tokens = f.read()

#   print(i)
#   print(current_prompt.get_prompt(tokens))
#   # response = client.chat.completions.create(
#   #   model="gpt-4-turbo",
#   #   messages=[{"role": "user", "content": "Hello"}],
#   # )
#   # print(response.choices[0].message.content)

#   completion = client.chat.completions.create(
#     model="gpt-3.5-turbo",
#     messages=[
#       {
#         "role": "user",
#         "content": [
#           {"type": "text", "text": current_prompt.get_prompt(tokens)}
#         ],
#       }
#     ],
#   )
#   print(len(completion.choices[0].message.content))
#   with open(f"{base_dir}/{direct}/maze{i+1}.txt", "w+", encoding='utf-8') as file:
#     file.write(completion.choices[0].message.content)

  # print(completion.choices[0].message.content)

