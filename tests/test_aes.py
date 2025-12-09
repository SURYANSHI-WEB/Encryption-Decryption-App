import pytest


@pytest.mark.skip(reason="AES support removed per user request")
def test_aes_removed():
    assert True


