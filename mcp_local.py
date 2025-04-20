import asyncio

class App:
    def __init__(self, name):
        self.name = name
        self._handlers = {}

    def register_request(self, request_name, handler):
        self._handlers[request_name] = handler

    def create_initialization_options(self):
        return {}

    def run(self, stdin=None, stdout=None, init_options=None):
        print(f"[MCP] Starting app '{self.name}' with handlers: {list(self._handlers.keys())}")
        # Minimal event loop to keep the server alive
        try:
            asyncio.get_event_loop().run_forever()
        except KeyboardInterrupt:
            print("[MCP] App stopped.")
