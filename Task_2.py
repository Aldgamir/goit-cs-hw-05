import requests
import re
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt
from tqdm import tqdm

def fetch_text_from_url(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def map_words(text):
    # Виправлємо код для кращого опрацювання символів українською мовою
    words = re.findall(r'\b[а-яєіїґ]+\b', text.lower(), flags=re.IGNORECASE)
    return Counter(words)

def reduce_word_counts(counts1, counts2):
    counts1.update(counts2)
    return counts1

def map_reduce(text, num_workers=4):
    text_length = len(text)
    chunk_size = text_length // num_workers
    text_chunks = [text[i*chunk_size:(i+1)*chunk_size] for i in range(num_workers)]
    
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        mapped_results = list(executor.map(map_words, text_chunks))
    
    total_counts = Counter()
    for counts in mapped_results:
        total_counts = reduce_word_counts(total_counts, counts)
    
    return total_counts

def visualize_top_words(word_counts, top_n=10):
    top_words = word_counts.most_common(top_n)
    words, counts = zip(*top_words)
    plt.figure(figsize=(10, 5))
    plt.bar(words, counts)
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.title(f'Top {top_n} Most Frequent Words')
    plt.xticks(rotation=45)  # Поворот підписів на вісі X для кращої видимості
    plt.show()

if __name__ == "__main__":
    url = "https://tsn.ua/ukrayina/okupanti-vikoristovuyut-use-scho-plavaye-zsu-pokazali-urazhennya-chovniv-armiyi-rf-video-2615979.html"
    text = fetch_text_from_url(url)
    word_counts = map_reduce(text)
    visualize_top_words(word_counts)