CLI-tool for [Stable Audio Open](https://stability.ai/news/introducing-stable-audio-open) 🎵🎵🎵

## Features

- Interactive prompt shell
- Batching
- Python CLI with arguments
- Output to custom folder

## Setup

This has been tested under Python **3.8.10**, as specified in the [Stable Audio Open Repo](https://github.com/Stability-AI/stable-audio-tools) and Conda.

Once you are in your Python 3.8.10 environment:

- [Install your version of PyTorch (>2.0)](https://pytorch.org/get-started/locally/)
- `pip install stable-audio-tools`

>It might take a long time to resolve dependencies, be patient!

Then, just run `python stable-audio-cli.py` to launch the interactive prompt shell, or provide arguments as shown below.

## Help

```
usage: Stable Audio Open CLI tool [-h] [--prompt PROMPT] [--start START] [--total TOTAL] [--num NUM] [--out-dir OUT_DIR]

Generate audio from prompt using Stable Audio Open model

optional arguments:
  -h, --help         show this help message and exit
  --prompt PROMPT    Prompt for the audio generation
  --start START      Start time in seconds
  --total TOTAL      Total time in seconds (max. 47)
  --num NUM          Number of sounds to generate
  --out-dir OUT_DIR  Output directory for generated audio. Default is current directory.

Run this script without any arguments to enter interactive mode, or provide, at minimum, --prompt to generate audio directly.
```

Example: `python stable-audio-cli.py --prompt "lofi synth tune" --out-dir "/home/cat" --num 2`

Let me know if you have any feedback or suggestions!
