# -*- coding: utf-8 -*-
import requests
import pytest

test_data = [(1),(2)]


def test_create_customer():
    response = requests.get(f"http://127.0.0.1:8007/GetCustomerBalance/1")
    assert response.status_code == 200