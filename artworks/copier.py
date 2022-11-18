# libs
import os
from glob import glob
from config import WORKDIR, S3_BUCKET

# grab all images
filepaths = glob(f"{WORKDIR}*/*/*.jpg")

# copy on a s3 bucket
for filepath in filepaths:
    os.system(f'aws s3 cp {filepath} {S3_BUCKET}')
