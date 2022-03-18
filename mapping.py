from collections import OrderedDict
from json import loads
from json import dumps
from typing import Tuple
from urllib.parse import urljoin
from urllib.parse import urlparse
from urllib.parse import parse_qs

from thefuzz import process


META = """<meta content="text/html;charset=utf-8" http-equiv="Content-Type">
<meta content="utf-8" http-equiv="encoding">"""
# default styling taken from http://bettermotherfuckingwebsite.com/
STYLE = """<style>body{font-family:-apple-system,BlinkMacSystemFont,sans-serif;margin:40px auto;max-width:650px;line-height:1.6;font-size:18px;color:#444;padding:0 10px}h1,h2,h3{line-height:1.2;font-weight:normal;}a{text-decoration:none;}a:visited{color:#00E;}</style>"""


def uri_validator(x: str):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc if result.scheme != "file" else result.path])
    except:
        return False


class LastUsedOrderedDict(OrderedDict):
    'Store items in the order the keys were last added'

    def __getitem__(self, key):
        self.move_to_end(key)
        return super().__getitem__(key)

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.move_to_end(key)

class Mapping:
    def __init__(self, path: str):
        self.mapping = LastUsedOrderedDict()
        self._path = path
        self.load()
    
    def load(self):
        with open(self._path) as f:
            self.mapping = LastUsedOrderedDict(loads(f.read()))

    def save(self):
        with open(self._path, "w") as f:
            f.write(dumps(self.mapping, indent=4))

    def get(self, key: str):
        s = key.split("/")
        if s[0] in self.mapping:
            return urljoin(self.mapping[s[0]], "/".join(s[1:]))
        return None

    def set(self, key: str, value: str):
        if uri_validator(value):
            self.mapping[key] = value
            self.save()

    def set_from_qs(self, qs: str) -> Tuple[str, bool]:
        response = ""
        ok = True
        for key, value in parse_qs(qs).items():
            value = value[0].strip()
            key = key.strip()
            self.set(key, value)
            if uri_validator(value):
                response += f"{key} -> {value}<br />"
            else:
                response += f"{key} -> {value} (invalid)<br />"
                ok = False
        return response, ok
    
    def delete(self, key: str):
        if key in self.mapping:
            del self.mapping[key]
            self.save()
            return f"Deleted {key}"
        return f"No mapping found for {key}"
    
    def delete_from_qs(self, qs: str):
        response = ""
        for key, _ in parse_qs(qs).items():
            key = key.strip()
            response += self.delete(key)
            response += f"<br />"
        return response
    
    def get_as_json(self) -> str:
        result = []
        for k, v in reversed(self.mapping.items()):
            result.append({
                "key": k,
                "value": v
            })
        return dumps(result, indent=4)
    
    def search_mapping(self, search: str) -> dict:
        if len(search) == 0:
            return self.get_as_json()
        keys = list(self.mapping.keys())
        selected = process.extract(search, keys)
        results = []
        for key, _ in selected:
            results.append({
                "key": key,
                "value": self.mapping[key]
            })
            
        return dumps(results, indent=4)

    def __str__(self) -> str:
        s = ""
        for key, value in sorted(self.mapping.items()):
            s += f"<h3><a href='{value}' target='_blank'>{key}</a> - {value}</h3>"
        return s
