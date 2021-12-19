from json import loads
from json import dumps
from urllib.parse import urljoin
from urllib.parse import urlparse
from urllib.parse import parse_qs


META = """<meta content="text/html;charset=utf-8" http-equiv="Content-Type">
<meta content="utf-8" http-equiv="encoding">"""
# default styling taken from http://bettermotherfuckingwebsite.com/
STYLE = """<style>body{margin:40px auto;max-width:650px;line-height:1.6;font-size:18px;color:#444;padding:0 10px}h1,h2,h3{line-height:1.2}</style>"""


def uri_validator(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc])
    except:
        return False


class Mapping:
    def __init__(self, path):
        self.mapping = {}
        self._path = path
        self.load()

    def load(self):
        with open(self._path) as f:
            self.mapping = loads(f.read())

    def save(self):
        with open(self._path, "w") as f:
            f.write(dumps(self.mapping, sort_keys=True, indent=4))

    def get(self, key):
        s = key.split("/")
        if s[0] in self.mapping:
            return urljoin(self.mapping[s[0]], "/".join(s[1:]))
        return None

    def set(self, key, value):
        if uri_validator(value):
            self.mapping[key] = value
            self.save()

    def set_from_qs(self, qs):
        response = ""
        for key, value in parse_qs(qs).items():
            value = value[0].strip()
            key = key.strip()
            self.set(key, value)
            response += "{} -> {}\n".format(key, value)
        return response

    def __str__(self):
        s = META + STYLE
        for key, value in self.mapping.items():
            s += f"<h3><a href='{value}' target='_blank'>{key}</a> - {value}</h3>"
        return s
