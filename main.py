import hashlib
import os
import file_embedder


def get_all_filenames(dirname):
    results = []
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path):
            results.append(item_path)
        elif os.path.isdir(item_path):
            results += get_all_filesnames(item_path)
    return results


def sha256_of_file(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256_hash.update(chunk)
    return sha256_hash.digest()


def index(directory):
    all_files = get_all_filenames(directory)
    for file in all_files:
        os.setxattr(file, "sha256", sha256_of_file(filepath))
        os.setxattr(file, "embedding", file_embedder.get_file_embedding_from_filename(file))


def search(query, num_results = 15):
    query_embedding = file_embedder.get_file_embedding_from_query(query)
    all_files = get_all_filenames(directory)
    results = []
    for file in all_files:
        results.append([file_embedder.dist(query_embedding), os.getxattr(file, "embedding")])
    results.sort()
    return [x[1] for x in results[:num_results]]

