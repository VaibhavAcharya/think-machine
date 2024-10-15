import json


class TemporaryMemory:
    def __init__(self):
        self.memory = {}

    def t_keys(self) -> list:
        """List all keys in temporary memory.

        Args: None

        Returns:
            list: keys
        """
        return list(self.memory.keys())

    def t_store(self, key: str, value: str) -> str:
        """Store a value in temporary memory.

        Args:
            key: str
            value: str

        Returns:
            str: success message
        """
        self.memory[key] = value
        return f"Stored '{key}' in temporary memory."

    def t_retrieve(self, key: str) -> str:
        """Retrieve a value from temporary memory.

        Args:
            key: str

        Returns:
            str: value
        """
        return self.memory.get(
            key, f"No value found for key in temporary memory: {key}"
        )

    def t_remove(self, key: str) -> str:
        """Remove a value from temporary memory.

        Args:
            key: str

        Returns:
            str: success message
        """
        self.memory.pop(key, None)
        return f"Removed '{key}' from temporary memory."


class PersistentMemory:
    def __init__(self, filepath: str):
        self.filepath = filepath  # a json file to store the memory
        self.memory = {}
        self.p_load()

    def p_sync(self):
        with open(self.filepath, "w") as f:
            json.dump(self.memory, f, indent=2)

    def p_load(self):
        with open(self.filepath, "r") as f:
            self.memory = json.load(f)

    def p_keys(self) -> list:
        """List all keys in persistent memory.

        Args: None

        Returns:
            list: keys
        """
        self.p_load()
        return list(self.memory.keys())

    def p_store(self, key: str, value: str) -> str:
        """Store a value in persistent memory.

        Args:
            key: str
            value: str

        Returns:
            str: success message
        """
        self.memory[key] = value
        self.p_sync()
        return f"Stored '{key}' in persistent memory."

    def p_retrieve(self, key: str) -> str:
        """Retrieve a value from persistent memory.

        Args:
            key: str

        Returns:
            str: value
        """
        self.p_load()
        return self.memory.get(
            key, f"No value found for key in persistent memory: {key}"
        )

    def p_remove(self, key: str) -> str:
        """Remove a value from persistent memory.

        Args:
            key: str

        Returns:
            str: success message
        """
        self.memory.pop(key, None)
        self.p_sync()
        return f"Removed '{key}' from persistent memory."
