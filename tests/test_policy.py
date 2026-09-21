from x4_beast.policy import PolicyEngine

def test_unknown_tool_is_denied():
    policy = PolicyEngine()
    assert policy.decide("unknown_tool").action == "deny"

def test_registered_read_only_tool_is_allowed():
    policy = PolicyEngine()
    policy.register_read_only("repository_summary")
    assert policy.decide("repository_summary").action == "allow"

def test_network_tool_requires_approval():
    policy = PolicyEngine()
    assert policy.decide("http_request").action == "approval"
