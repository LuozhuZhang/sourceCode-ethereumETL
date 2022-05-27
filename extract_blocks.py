import argparse
import fileinput
import json

from ethereumetl.exporters import CsvItemExporter
from ethereumetl.mapper.block_mapper import EthBlockMapper
from ethereumetl.utils import smart_open

parser = argparse.ArgumentParser(description='Extract blocks from eth_getBlockByNumber JSON RPC output')
# 输入批量RPC的JSON文件
parser.add_argument('--input', default=None, type=str, help='The input file. If not specified stdin is used.')
# 导出解析后的数据，我们load成了csv文件，方便之后导入Clickhouse数据库
parser.add_argument('--output', default=None, type=str, help='The output file. If not specified stdout is used.')

args = parser.parse_args()

with smart_open(args.output, binary=True) as output_handle:
    # 定义解析的数据结构
    block_mapper = EthBlockMapper()

    # CsvItemExporter将每行数据导入CSV table中
    exporter = CsvItemExporter(output_handle)
    # 开始导入
    exporter.start_exporting()
    for line in fileinput.input(files=args.input):
        # 从RPC batch（JSON文件）中分别取出每一行的单个RPC
        json_line = json.loads(line)
        # 得到geth返回的raw data
        result = json_line.get('result', None)
        if result is None:
            continue
        # 如果没有出现报错，则把raw data转换成我们之前定义好的格式
        block = block_mapper.json_dict_to_block(result)
        # 将转换后的clean data导入CSV文件
        exporter.export_item(block_mapper.block_to_dict(block))
    # 导入结束，生成csv文件
    exporter.finish_exporting()




 