

def hello_world(name: str = None) -> str:
    name = "world" if not name else name
    return f"Hello {name}!"

