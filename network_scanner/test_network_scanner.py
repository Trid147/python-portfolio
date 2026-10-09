import pytest
from network_scanner.network_scanner import check_port

@pytest.mark.asyncio
async def test_port_github():
    host = 'github.com'
    result = await check_port(host, 53)
    assert result == (53, False)