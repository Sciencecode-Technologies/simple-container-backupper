"""
Core Module
Basic methods, settings.
"""
import json
import docker


class ConbackCore:
    """
    - Reading configs
    - Docker methods
    """
    def __init__(self, config_file_name: str = "config.json"):
        self.__config_file_name = config_file_name

        self.__docker_client = docker.from_env()

    def __get_config_file(self):
        with open(self.__config_file_name) as config_file:
            self.config = json.load(config_file)
        # Reading JSON config file
