# libs
import os
import json
from config import WORKDIR, SDDIR, NBR_OF_ARTWORKS_PER_PROMPT

# config
SEED = 42
PROMPT_INDEX_START = 0
PROMPT_INDEX_END = None


# load prompts
with open('./prompts.json') as f:
    dataframe = json.load(f)


# helper function to generate generate command
def build_cmd(prompt, outdir):
    return f'cd {SDDIR} && python3 scripts/txt2img.py --prompt "{prompt}" --outdir "{outdir}" --seed {SEED} --n_iter {round(NBR_OF_ARTWORKS_PER_PROMPT/3.0)} --skip_grid --plms'

    
# go through
for i, datum in enumerate(dataframe):

    # skip if outside of index window
    if PROMPT_INDEX_START is not None and i < PROMPT_INDEX_START: continue
    if PROMPT_INDEX_END is not None and i > PROMPT_INDEX_END: continue
    
    # destructure
    uid = datum['uid']
    prompt = datum['prompt']

    # dirpath
    dirpath = f"{WORKDIR}{uid}"
    if not os.path.exists(dirpath): os.system(f'mkdir {dirpath}')
    
    # build cmd
    cmd = build_cmd(prompt, dirpath)

    # run
    os.system(cmd)
