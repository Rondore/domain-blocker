#!/usr/bin/env python3

import os
import platform
from tempfile import NamedTemporaryFile
import util

ip_address = '0.0.0.0'
section_name = 'RONDORE-DOMAIN-BLOCKER'

return_line = '\n'
if platform.system() == 'Windows':
  return_line = '\r\n'

def hostsname():
  if platform.system() == 'Windows':
    return os.path.join( 'C:/', 'Windows', 'System32', 'drivers', 'etc', 'hosts' )
  elif platform.system() == 'Darwin':
    return '/private/etc/hosts'
  elif platform.system() == 'Android':
    return '/system/etc/hosts'
  else:
    return os.path.join( '/etc', 'hosts' )

def write_blocks(hostsFile):
  writeCount = 0
  block_list = util.get_domain_list(util.full_block_list())
  for line in block_list:
      hostsFile.write( ip_address + ' ' + line + return_line )
      hostsFile.write( ip_address + ' www.' + line + return_line )
      writeCount += 1
  print('Wrote ' + str(writeCount) + ' entries')

def rewrite_hosts_file():
  hosts = hostsname()
  dirpath = os.path.dirname(hosts)
  deleting = False
  inserted = False
  with open(hosts) as file, NamedTemporaryFile('w', dir=dirpath, delete=False) as outfile:
    for line in file:
      if f'#START {section_name}' in line:
        outfile.write(line)
        write_blocks(outfile)
        inserted = True
        deleting = True
      elif f'#END {section_name}' in line:
        deleting = False
        outfile.write(line)
      elif not deleting:
        outfile.write(line)
      #else:
        #print('Skipping: ' + line)
    if not inserted:
      outfile.write(f'#START {section_name} - AUTOGENERATED (DO NOT MODIFY)' + return_line)
      write_blocks(outfile)
      outfile.write(f'#END {section_name}' + return_line)
  with open(outfile.name) as inflow, open(hosts, 'w') as outflow:
    for line in inflow:
      outflow.write(line)
  os.remove(outfile.name)
  #print('Tempfile: ' + outfile.name)

if __name__ == "__main__":
  rewrite_hosts_file()
