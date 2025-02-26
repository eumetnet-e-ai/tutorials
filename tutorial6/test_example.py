# content of test_example.py

def add(a, b):
    return a + b

def test_answer():
    assert add(1, 3) == 5

#####################################

def test_answer_correctly():
    assert add(1, 3) == 4

def test_demo_with_message():
    val = 5 + 3
    assert val % 2 == 0, "even value expected"

import pytest
def test_zero_division():
    with pytest.raises(ZeroDivisionError):
        1 / 0

#####################################

import torch
def some_f():
    return torch.Tensor([3.14])

def test_torch():
    val = some_f()
    torch.testing.assert_close(
        actual=val,
        expected=torch.Tensor([torch.pi]),
        atol=0.002,
        rtol=0.0000001,
    )

#####################################

class TestClass:
    def test_one(self):
        x = "this"
        assert "h" in x

    def test_two(self):
        x = "hello"
        assert hasattr(x, "check")

#####################################

class TestClassDemoInstance:
    value = 0
    def test_one(self):
        self.value = 1
        assert self.value == 1

    def test_two(self):
        assert self.value == 0

#####################################

import pytest

@pytest.fixture
def simple_data():
    return [42]

def test_simple_data(simple_data):
    assert simple_data[0] == 42
    assert len(simple_data) == 1

def test_two(simple_data):
    simple_data.append(23)
    assert sum(simple_data) == 65

#####################################

@pytest.mark.parametrize("n,expected", [(1, 2), (3, 4)])
class TestClass:
    def test_simple_case(self, n, expected):
        assert n + 1 == expected

    def test_weird_simple_case(self, n, expected):
        assert (n * 1) + 1 == expected

#####################################

import xarray, numpy

def my_processing(filename):
    data = xarray.open_dataset(filename)
    # some processing
    return data

def open_dataset_mock(*kwargs, **args):
    return xarray.Dataset({"X": numpy.arange(5)})

def test_processing(monkeypatch):
    monkeypatch.setattr(xarray, "open_dataset", open_dataset_mock)
    x = my_processing("no-name.nc")
    assert x.X.sum() == 10