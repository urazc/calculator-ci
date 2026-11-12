import pytest
import math

from calculator import add, subtract, multiply, divide, sin, tangent, square_area, triangle_area, pow_, CircleArea


def test_add():
    assert add(2, 3) == 5


def test_subtract():
    assert subtract(8, 3) == 5


def test_multiply():
    assert multiply(3, 4) == 12


def test_divide():
    assert divide(6, 2) == 3


def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(6, 0)

def test_sin_zero():
    assert sin(0) == pytest.approx(0)


def test_sin_pi_over_two():
    assert sin(math.pi / 2) == pytest.approx(1)


def test_sin_pi():
    assert sin(math.pi) == pytest.approx(0)


def test_sin_negative():
    assert sin(-math.pi / 2) == pytest.approx(-1)
    
def test_tangent_zero():
    assert tangent(0) == pytest.approx(0.0)


def test_tangent_45_degrees():
    angle = math.pi / 4  # 45 degrees in radians
    assert tangent(angle) == pytest.approx(1.0)
    
def test_square_area():
    assert square_area(4) == 16

def test_triangle_area():
    assert triangle_area(4,8) == 16
    
def test_pow():
    assert pow_(2,3) == 8

def test_CircleArea():
    assert CircleArea(-4) == "Error" 
