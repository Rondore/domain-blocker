#!/usr/bin/env python3

import sys
import util
import pull_duck_duck_go_list
import pull_steven_black_list

block_filename = util.config_file('block.list')
allow_filename = util.config_file('allow.list')
user_block_filename = util.config_file('block.user.list')
user_allow_filename = util.config_file('allow.user.list')

class Blocklist():
    block_list: set[str] = set()

    def apply_blocks(self, domain_list: list[str]):
        for domain in domain_list:
            self.block_list.add(domain)

    def remove_blocks(self, domain_list: list[str]):
        for domain in domain_list:
            try:
                self.block_list.remove(domain)
            except KeyError:
                pass

    def get_result(self) -> list[str]:
        return list(self.block_list)

def pull_all():
    pull_duck_duck_go_list.cache_json()
    pull_duck_duck_go_list.parse()
    pull_steven_black_list.cache()

def compile():
    block_list = Blocklist()

    # Apply default block lists
    block_files = [
        pull_duck_duck_go_list.list_file(),
        pull_steven_black_list.list_file(),
        block_filename
    ]
    for filename in block_files:
        block_list.apply_blocks(util.get_domain_list(filename))

    # Apply default allow list
    block_list.remove_blocks(util.get_domain_list(allow_filename))

    # Apply user block list
    block_list.apply_blocks(util.get_domain_list(user_block_filename))

    # Apply user allow list
    block_list.remove_blocks(util.get_domain_list(user_allow_filename))

    # Sort and save
    result = block_list.get_result()
    with open(util.full_block_list(), 'w+') as output:
        for domain in result:
            output.write(domain + '\n')

if __name__ == "__main__":
    pull = True
    for arg in sys.argv:
        lower_arg = arg.lower()
        if lower_arg == 'usecache':
            pull = False
    if pull:
        pull_all()
    compile()