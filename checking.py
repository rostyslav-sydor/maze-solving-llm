from re import compile, findall
from maze_dataset import SolvedMaze
from maze_dataset.plotting import MazePlot
import matplotlib.pyplot as plt

from maze_dataset.tokenization import MazeTokenizer, TokenizationMode

better_method = True

maze = "plain4x4"
model = "gemini-token-eighty-shot"
ascii = False
model_solutions = f"dataset/{maze}/{model}"
basedir = f"dataset/{maze}"

regex = compile("<PATH_START>(?: ?\(\d,\d\) ?)+?<PATH_END>+?")

correct = 0

def parse_ascii(string: str):
    # 1 -> 0
    # 3 -> 1
    # 5 -> 2
    # 7 -> 3

    right_list = set([1,3,5,7])
    out_list = ["<PATH_START>"]
    tokens = [eval(token) for token in string.split()[1:-1]]
    for token in tokens:
        if(token[0] not in right_list or token[1] not in right_list):
            continue
    
        out_list.append(str((token[0]//2, token[1]//2)))
    
    out_list.append("<PATH_END>")
    return " ".join(out_list)

if better_method:
    for i in range(100):
        # print(i)

        with open(f"{basedir}/tokens/maze{i+1}.txt", "r") as f:
            s = f.read()

        with open(f"{model_solutions}/maze{i+1}.txt", "r", encoding='utf-8') as f:
            ss = findall(regex, f.read().replace("\n"," ").replace(")(", ") (").upper())

            if len(ss):
                if ascii:
                    ss = [parse_ascii(ss[0])]
                s += " " + ss[0]
            else :
                s += " <PATH_START> (0,0) (1,1) <PATH_END>"


        # print(s)
        # print(i)
        # print(s)
        representation: SolvedMaze = SolvedMaze.from_tokens(s, maze_tokenizer=MazeTokenizer(
                                                tokenization_mode=TokenizationMode.AOTP_UT_rasterized, max_grid_size=100,
                                                ))
        
        if (representation.is_valid_path(representation.solution)):
            # MazePlot(representation).plot()
            # plt.show()
            print(i)
            print(s)
            correct += 1

else:
    for i in range(100):
        print(i)

        with open(f"{basedir}/solutions/maze{i+1}.txt", "r") as f:
            s = f.read()

        with open(f"{model_solutions}/maze{i+1}.txt", "r", encoding='utf-8') as f:
            ss = findall(regex, f.read().replace("\n"," ").upper())
            if len(ss):
                ss = ss[0]
            else:
                ss = ""

        print(s)
        
        if (s == ss):
            correct += 1


print(correct)