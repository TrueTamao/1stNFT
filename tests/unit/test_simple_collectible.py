from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
from brownie import network
import pytest
from scripts.simple_collectible.deploy_n_create import deploy_n_create


def test_can_create_simple_collectible():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    simple_collectible = deploy_n_create()
    assert simple_collectible.ownerOf(0) == get_account()
    