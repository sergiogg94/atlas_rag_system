import argparse
import requests
from pathlib import Path


def upload_file(file_path: Path, url: str, timeout: int):
    try:
        with open(file_path, "rb") as f:
            response = requests.post(
                url, files={"file": (file_path.name, f)}, timeout=timeout
            )

        if response.status_code == 200:
            print(f"[OK] {file_path.name}")
        else:
            print(f"[ERROR {response.status_code}] {file_path.name} -> {response.text}")

    except Exception as e:
        print(f"[EXCEPTION] {file_path.name} -> {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Upload multiple files to the RAG system via the /upload endpoint"
    )
    parser.add_argument("--path", help="Path to the folder containing files to upload")
    parser.add_argument("--url", help="URL of the /upload endpoint")
    parser.add_argument(
        "--timeout", type=int, default=30, help="Timeout for the request (in seconds)"
    )

    args = parser.parse_args()

    folder = Path(args.path)
    url = args.url
    timeout = args.timeout

    for file_path in folder.glob("*"):
        if file_path.is_file():
            upload_file(file_path, url, timeout)


if __name__ == "__main__":
    main()
