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
        self.active_containers = []
        self.images = []
        self.selected_containers = []
        # Defindings
        self.__get_config_file()

    def __get_config_file(self):
        """
        reads config file
        """
        with open(self.__config_file_name, encoding="UTF-8") as config_file:
            self.config = json.load(config_file)

    def list_active_containers(self):
        """
        returns: list

        Lists active docker containers
        """
        containers = self.__docker_client.containers.list()
        for container in containers:
            self.active_containers.append((container.id, container.name))
        return self.active_containers

    def list_images(self):
        """
        returns: list

        Lists images
        """
        images = self.__docker_client.images.list()
        for image in images:
            self.images.append((image.id, image.tags[0].split(':')))
        return self.images

    def select_containers(self, selections: str):
        """
        returns: list

        Gets containers hash
        """
        __selections = selections.split(' ')
        for container_index in range(len(self.active_containers)):
            for selected_id in __selections:
                if selected_id in self.active_containers[container_index][0][:self.config['General']['id_len']]:
                    if selected_id not in self.selected_containers:
                        self.selected_containers.append(self.__docker_client.containers.list()[container_index])
        return self.selected_containers
