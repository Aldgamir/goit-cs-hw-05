import argparse
import asyncio
import aiofiles
import os
from pathlib import Path

async def copy_file(src, dst):
    try:
        dst.parent.mkdir(parents=True, exist_ok=True)
        async with aiofiles.open(src, 'rb') as fsrc:
            async with aiofiles.open(dst, 'wb') as fdst:
                while True:
                    buffer = await fsrc.read(1024 * 1024)
                    if not buffer:
                        break
                    await fdst.write(buffer)
        print(f"Copied: {src} to {dst}")
    except Exception as e:
        print(f"Error copying {src} to {dst}: {e}")

async def read_folder(src_folder, dst_folder):
    tasks = []
    for root, _, files in os.walk(src_folder):
        for file in files:
            src_path = Path(root) / file
            file_ext = src_path.suffix[1:]
            dst_path = Path(dst_folder) / file_ext / file
            tasks.append(copy_file(src_path, dst_path))
    await asyncio.gather(*tasks)

def main():
    parser = argparse.ArgumentParser(description="Asynchronous file sorter by extension.")
    parser.add_argument('src_folder', type=str, help="Source folder to read files from.")
    parser.add_argument('dst_folder', type=str, help="Destination folder to store sorted files.")
    args = parser.parse_args()

    src_folder = Path(args.src_folder)
    dst_folder = Path(args.dst_folder)

    if not src_folder.is_dir():
        print(f"Source folder '{src_folder}' does not exist or is not a directory.")
        return

    asyncio.run(read_folder(src_folder, dst_folder))

if __name__ == "__main__":
    main()


# Тепер, замість прописання шляху до директорій безпосередньо в коді, можна використовувати командний рядок...
