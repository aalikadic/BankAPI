# -*- coding: utf-8 -*-


import requests
import pytest

test_data= [
    ("Some", "Name", "2020-01-02", "Long St.", "123", "34567", "Chicago", "USA"),
    ("Some", "Other", "2020-03-02", "Short St.", "23", "4444", "Berlin", "Germany"),
    ("Name", "Name", "2020-07-02", "Middle St.", "123", "34167", "Istanbul", "Turkey"),
    ]
    
@pytest.mark.parametrize("FirstName, LastName, DateOfBirth, StreetName, HouseNumber, PostCode, City, Country" ,test_data)
def test_create_customer(FirstName, LastName, DateOfBirth, StreetName, HouseNumber, PostCode, City, Country, test_data):
    response = requests.post(f"http://127.0.0.1:8007/CreateCustomer/{FirstName}/{LastName}/{DateOfBirth}/{StreetName}/{HouseNumber}/{PostCode}/{City}/{Country}")
    assert response.status_code == 200
    
    
    
