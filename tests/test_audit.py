from x4_beast.audit import AuditStore

def test_fingerprint_is_stable():
    a = AuditStore("/tmp/x4-test.jsonl")
    assert a.fingerprint({"a": 1}) == a.fingerprint({"a": 1})
    assert a.fingerprint({"a": 1}) != a.fingerprint({"a": 2})
