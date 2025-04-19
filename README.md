This projects updates your hosts file to block domains used for tracking and advertising. It pulls block lists from multiple sources, adds a few more domains to block and removes a few domains from being blocked. It also allows the user to block or allow domains using their own lists.

# Prerequisites

This script requires that you have python 3 installed on Windows or Linux. The project only uses core python libraries so no pip or venv commands are needed.

# Running

## Step 1: pulling lists

First we need to aggregate the current block lists and compile them into a single file. To do so, run this command:

```bash
./pull_all.py
```

If you changed your user block/allow lists (see below) and want to apply the changes without updating from remote sources, we can simply recompile the lists with this command:

```bash
./pullall.py usecache
```

## Step 2: updating hosts files

Now that the full list of blocked domains is compiled, use this command to apply them to your hosts file:

#### Linux:
```bash
sudo ./update_hosts_file.py
```

#### Windows:
```shell
./update_hosts_file.py
```

# Adding your own blocks and allows

You can create the files `config/block.user.list` and `config/allow.user.list` to block and allow domains respectively. In both lists, you can add one domain per line. If a domain is listed in both files, the allow list takes precedence.

Once any user lists have been updated, you will need to re-run both commands above to apply the changes.

It sould be noted that for each domain that is blocked, the "www" subdomain is also blocked. So if example.com is blocked, www.example.com is also blocked.

# Removing all blocks

To remove all blocks applied by this script, remove the compiled domain list file. Then run the `update_hosts_file` command from step 2. You can remove the compiled domain list file with this command:

#### Linux:
```bash
rm cache/compiled_block.list
```

#### Windows:
```shell
del cache/compiled_block.list
```