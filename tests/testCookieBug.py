from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from scrapy import Spider, Request
from scrapy.crawler import CrawlerProcess


class RedirectHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/a":
            self.send_response(302)
            self.send_header("Location", "http://localhost:8998/b")
            self.end_headers()
        elif self.path == "/b":
            cookies = self.headers.get("Cookie", "")
            print(f"\n>>> Cookies received at /b: '{cookies}'")
            if "foo=bar" in cookies:
                print(">>> BUG FIXED: cookie was sent to /b!")
            else:
                print(">>> BUG REPRODUCED: cookie was NOT sent to /b!")
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"ok")

    def log_message(self, format, *args):
        pass  


class CookieBugSpider(Spider):
    name = "cookie_bug"

    def start_requests(self):
        yield Request(
            url="http://localhost:8998/a",
            cookies=[{"name": "foo", "value": "bar", "domain": "localhost"}],
            callback=self.parse,
        )

    def parse(self, response):
        pass


if __name__ == "__main__":
    server = HTTPServer(("localhost", 8998), RedirectHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    print("Server started on http://localhost:8998")

    process = CrawlerProcess({
        "TWISTED_REACTOR_ENABLED": True,
        "COOKIES_DEBUG": True,
        "LOG_LEVEL": "WARNING",
    })
    process.crawl(CookieBugSpider)
    process.start()
    server.shutdown()