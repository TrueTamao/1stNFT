from brownie import accounts, network, config

LOCAL_BLOCKCHAIN_DEVELOPMENT = ["hardhat", "development", "ganache"]


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if network.show_active() in LOCAL_BLOCKCHAIN_DEVELOPMENT:
        return accounts[0]
    if id:
        return accounts.load(id)

    return accounts.add(config["wallets"]["fromKey"])
