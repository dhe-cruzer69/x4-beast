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

def test_level_0_observe_only():
    policy = PolicyEngine(autonomy_level=0)
    policy.register_read_only("read_file")
    assert policy.decide("read_file").action == "allow"
    assert policy.decide("write_file").action == "deny"

def test_autofix_respects_level_and_flag():
    # Autofix disabled
    policy = PolicyEngine(autonomy_level=2, autofix_enabled=False)
    assert policy.decide("autofix_patch").action == "deny"

    # Level too low
    policy = PolicyEngine(autonomy_level=1, autofix_enabled=True)
    assert policy.decide("autofix_patch").action == "approval"

    # Level 2 + enabled → still needs approval unless token supplied
    policy = PolicyEngine(autonomy_level=2, autofix_enabled=True)
    assert policy.decide("autofix_patch").action == "approval"
    assert policy.decide("autofix_patch", approval="token").action == "allow"
