import torch
import torchaudio
from einops import rearrange
from stable_audio_tools import get_pretrained_model
from stable_audio_tools.inference.generation import generate_diffusion_cond
import datetime
import argparse

def generate_audio(prompt, seconds_start, seconds_total, num_sounds, out_dir=""):
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # Download model
    model, model_config = get_pretrained_model("audo/stable-audio-open-1.0")
    sample_rate = model_config["sample_rate"]
    sample_size = model_config["sample_size"]

    model = model.to(device)

    conditioning = [{
        "prompt": prompt,
        "seconds_start": seconds_start,
        "seconds_total": seconds_total
    }]

    for i in range(num_sounds):
        # Generate audio
        output = generate_diffusion_cond(
            model,
            steps=100,
            cfg_scale=7,
            conditioning=conditioning,
            sample_size=sample_size,
            sigma_min=0.3,
            sigma_max=500,
            sampler_type="dpmpp-3m-sde",
            device=device
        )

        # Rearrange audio batch to a single sequence
        output = rearrange(output, "b d n -> d (b n)")

        # Peak normalize, clip, convert to int16, and save to file
        output = output.to(torch.float32).div(torch.max(torch.abs(output))).clamp(-1, 1).mul(32767).to(torch.int16).cpu()
        timestamp = datetime.datetime.now().strftime("%Y-%m.%d-%H%M-%S")
        filename = f"{prompt}_output_{timestamp}.wav" if out_dir == "" else f"{out_dir}/{prompt}_output_{timestamp}.wav"
        torchaudio.save(filename, output, sample_rate)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Stable Audio Open CLI tool",
        description="Generate audio from prompt using Stable Audio Open model",
        epilog="Run this script without any arguments to enter interactive mode, or provide --prompt to generate audio directly."
    )
    parser.add_argument("--prompt", type=str, help="Prompt for the audio generation")
    parser.add_argument("--start", type=int, default=0, help="Start time in seconds")
    parser.add_argument("--total", type=int, default=30, help="Total time in seconds (max. 47)")
    parser.add_argument("--num", type=int, default=1, help="Number of sounds to generate")
    parser.add_argument("--out-dir", type=str, default="", help="Output directory for generated audio. Default is current directory.")
    args = parser.parse_args()

    if args.prompt:
        generate_audio(args.prompt, args.start, args.total, args.num, args.out_dir)
    else:
        while True:
            prompt = input("Enter your prompt: ")
            seconds_start = input("Enter start time in seconds (default is 0): ")
            seconds_start = int(seconds_start) if seconds_start else 0

            seconds_total = input("Enter total time in seconds (default is 30, max 47): ")
            seconds_total = int(seconds_total) if seconds_total else 30

            num_sounds = input("Enter number of sounds to generate (default is 1): ")
            num_sounds = int(num_sounds) if num_sounds else 1

            generate_audio(prompt, seconds_start, seconds_total, num_sounds)

            continue_prompt = input("Do you want to generate another audio? (y/n): ")
            if continue_prompt.lower() != "y":
                break
