# libs
import os
from glob import glob
from config import WORKDIR, S3_BUCKET

# grab all GIFs
filepaths = glob(f"{WORKDIR}*/*.gif")

# copy on a s3 bucket
for filepath in filepaths:
    os.system(f'aws s3 cp {filepath} {S3_BUCKET}')
