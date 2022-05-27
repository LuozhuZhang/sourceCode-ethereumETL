import json
import argparse

from builtins import str

from ethereumetl.utils import smart_open

# argparse用于terminal输入参数
parser = argparse.ArgumentParser(
    description='Generate Ethereum eth_getBlockByNumber JSON RPC call inputs for a block range')
parser.add_argument('--start-block', default=0, type=int, help='Start block')
parser.add_argument('--end-block', required=True, type=int, help='End block')
parser.add_argument('--output', default=None, type=str, help='The output file. If not specified stdout is used.')

args = parser.parse_args()

# 批量生成RPC call
def generate_get_block_by_number_json_rpc(start_block, end_block):
    for block_number in range(start_block, end_block):
        yield {
            'jsonrpc': '2.0',
            'method': 'eth_getBlockByNumber',
            # 传入block number，每个block height下都有一个block RPC
            'params': [hex(block_number), True],
            'id': 1,
        }


with smart_open(args.output) as handle:
    # 把所有RPC写入一个JSON文件
    for data in generate_get_block_by_number_json_rpc(args.start_block, args.end_block):
        handle.write(json.dumps(data))
