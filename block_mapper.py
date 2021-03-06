from ethereumetl.domain.block import EthBlock
from ethereumetl.mapper.transaction_mapper import EthTransactionMapper
from ethereumetl.utils import hex_to_dec
from builtins import map


class EthBlockMapper(object):

    transaction_mapper = EthTransactionMapper()

    def json_dict_to_block(self, json_dict):
        # type: ({}) -> EthBlock

        # block mapper文件，对数据格式进行转换
        block = EthBlock()
        # 16进制 to 10进制
        block.number = hex_to_dec(json_dict.get('number', None))
        block.hash = json_dict.get('hash', None)
        block.parent_hash = json_dict.get('parentHash', None)
        block.nonce = json_dict.get('nonce', None)
        block.sha3_uncles = json_dict.get('sha3Uncles', None)
        block.logs_bloom = json_dict.get('logsBloom', None)
        block.transactions_root = json_dict.get('transactionsRoot', None)
        block.state_root = json_dict.get('stateRoot', None)
        block.miner = json_dict.get('miner', None)
        # 16进制 to 10进制
        block.difficulty = hex_to_dec(json_dict.get('difficulty', None))
        block.total_difficulty = hex_to_dec(json_dict.get('totalDifficulty', None))
        block.size = hex_to_dec(json_dict.get('size', None))
        block.extra_data = json_dict.get('extraData', None)
        block.gas_limit = hex_to_dec(json_dict.get('gasLimit', None))
        block.gas_used = hex_to_dec(json_dict.get('gasUsed', None))
        block.timestamp = json_dict.get('timestamp', None)

        if 'transactions' in json_dict:
            # 将block的所有transaction都拿出来，分别调用transaction mapper进行相同的格式转换（大部分还是进制转换）
            # 一个block可能会有上百笔交易
            block.transactions = list(map(lambda tx: self.transaction_mapper.json_dict_to_transaction(tx), json_dict['transactions']))

        return block

    def block_to_dict(self, block):
        # type: (EthBlock) -> {}

        return {
            # 之后返回转换后的数据结果
            'block_number': block.number,
            'block_hash': block.hash,
            'block_parent_hash': block.parent_hash,
            'block_nonce': block.nonce,
            'block_sha3_uncles': block.sha3_uncles,
            'block_logs_bloom': block.logs_bloom,
            'block_transactions_root': block.transactions_root,
            'block_state_root': block.state_root,
            'block_miner': block.miner,
            'block_difficulty': block.difficulty,
            'block_total_difficulty': block.total_difficulty,
            'block_size': block.size,
            'block_extra_data': block.extra_data,
            'block_gas_limit': block.gas_limit,
            'block_gas_used': block.gas_used,
            'block_timestamp': block.timestamp,
            # 我们把block里面的transaction单独放到了一个文件里，这里专注block的数据
            'block_transaction_count': len(block.transactions),
        }
