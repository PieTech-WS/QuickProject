from xmlrpc.server import SimpleXMLRPCServer
from socketserver import ThreadingMixIn


class Server(ThreadingMixIn, SimpleXMLRPCServer):
    pass
