
from functools import partial
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
from ssl import wrap_socket
from urllib.parse import urlparse
from urllib.parse import parse_qs

from pandas import read_csv

from thefuzz import process

from config import *
from mapping import Mapping as Redirects
from mapping import META
from mapping import STYLE


MAPPING = Redirects(path=MAPPING_FILE)


class GoLinksHandler(BaseHTTPRequestHandler):
    def construct_response(self, status: int, data: str):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(META + STYLE + data, "utf-8"))
    
    def construct_json_response(self, status: int, data: str):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(data, "utf-8"))

    def construct_redirect(self, url: str):
        self.send_response(302)
        self.send_header("Location", url)
        self.end_headers()

    def construct_ico(self):
        self.send_response(200)
        self.send_header("Content-Type", "image/x-icon")
        self.send_header("Content-Length", 0)
        self.end_headers()

    def get_metrics(self):
        # read metrics file
        df = read_csv(METRICS_FILE, header=0)
        df = df[~df.shortlink.str.startswith(TEST_LINK_PREFIX)]
        df = df.groupby(["shortlink", "domain"]).count()
        df = df.reset_index().sort_values(by="datetime", ascending=False)
        return df.to_html()

    def do_GET(self):
        parsed = urlparse(self.path)
        shortlink = parsed.path[1:]
        url = MAPPING.get(shortlink)

        # if empty path, show all redirects
        if not shortlink:
            self.construct_response(200, str(MAPPING))

        elif self.path.startswith("/favicon.ico"):
            self.construct_ico()

        # Create new routes
        elif parsed.path.startswith(NEW_LINK_PREFIX):
            response, ok = MAPPING.set_from_qs(parsed.query)
            self.construct_response(status=200 if ok else 406, data=response)
            return
        
        # Analytics routes
        elif parsed.path.startswith(ANALYTICS_LINK_PREFIX):
            response = self.get_metrics()
            self.construct_response(status=200, data=response)
            return
        
        # API routes
        elif parsed.path.startswith(API_LINK_PREFIX):
            search = parse_qs(urlparse(self.path).query).get("q", [""])[0]
            response = MAPPING.search_mapping(search)
            self.construct_json_response(status=200, data=response)
            return
        
        # Create delete routes
        elif parsed.path.startswith(DELETE_LINK_PREFIX):
            response = MAPPING.delete_from_qs(parsed.query)
            self.construct_response(status=200, data=response)
            return

        # if route not found
        elif url is None:
            self.construct_response(
                status=404, data="Sorry no mapping found for {}".format(parsed.path)
            )
        else:
            # if redirect found
            self.log_redirect(shortlink, url)
            self.construct_redirect(url)
        return

    def log_redirect(self, shortlink: str, url: str):
        # log redirects for analysis
        with open(METRICS_FILE, "a") as f:
            f.write(f"{self.log_date_time_string()},{shortlink},{url}\n")

    def log_request(self, code: str="-", size: str="-"):
        # switch off default logging
        return


server = HTTPServer(("localhost", PORT), GoLinksHandler)
if PORT == 443:
    server.socket = wrap_socket(server.socket, certfile=CERTIFICATE_FILE, server_side=True)
server.serve_forever()
