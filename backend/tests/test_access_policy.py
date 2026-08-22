from core.access_policy import AccessPolicyManager
import urllib.robotparser

def test_access_policy_allowed():
    # Verify that default allowed rules respond with True
    assert AccessPolicyManager.is_allowed("https://gov.in/news") is True
