#!/bin/bash

START_BLOCK=8078112
DAYS_TO_READ=365
BLOCKS_IN_A_DAY=5760
STOP_BLOCK=$(($START_BLOCK - ($DAYS_TO_READ * $BLOCKS_IN_A_DAY)))
current_block=$(($START_BLOCK))
CONTRACT_ADDRESS=0x2260fac5e5542a773aa44fbcfedf7c193bc2c599

export ETH_RPC_URL=https://mainnet.infura.io/6b2a298e15f1496d8e9b2f48decabcf4

erc20_digits=$(seth call $CONTRACT_ADDRESS 'decimals()' -B $current_block | seth --to-dec)
echo "$CONTRACT_ADDRESS decimals: $erc20_digits"
echo ""

echo "block,wbtc_supply,timestamp" > wbtc_supply.csv

while [ $current_block -gt $STOP_BLOCK ]
do
  echo "Reading block $current_block ..."
  wbtc_supply=$(seth call $CONTRACT_ADDRESS 'totalSupply()' -B $current_block | seth --to-dec)
  echo "wbtc_supply: $wbtc_supply"
  wbtc_supply_with_decimals=$(echo "scale=$erc20_digits; $wbtc_supply/(10^$erc20_digits)" | bc -l )
  echo "WBTC Supply at block $current_block: $wbtc_supply_with_decimals"
  
  block_timestamp=$(seth block $current_block timestamp)
  formatted_timestamp=$(date -r $block_timestamp '+%Y-%m-%d %H:%M:%S')
  echo "Timestamp at block $current_block: $formatted_timestamp"

  echo "Saving result to wbtc_supply.csv ..."
  echo "$current_block,$wbtc_supply_with_decimals,$formatted_timestamp" >> wbtc_supply.csv
  echo ""

  current_block=$(($current_block - $BLOCKS_IN_A_DAY))
done