import pytest
from specklepy.api import operations
from specklepy.api.client import SpeckleClient
from specklepy.objects.base import Base
from specklepy.transports.server import ServerTransport
from specklepy.api.credentials import Account, get_account_from_token
from specklepy.logging.exceptions import SpeckleException, SpeckleWarning


def test_invalid_authentication():
    client = SpeckleClient()

    with pytest.warns(SpeckleWarning):
        client.authenticate_with_token("fake token")


def test_invalid_send():
    client = SpeckleClient()
    client.account = Account(token="fake_token")
    transport = ServerTransport("3073b96e86", client)

    with pytest.raises(SpeckleException):
        operations.send(Base(), [transport])


def test_invalid_receive():
    client = SpeckleClient()
    client.account = Account(token="fake_token")
    transport = ServerTransport("fake stream", client)

    with pytest.raises(SpeckleException):
        operations.receive("fake object", transport)


def test_account_from_token():
    token = "fake token"
    acct = get_account_from_token(token)

    assert acct.token == token


def test_account_from_token_and_url():
    token = "fake token"
    url = "fake.server"
    acct = get_account_from_token(token, url)

    assert acct.token == token
    assert acct.serverInfo.url == url