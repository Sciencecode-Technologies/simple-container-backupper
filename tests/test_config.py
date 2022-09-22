""" package tests"""
from conback.core import ConbackCore
import pytest


@pytest.mark.len
def test_id_len():
    assert ConbackCore().config['General']['id_len'] == 4


@pytest.mark.len
def test_name_len():
    assert ConbackCore().config['General']['name_len'] == 16
