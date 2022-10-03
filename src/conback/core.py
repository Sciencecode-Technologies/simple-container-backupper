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
        self.active_containers: list = []
        self.images: list = []
        self.selected_containers: list = []
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
        for container_index in range(active_container_data['ac_len']):
            # MYPY->No overload variant of "range" matches argument type object
            for selected_id in selections.split(' '):
                if selected_id in self.active_containers[container_index][0][:id_len]:
                    if selected_id not in self.selected_containers:
                        self.selected_containers.append(self.containers[container_index])
        return self.selected_containers

    def export_filesystem(self, container_names: list, make_tar: bool = True):
        """
        returns: list
        attributes:
            - container_name: list
            - make_tar: bool

        Exports selected containers filesystem.
        """
        exported: list = []
        for ac_i in range(len(self.active_containers)):
            # get file path
            if container_names in self.__docker_client.containers.list()[ac_i].names:
                if make_tar:
                    with open(self.active_containers[ac_i][1]+".tar", "wb", encoding="UTF-8") as tarfile:
                        for chunk in self.__docker_client.containers.list()[ac_i].export():
                            tarfile.write(chunk)
                        exported.append(self.containers[ac_i][1])
        return exported

    def create_backup(self):
        """
        returns: list
        attributes:
        """
        committed: list = []
        for container in self.select_containers:
            committed.append(container.commit(repository=container.name, tag=self.config['Commit']['tag']))
        if not len(committed) > 0:
            return committed
        else:
            return False

    def save_backups(self, rmi: bool = True):
        """
        exports backups
        Keyword arguments:
        rmi: bool --
        Return: list
        """
        __s, __c = False, -1
        committeds: list = self.create_backup()
        committeds_status = [False for i in range(len(committeds))]
        for backup_img in committeds:
            with open(backup_img.tags[0].split(':')[0]+".tar", "wb") as tarfile:
                __c = __c+1
                for chunk in backup_img.save():
                    if tarfile.write(chunk):
                        __s = True
            committeds_status[__c] = __s
            if rmi:
                backup_img.remove()
        return committeds_status
