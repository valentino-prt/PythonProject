from hello_world.main import greet


def test_greet():
    msg = greet("Test")
    assert "Hello" in msg
    assert "Test" in msg
