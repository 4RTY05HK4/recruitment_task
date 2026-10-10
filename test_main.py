from main import HelloWorld


class TestClass:
    def test_HelloWorld(self):
        result = HelloWorld()
        assert result == "Hello World!"
