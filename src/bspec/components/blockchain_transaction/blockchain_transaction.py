from dataclasses import dataclass as component
from typing import Dict

from deprecated.sphinx import versionadded

from bspec.components import component_factory

###########################################
# Define BlockchainTransaction Component: #
###########################################
@versionadded(
    version="0.1.11",
    reason="This allows for transaction values intended to be used with blockchain logic",
)
@component
class BlockchainTransaction:
    """This allows for transaction values intended to be used with blockchain logic

    Params:
        from_address (str): the address that the transaction comes from

        to_address (str): the address that the transaction is going to

        data (Dict[str:Dict]): this is a dictionary of the transaction data.
                the dictionary allows you to include multiple nested datasets

        amount (float): allows you to assign a value (transaction amount), to
                the transaction, sent from `from_address` to the `to_address`
    """

    from_address: str
    to_address: str
    data: Dict[str:Dict]
    amount: float = 0


def register() -> None:
    """use `component_factory` to register the `BlockchainTransaction` component as 'blockchain_transaction'"""
    component_factory.register("blockchain_transaction", BlockchainTransaction)
