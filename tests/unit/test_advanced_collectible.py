import pytest
from brownie import network, AdvancedCollectible
from scripts.helpful_scripts import (
    get_account,
    get_contract,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)
from scripts.advanced_collectible.deploy_n_create import deploy_n_create


def test_can_create_advanced_collectible():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    
    advanced_collectible, transaction_receipt = deploy_n_create()

    requestId = transaction_receipt.events["requestedCollectible"]["requestId"]
    assert isinstance(transaction_receipt.txid, str)
    get_contract("vrf_coordinator").callBackWithRandomness(
        requestId, 777, advanced_collectible.address, {"from": get_account()}
    )
    # Assert
    assert advanced_collectible.tokenCounter() > 0
    assert advanced_collectible.tokenIdToBreed(0) == 777 % 3
    assert isinstance(advanced_collectible.tokenCounter(), int)