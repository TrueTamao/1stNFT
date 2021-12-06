from brownie import AdvancedCollectible, network
from scripts.helpful_scripts import get_breed
from metadata.sample_metadata import metadata_template
from pathlib import Path
import requests
import json
import os

breed_to_image_uri = {
    "PUG": "https://ipfs.io/ipfs/QmSsYRx3LpDAb1GZQm7zZ1AuHZjfbPkD6J7s9r41xu1mf8?filename=pug.png",
    "SHIBA_INU": "https://ipfs.io/ipfs/QmYx6GsYAKnNzZ9A6NvEKV9nf1VaDzJrqDR23Y8YSkebLU?filename=shiba-inu.png",
    "ST_BERNARD": "https://ipfs.io/ipfs/QmUPjADFGEKmfohdTaNcWhp7VGk26h5jXDA7v3VtTnTLcW?filename=st-bernard.png",
}

def main():
    advanced_collectible = AdvancedCollectible[-1]
    number_of_advanced_collectible = advanced_collectible.tokenCounter()
    print(f"You ve created {number_of_advanced_collectible} collectible ")
    for tokenId in range(number_of_advanced_collectible):
        breed = get_breed(advanced_collectible.tokenIdToBreed(tokenId))
        metadata_filename = f"./metadata/{network.show_active()}/{tokenId}-{breed}.json"
        collectible_metadata = metadata_template
        print(metadata_filename)
        if Path(metadata_filename).exists():
            print(f"File alrd exists, delete to create new")
        else:
            print(f"Creating {metadata_filename}")
            collectible_metadata["name"] =  breed
            collectible_metadata["description"] = f"An Adorable {breed} pup"
            image_uri = None
            if os.getenv("UPLOAD_IPFS") == "true":
                image_path = "./img/" + breed.lower().replace("_", "-") + ".png"
                print(image_path)
                image_uri = upload_to_ipfs(image_path)
            
            image_uri = image_uri if image_uri else breed_to_image_uri[breed]
                 
            collectible_metadata["image"] = image_uri
            with open(metadata_filename, "w") as file:
                json.dump(collectible_metadata, file)
            upload_to_ipfs(metadata_filename)


def upload_to_ipfs(image_path):
    with Path(image_path).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url + endpoint, files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        filename = image_path.split("/")[-1]
        image_uri = "https://ipfs.io/ipfs/{}?filename={}".format(
            ipfs_hash, filename)
        print(image_uri)
        return image_uri

