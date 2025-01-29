import argparse
import logging
import os
import shutil
from pathlib import Path
from typing import Union

from dotenv import load_dotenv
from huggingface_hub import login, snapshot_download

load_dotenv()

logger = logging.getLogger(__name__)

def download_model_locally(
    model_name: str,
    local_model_path: Union[str, Path],
    replace_if_exists: bool = False,
) -> str:
    """
    Download a Hugging Face model locally.

    Args:
        model_name (str): Model name/ID from Hugging Face.
        local_model_path (Union[str, Path]): Local path to store the model.
        replace_if_exists (bool): If True, re-download the model if it already exists.

    Returns:
        str: The local path where the model is stored.
    """
    # Handle Hugging Face login
    hf_token = os.getenv("HF_TOKEN")
    if hf_token:
        hf_token = hf_token.strip()
        login(token=hf_token, add_to_git_credential=True)
        logger.info("Successfully logged in to Hugging Face.")
    else:
        raise EnvironmentError(
            "HF_TOKEN is not defined. Please set the Hugging Face token as an environment variable."
        )

    converted_model_path = os.path.join(local_model_path, model_name.replace("/", "-"))

    if Path(converted_model_path).exists() and not replace_if_exists:
        logger.info(f"Path '{converted_model_path}' already exists. Skipping download.")
    else:
        # If it exists and we want to replace it, remove it first
        if Path(converted_model_path).exists():
            shutil.rmtree(converted_model_path)
            logger.info(f"Removed existing directory at {converted_model_path}.")

        snapshot_download(repo_id=model_name, local_dir=converted_model_path)
        logger.info(f"Model '{model_name}' downloaded to {converted_model_path}")

    return converted_model_path


# Example usage
# export HF_TOKEN="xxx"
# export MODEL="microsoft/phi-4"
# python download.py --local_model_path="${HOME}/models"
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--local_model_path",
        default="./models",
        help="Local directory path to store the model."
    )
    args = parser.parse_args()

    downloaded_path = download_model_locally(
        model_name=os.getenv("MODEL"),
        local_model_path=args.local_model_path,
        replace_if_exists=False,
    )
    logger.info(f"Model is ready at: {downloaded_path}")
