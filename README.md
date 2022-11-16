# Audio Visualizer

An audio-driven artwork visualizer. 

## Demonstration

Webapp available [here](http://15.223.5.40:8082/).

Recording of a live performance available [here](https://youtu.be/AnA1DCfEnog).


## Prompt Generator

Prompts can be generated from a concept tree. The format should follow the example available in [concepts.json](./prompts/concepts.json), concept -> subconcept -> list of words.

    {
        "themes": {
            "astronomy": [
                "selenology",
                "stargazing",
                ...
            ],
            "urban": [
                "city",
                "downtown",
                ...
            ],
            ...
        },
        "emotions": {
            ...
        },
        ...
    }   

To generate a random list of prompts run,

    cd prompts/
    python3 generator.py


The output should look like the example available in [prompts.json](./prompts/prompts.json).

    [
        {
            "uid": "89d36b2d-3390-4c62-a0f1-c6e32219ad78",
            "theme": "astronomy",
            "emotion": "happiness",
            "style": "cubism",
            "prompt": "cosmos universe innovative visionary recent, laughter, euphoria, jubilation, in the style of Piet Mondrian and Kazimir Malevich"
        },
        ...
    ]


## Artwork Generator

Artwork generation is done on servers equipped with a GPU. Central to this system is the Stable Diffusion model. Its weights can be downloaded from [huggingface](https://huggingface.co/runwayml/stable-diffusion-v1-5).

Here are the steps to setup a server. 

    # clone the repository of stable diffusion
    git clone https://github.com/runwayml/stable-diffusion.git
    cd stable-diffusion/

    # environment setup
    conda env create -f environment.yaml
    source ~/anaconda3/etc/profile.d/conda.sh
    conda activate ldm

    # create directory for weights
    mkdir -p models/ldm/stable-diffusion-v1/

    # copy weights to directory
    aws s3 cp s3://{PATH-TO-YOUR-MODEL}/v1-5-pruned-emaonly.ckpt ./models/ldm/stable-diffusion-v1/

    # symbolic link to the weights
    cd ./models/ldm/stable-diffusion-v1/
    ln -s v1-5-pruned-emaonly.ckpt model.ckpt
    cd ../../../

    # test the install
    python3 scripts/txt2img.py --prompt "a photograph of an astronaut riding a horse" --plms 
    

The model contains a NSFW filter that can be disabled as follows. Edit the script file, 

    nano scripts/txt2img.py

and make the following modification,

    #x_checked_image, has_nsfw_concept = check_safety(x_samples_ddim)
    x_checked_image = x_samples_ddim


In your home directory, create the directory where your generated artwork will be created. 

    mkdir ~/outputs/

Import the prompts.json file generated earlier to your home directory

Copy the content of the [artworks](./artworks/) folder on the server and update the [config.py](./artworks/config.py) file to match your environment. 

The helper scripts are described below. 

**generate.py** - takes as input an array of prompts and returns a number distinct artwork for each.

    [
        {
            "uid": "89d36b2d-3390-4c62-a0f1-c6e32219ad78",
            "prompt": "cosmos universe innovative visionary recent, laughter, euphoria, jubilation, in the style of Piet Mondrian and Kazimir Malevich"
        },
        {
            "uid": "b43fd141-ed54-4a96-8333-ce20e3e0260a",
            "prompt": "port town nominal vital essential, astonishment, consternation, curiosity, in the style of Bill Bollinger and Félix González-Torres"
        },
        ...
    ]

**gifyer.py** - combines the images of each prompt into a GIF. 

**copier.py** - copies the GIFs to an S3 bucket. 


## Artwork Visualizer

A webapp is used to visualize the generated artwork. Here are the steps to install it,

    # clone this repository on your personal computer
    git clone https://github.com/jeanromainroy/audio-visualizer.git
    cd audio-visualizer/

    # install dependencies
    npm i --force

    # build it
    npm run build

    # to test it
    npm start

Copy your prompts.json file to [public](./public/)

Copy all your generated GIFs to the [gifs](./public/gifs/) folder. 


## Benchmarking

We tested the model on two AWS instances – ml.p3.2xlarge and ml.g5.xlarge.

Generation of 1 artwork, 

 - Takes about 8 seconds
 - Costs ~0.01$
