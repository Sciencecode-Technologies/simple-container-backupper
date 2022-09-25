""" package tests"""
from conback.core import ConbackCore
import pytest


@pytest.mark.length
def test_id_len():
    assert ConbackCore().config['General']['id_len'] == 4

@pytest.mark.length
def test_name_len():
    assert ConbackCore().config['General']['name_len'] == 16

@pytest.mark.container_selection
def test_list_containers():
    active_containers = ConbackCore().list_active_containers()

    assert type(active_containers) == list
