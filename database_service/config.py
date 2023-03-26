import json, xml, tomllib


class DatabaseConfig:
    def __init__(self, file_name: str):
        self.file = file_name
        self.option_dict = {
            "json": self.from_json(),
            "py": self.from_pyfile(),
            "xml": self.from_xml(),
            "toml": self.from_toml(),
        }
        self.option_dict["".format(lambda: file_name.split(".")[:][1])]

    def from_json(self):
        json_data = json.loads(self.file)
        return json_data

    def from_pyfile(self): ...

    def from_xml(self): ...

    def from_toml(self): ...
