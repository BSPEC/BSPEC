from dataclasses import dataclass as component
from dataclasses import asdict
from datetime import datetime
import json
import hashlib
from typing import List
import uuid

from deprecated.sphinx import versionadded

from bspec.components import component_factory
from bspec.components.blockchain_transaction.blockchain_transaction import (
    BlockchainTransaction,
)

#####################################
# Define BlockchainBlock Component: #
#####################################
@versionadded(
    version="0.1.11",
    reason="This allows for a block of transactions intended to be used with blockchain logic",
)
@component
class BlockchainBlock:
    """This allows for a block of transactions intended to be used with blockchain logic

    Params:
        transactions (List[BlockchainTransaction]): a list of BlockchainTransactions
                that will become a single block

        difficulty (int, default 2): the number of 0's at the beginning of the hashed
                block

        previous_hash (str, default uuid4): will be the previous blocks hashed value.
                this will be used in the current hash and will ensure that the chain
                is correct and has not been tampered with as the previous hash is
                baked into the next hashed value

        timestamp (datetime, default now): the current block process timestamp

        nonce (int, default 0): the current nonce value used to adjust the current `_hash`
                to add additional 0's, to the number in `difficulty` at the beginning
                of a hashed value. this value allows you to change the output hash without
                changing the data values

        hash_func (str, default sha512): the hashing function that should be used for
                hashing the transactions and block data

         _hash (str): a `property` value based on the hashed value of the transactions.
                it is the Encrypted Hash of the transactions

        _encoding (str, default utf-8): what string encoding should be used
    """

    transactions: List[BlockchainTransaction]
    difficulty: int = 2
    previous_hash: str = str(uuid.uuid4())
    timestamp: datetime = datetime.now()
    nonce: int = 0
    hash_func: str = "sha512"
    _hash: str = ""
    _encoding: str = "utf-8"

    @property
    def hash(self):
        return self._hash

    @hash.getter
    def hash(self):
        self._hash = self.calculate_hash()
        return self._hash

    def calculate_hash(self):
        """calculate an Encrypted Hash of the transactions

        Returns:
            hexdigest: Encrypted Hash of:
                he previous_hash
                + string of timestamp
                + string of transactions
                + string of nonce
        """
        transaction = (
            str(self.previous_hash)
            + self.timestamp.strftime("%Y/%m/%d %H:%M:%S")
            + json.dumps([asdict(transaction) for transaction in self.transactions])
            + str(self.nonce)
        )
        h = hashlib.new(self.hash_func)
        h.update(transaction.encode(self._encoding))
        encrypted_transaction = h.hexdigest()

        return encrypted_transaction

    def mine_block(self):
        """This will continue to hash the block until the beginning
            of the hash string matches the `difficulty` * "0"
            e.g. if the `difficulty` is 3 then there should be 3 0's
                at the beginning of the hash:
                000a92e9fb40f0d507ccffa87773260e9d42ef7d48fe1e96...

        Returns:
            hexdigest: Encrypted Hash of:
                he previous_hash
                + string of timestamp
                + string of transactions
                + string of nonce
        """
        while self._hash[0 : self.difficulty] != ("0" * self.difficulty):
            self.nonce = self.nonce + 1
            self.hash

        return self._hash


def register() -> None:
    """use `component_factory` to register the `BlockchainBlock` component as 'blockchain_block'"""
    component_factory.register("blockchain_block", BlockchainBlock)
