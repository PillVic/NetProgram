from GetWeather import getWeather
from http.server import BaseHTTPRequestHandler, HTTPServer
import codecs

class WeatherServer(BaseHTTPRequestHandler):
    def do_GET(self):
        print('Path:' + self.path)
        if '?' in self.path:
            print('Start Searching for Weather...')
            t, city = self.path.split('?')
            city = codecs.decode(city, 'unicode_escape')
            print('City Name: '+ city)
            info = getWeather(city)
            print(info)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(info, 'utf-8'))
        else:
            print('Searching for Main Page......')
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = open('index.html').read()
            self.wfile.write(bytes(message,'utf-8'))
        return

if __name__ == '__main__':
    print('Start Server .....')
    serverAddress = ('127.0.0.1', 8081)
    httpd = HTTPServer(serverAddress, WeatherServer)
    print('Server is running')
    httpd.serve_forever()
