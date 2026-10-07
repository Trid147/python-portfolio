import pytest
from app import scanner

def test_regex():
    bad_line = "client = SlackClient(token='xoxb-12345678901-abcdefghijklmnopqrstuvwx')"
    result = scanner.scan_line(bad_line)
    assert result and result['type'] == 'Regex Match'

def test_entropy():
    bad_line = "secret_value = 'g6F9sK2mN5qQzXwY1vB9xZ2wK3lL5mN7pQ1rS'"
    result = scanner.scan_line(bad_line)
    assert result and result['type'] == 'High entropy'

def test_good_text():
    bad_line = 'Hello world!'
    result = scanner.scan_line(bad_line)
    assert result is None