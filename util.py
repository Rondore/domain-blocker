#!/usr/bin/env python3

import os

project_dir = os.path.abspath(os.path.dirname(__file__))
cache_dir = os.path.join(project_dir, "cache")
config_dir = os.path.join(project_dir, "config")

def reserve_cache_file(file: str) -> str:
    os.makedirs(cache_dir, exist_ok=True)
    return os.path.join(cache_dir, file)

def config_file(file: str) -> str:
    return os.path.join(config_dir, file)

def full_block_list() -> str:
    return reserve_cache_file('compiled_block.list')

def get_headers():
    return {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:137.0) Gecko/20100101 Firefox/137.0'}

def get_domain_list(filename: str) -> list[str]:
    domain_list: list[str] = []
    if os.path.isfile(filename):
        with open(filename, 'r') as allow_content:
            for line in allow_content.readlines():
                line = line.strip()
                if len(line) > 0 and line[0] != '#':
                    domain_list.append(line)
    return domain_list