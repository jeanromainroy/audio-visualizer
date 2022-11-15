# libs
import os
from glob import glob
from PIL import Image
from config import WORKDIR, STEP_TIME_MS


# grab all image paths
imagepaths = glob(f"{WORKDIR}*/samples/*.png")

# select unique directories
dirpaths = list(set([imagepath.split('/samples')[0] for imagepath in imagepaths]))

# uids
uids = [dirpath.split('/')[-1] for dirpath in dirpaths]

# go through
for uid in uids:
    
    # filepaths
    fp_in = f"{WORKDIR}{uid}/samples/*.png"
    fp_out = f"{WORKDIR}{uid}/{uid}.gif"
    
    # load images
    paths = glob(fp_in)
    if len(paths) == 0: continue
    
    # check if was already done
    if os.path.exists(fp_out): continue    
    
    # create gifs
    imgs = (Image.open(f) for f in sorted(paths))
    img = next(imgs)  # extract first image from iterator
    img.save(fp=fp_out, format='GIF', append_images=imgs, save_all=True, duration=STEP_TIME_MS, loop=0)

    # log
    print(f'GIF ready - {fp_out}')
