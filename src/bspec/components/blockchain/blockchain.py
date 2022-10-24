from dataclasses import dataclass as component
from typing import List, Sequence
import uuid

from deprecated.sphinx import versionadded

from bspec.components import component_factory
from bspec.components.blockchain_transaction.blockchain_transaction import (
    BlockchainTransaction,
)
from bspec.components.blockchain_block.blockchain_block import BlockchainBlock

################################
# Define Blockchain Component: #
################################
@versionadded(
    version="0.1.11",
    reason="This allows unique instance of a blockchain and it's logic",
)
@component
class Blockchain:
    """This allows unique instance of a blockchain and it's logic

    Params:
        name (str): the name of the Blockchain instance

        symbol (str): the symbol of the Blockchain instance

        difficulty (int, default 2): the number of 0's at the beginning of the hashed
                block, this will be passed down to the BlockchainBlock object

        mining_reward (float, default 1): the reward for mining a block

        pending_transactions (Sequence[BlockchainTransaction], default None): a list of unprocessed
                BlockchainTransaction's. Each Block will be processed

        chain (Sequence[BlockchainTransaction], default None): the list of processed
                BlockchainTransaction's. Each Block has been processed and creates the chain

        hash_func (str, default sha512): the hashing function that should be used for
                hashing the transactions and block data

        _encoding (str, default utf-8): what string encoding should be used

        __init_previous_hash (str, default uuid4): root block initial previous hash
    """

    name: str
    symbol: str
    difficulty: int = 2
    mining_reward: float = 1
    pending_transactions: Sequence[BlockchainTransaction] = None
    chain: Sequence[BlockchainTransaction] = None
    hash_func: str = "sha512"
    _encoding: str = "utf-8"
    __init_previous_hash: str = None

    def __post_init__(self):
        """
        Default class attribute values
        """
        self.__init_previous_hash = str(uuid.uuid4())
        if self.chain is None or self.chain == []:
            self.chain = [self.create_root_block()]

        if self.pending_transactions is None or self.pending_transactions == []:
            self.pending_transactions = []

    def create_root_block(self) -> BlockchainBlock:
        """this will create the first instance of a BlockchainBlock for the blockchain

        Returns:
            BlockchainBlock: initial block of empty transactions
        """
        return BlockchainBlock(
            transactions=[],
            difficulty=self.difficulty,
            previous_hash=self.__init_previous_hash,
            hash_func=self.hash_func,
            _encoding=self._encoding,
        )

    def get_latest_block(self) -> BlockchainBlock:
        """return most recent BlockchainBlock from the `chain` to be used for `previous_hash`

        Returns:
            BlockchainBlock: return most recent BlockchainBlock from the `chain`
        """
        return self.chain[len(self.chain) - 1]

    def mine_pending_transactions(self, mining_reward_address: str) -> None:
        """This will mine all pending transactions

        Args:
            mining_reward_address (str): the address to add the mining_reward to
        """
        reward = BlockchainTransaction(
            None,
            mining_reward_address,
            {"message": "Verifying transactions"},
            self.mining_reward,
        )
        self.pending_transactions.append(reward)

        block = BlockchainBlock(
            transactions=self.pending_transactions,
            difficulty=self.difficulty,
            previous_hash=self.get_latest_block().hash,
            hash_func=self.hash_func,
            _encoding=self._encoding,
        )
        block.mine_block()

        print("Block successfully mined!")
        self.chain.append(block)

        self.pending_transactions = []

    def create_transaction(self, transaction: BlockchainTransaction):
        """Add a transaction to the pending transaction

        Args:
            transaction (BlockchainTransaction): this is a singular BlockchainTransaction
        """
        self.pending_transactions.append(transaction)

    def get_balance_of_address(self, address: str) -> float:
        """The final balance of all transactions for a specific address

        Args:
            address (str): the address to calculate the balance/amount

        Returns:
            float: the final balance of all transactions for a specific address
        """
        balance = 0

        for block in self.chain:
            for transaction in block.transactions:
                if transaction.from_address == address:
                    balance -= transaction.amount

                if transaction.to_address == address:
                    balance += transaction.amount

        return balance

    def is_chain_valid(self) -> bool:
        """Checks all the hashes of a chain to validate that the chain has not changed

        Returns:
            bool: if the chain is valid or not (True/False)
        """
        for i in range(0, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if i == 0 and current_block.previous_hash == self.__init_previous_hash:
                return True
            elif current_block.previous_hash != previous_block.calculate_hash():
                return False

        return True


def register() -> None:
    """use `component_factory` to register the `Blockchain` component as 'blockchain'"""
    component_factory.register("blockchain", Blockchain)
