from brownie import AdvancedCollectible

def main():
    advanced_collectible = AdvancedCollectible[-1]
    number_of_advanced_collectible = advanced_collectible.tokenCounter()
    print(f"You ve created {number_of_advanced_collectible} collectible ")