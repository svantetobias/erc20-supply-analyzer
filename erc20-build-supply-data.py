#!/usr/bin/python3
import argparse
import os
import signal
import sys
import subprocess
import math
from datetime import datetime

# Register SIGINT handler (when user presses CTRL+C)
def signal_handler(sig, frame):
  print("\nClosing...")
  csv_file.close()
  sys.exit(1)

signal.signal(signal.SIGINT, signal_handler)

# Get environment variables from shell so we can use current PATH when running shell commands
env = {}
env.update(os.environ)

# Run a shell command and return the output
def run_cmd(cmd):
  return subprocess.run(
    cmd,
    shell=True,
    check=True,
    universal_newlines=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    env=env
  ).stdout.strip()

# Use Seth to read the supply of the ERC20 token contract at the specified block number
def get_erc20_supply(address, block):
  seth_result = run_cmd(f"seth call {address} 'totalSupply()' -B {block} | seth --to-dec")
  if seth_result == "":
    print(f"Could not read ERC20 supply of {address} at block {block}. Possible causes include: ERC20 contract was not deployed at that block, or the contract is not an ERC20 with 'totalSypply()' function.")
    print("Exiting...")
    sys.exit(0)
  else:
    return int(seth_result)/(10**erc20_decimals)

# Configure and read cmd arguments
parser = argparse.ArgumentParser(description="Read ERC20 token supply and write result to a CSV file.\nReads supply from the given block number and *backwards* with the given interval of blocks between data points.\n\nExample: python3 erc20-build-supply-data.py --start 8090000 --end 8000000 --interval 100 0x2260fac5e5542a773aa44fbcfedf7c193bc2c599")
parser.add_argument("erc20_address")
parser.add_argument("-s", "--start", default="latest", help="Block number to start at. Can be 'latest' or a block number like '8293843'. Default: latest.")
parser.add_argument("-e", "--end", default=0, type=int, help="Block number to stop at. Will automatically stop if the contract call stops giving results, i.e. if we go before the contract was deployed. Default: 0.")
parser.add_argument("-i", "--interval", default=5760, type=int, help="How many blocks to skip between data points. There are approximately 5760 blocks in a day. Default: 5760")
parser.add_argument("-o", "--output", default="erc20_supply_data.csv", type=str, help="Filename or full path to save CSV file. Remember to post-fix it with .csv. Default: erc20_supply_data.csv")

args = parser.parse_args()

blocks_per_datapoint = args.interval
contract_address = args.erc20_address
csv_file_path = args.output

# Determining start block
print("Fetching lastest Ethereum block number...")
start_block = int(run_cmd('seth block latest number'))
print(f"Latest block number: {start_block}")
print("")
if args.start != "latest":
  try:
    i = int(args.start)
    if i <= start_block:
      start_block = i
    else:
      print("Parameter start_block must be less or equal the latest block number.")
      sys.exit(1)
  except ValueError:
    print("Parameter start_block must be a number or the string 'latest'")
    sys.exit(1)

end_block = args.end
current_block = start_block

print("Fetching decimals for ERC20...")
erc20_decimals = int(run_cmd(
    f"seth call {contract_address} 'decimals()' -B {current_block} | seth --to-dec"))
print(f"Decimals: {erc20_decimals}")
print("")

# Initialize CSV file with column names
csv_file = open(csv_file_path, "w+")
csv_file.write("block,supply,timestamp\n")
csv_file.close()

# Read ERC20 Supply until done
while current_block >= end_block:
  print(f"Fetching data for block {current_block}...")

  # Get datetime of current block
  timestamp = int(run_cmd(f"seth block {current_block} timestamp"))
  block_datetime = datetime.utcfromtimestamp(timestamp).isoformat()
  print("block_datetime", block_datetime)

  # Get token supply at current block
  erc20_supply = get_erc20_supply(contract_address, current_block)
  print("erc20_supply", erc20_supply)

  # Write result to DataFrame and CSV
  csv_file = open(csv_file_path, "a")
  csv_file.write(f"{current_block},{erc20_supply},{block_datetime}\n")
  csv_file.close()

  # Move to next block we want to read
  current_block -= blocks_per_datapoint
  print("")
