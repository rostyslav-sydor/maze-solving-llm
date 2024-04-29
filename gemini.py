import vertexai
from time import sleep
from vertexai.generative_models import GenerativeModel, Part

# Initialize Vertex AI
vertexai.init(project="symmetric-fin-305313", location="europe-central2")
# Load the model
multimodal_model = GenerativeModel(model_name="gemini-1.0-pro-vision-001")

from prompting import *
from os import mkdir, path
from links import links_plain_5x5, links_plain_4x4

maze_struct = "plain4x4"
base_dir = f"dataset/{maze_struct}"
current_prompt = TokenEightyShotPrompt()
direct = f"gemini-{current_prompt.kind}"

if not path.exists(f"{base_dir}/{direct}"):
  mkdir(f"{base_dir}/{direct}")

for i in range(100):
  if i % 10 == 9:
    sleep(60)
  tokens = ""
  with open(f"{base_dir}/{current_prompt.dir_name}/maze{i+1}.txt") as f:
    tokens = f.read() 
  
  if i == 0:
    print(current_prompt.get_prompt(tokens))
  
  response = multimodal_model.generate_content(
    [
        # # Add an example image
        # Part.from_uri(
        #     links_plain_4x4[i], mime_type="image/png"
        # ),
        # Add an example query
        current_prompt.get_prompt(tokens)
    ]
)

  with open(f"{base_dir}/{direct}/maze{i+1}.txt", "w+") as file:
    file.write(response.candidates[0].content.text)
