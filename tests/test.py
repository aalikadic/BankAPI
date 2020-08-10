# -*- coding: utf-8 -*-
"""

"""
import requests
import pytest

def test_home():
    response = requests.get("http://127.0.0.1:8007/")
    assert response.status_code == 200


