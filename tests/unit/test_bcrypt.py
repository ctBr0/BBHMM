import pytest

# Using relative path
from utils.bcrypt_helper import hash_password, check_password # type: ignore

@pytest.mark.unit
@pytest.mark.parametrize("input_password, output_password", [
    ("euoiwrghxueiwxhg", "euoiwrghxueiwxhg"),    # First test case
    ("120347981347", "120347981347"),   # Second test case
    (";.[];.;/;.,';;].", ";.[];.;/;.,';;]."),
    ("       ", "       "),
    ("asdfasdf12341234", "asdfasdf12341234"),
    ("43298 uh sidjqh-;,;'c.z[]", "43298 uh sidjqh-;,;'c.z[]")
])
def test_true_encrpyt_decrpyt(input_password, output_password):
  assert check_password(output_password, hash_password(input_password)) == True

@pytest.mark.unit
@pytest.mark.parametrize("input_password, output_password", [
    ("euoiwrghxueiwxhg", "euoiwrghxueiw"),
    ("120347981", "120347981347"),
    (";.[];     ';;].", ";.[];.;/;.,';;]."),
    ("       ", "    "),
    ("asdfasdf12341234", "asdfa41234"),
    ("43298 uh si2ufdg.'//djqh-;,;'c.z[]", "43298 uh sidjqh-;,;'c.z[]")
])
def test_false_encrpyt_decrpyt(input_password, output_password):
  assert check_password(output_password, hash_password(input_password)) == False
