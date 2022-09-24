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
        self.containers = self.__docker_client.containers.list()
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
        for container in self.containers:
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
        attribute:
            - selections: str

        Gets containers hash
        """
        id_len = self.config['General']['id_len']
        active_container_data = {
            "active_containers": self.active_containers,
            "ac_len": len(self.active_containers)
        }
        # locals
        for container_index in range(active_container_data['ac_len']):
            for selected_id in selections.split(' '):
                if selected_id in self.active_containers[container_index][0][:id_len]:
                    if selected_id not in self.selected_containers:
                        self.selected_containers.append(self.containers[container_index])
        return self.selected_containers
