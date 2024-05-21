import requests, os, json
import numpy as np


def get_ids(path="partIds.csv"):
    ids = np.genfromtxt(path, delimiter=",", skip_header=1, usecols=0, dtype=str)
    return ids


def create_dir(dir_path="BiggestBook"):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)


def get_json_data(id="HONMTS01EA11"):
    headers = {
        "X-API-KEY": "31BC6E02FD51DF7F7CE37186A31EE9B9DEF9C642526BC29F8201D81B669B9",
    }
    url = f"https://api.essendant.com/digital/digitalservices/search/v2/items?&vc=n&sgs=Simple&win={id}&re=Detail&"
    resp = requests.get(
        url,
        headers=headers,
    )

    json_data = resp.json()["items"][0]

    return json_data


def format_json_data(json_data):
    json_data_formatted = {}
    json_data_formatted["title"] = json_data["description"]
    json_data_formatted["shortDesc"] = json_data["sellingPoints"]
    json_data_formatted["longDesc"] = json_data["sellingCopy"]
    json_data_formatted["productDetails"] = {
        a["name"]: a["value"] for a in json_data["attributes"]
    }
    json_data_formatted["shippingWeightItemDimensions"] = {
        "weight": f'{json_data["weight"]}{json_data["weightUnit"]}',
        "length": f'{json_data["length"]}{json_data["lengthUnit"]}',
        "height": f'{json_data["height"]}{json_data["heightUnit"]}',
        "width": f'{json_data["width"]}{json_data["widthUnit"]}',
    }
    try:
        json_data_formatted["warranty"] = json_data["warranty"]
    except:
        # no warranty
        pass
    json_data_formatted["partNum"] = json_data["win"]
    try:
        json_data_formatted["images"] = ["https:" + json_data["image"]["url"]] + [
            "https:" + i["url"] for i in json_data["moreImages"]
        ]
    except:
        # no extra images
        pass

    try:
        json_data_formatted["options"] = [
            option["description"] for option in json_data["skuGroupItems"]
        ]
    except:
        # no options
        pass

    return json_data_formatted


def export_to_json(full_path, json_data):
    with open(full_path, "w") as json_file:
        json.dump(json_data, json_file, indent=4, sort_keys=False)
