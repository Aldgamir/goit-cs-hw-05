import asyncio
import aiofiles
from pathlib import Path
import logging
from argparse import ArgumentParser

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Асинхронна функція для рекурсивного читання файлів у папці
async def read_folder(folder: Path):
    files = []
    for item in folder.iterdir():
        if item.is_dir():
            files.extend(await read_folder(item))
        else:
            files.append(item)
    return files

# Асинхронна функція для копіювання файлів у відповідні підпапки на основі розширення
async def copy_file(file: Path, output_folder: Path):
    ext = file.suffix.lstrip('.').lower()  # Отримання розширення файлу
    target_folder = output_folder / ext
    target_folder.mkdir(parents=True, exist_ok=True)
    target_file = target_folder / file.name

    async with aiofiles.open(file, 'rb') as fsrc:
        async with aiofiles.open(target_file, 'wb') as fdst:
            await fdst.write(await fsrc.read())

# Головна асинхронна функція
async def main(source_folder: Path, output_folder: Path):
    try:
        files = await read_folder(source_folder)
        tasks = [copy_file(file, output_folder) for file in files]
        await asyncio.gather(*tasks)
        logger.info("Files sorted successfully.")
    except Exception as e:
        logger.error(f"Error occurred: {e}")

# Основний блок для запуску скрипта
if __name__ == "__main__":
    source_folder = Path("/Users/vladimirvinogradov/Desktop/germany.select.shop")   # Шлях до директорії з файлами для сортування
    output_folder = Path("/Users/vladimirvinogradov/Desktop/Новая папка")   # Шлях до директорії для відсортованих файлів
    output_folder.mkdir(parents=True, exist_ok=True)

    asyncio.run(main(source_folder, output_folder))