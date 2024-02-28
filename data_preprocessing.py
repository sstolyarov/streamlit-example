import json


def convert2onelvl(node: dict, parent: str = None) -> dict:
    """
        converting a nested dictionary to a dictionary with a depth of one

        :node: nested dictionary.
        :return: dict.
    """
    result = dict()

    if not parent:

        result["root"] = {
            "children": list(node.keys()),
            "udc": "root",
            "name": "root",
            "parent": None,
        }

        for k, v in node.items():
            result[v["udc"]] = {
                "children": list(v["children"].keys()),
                "udc": v["udc"],
                "name": v["name"],
                "parent": "root",
            }

            for child_k, child_v in v["children"].items():
                result.update(convert2onelvl(child_v, k))

    elif node["children"]:
        result[node["udc"]] = {
                    "children": list(node["children"].keys()),
                    "udc": node["udc"],
                    "name": node["name"],
                    "parent": parent,
                }

        for child_k, child_v in node["children"].items():
            result.update(convert2onelvl(child_v, node["udc"]))

    else:
        result[node["udc"]] = {
                    "children": None,
                    "udc": node["udc"],
                    "name": node["name"],
                    "parent": parent,
                }
    return result


if __name__ == "__main__":

    with open("udc_teacode_utf.json", "r") as fp:
        d_graph = json.load(fp)

    onelvl = convert2onelvl(d_graph)
    with open("udc_teacode_utf_onelvl.json", 'w', encoding='utf-8') as fp:
        json.dump(onelvl, fp, ensure_ascii=False)
