# Direct-mode unit tests for WhitepaperRate.  Run: pytest tests/direct/ -v
import json

CONTRACT = "contracts/whitepaperrate.py"


def test_submit_and_evaluate(direct_vm, direct_deploy, direct_alice):
    c = direct_deploy(CONTRACT)
    direct_vm.sender = direct_alice
    idx = c.submit("https://example.com/x")
    assert int(idx) == 0
    direct_vm.mock_web(r".*example\.com.*", {"status": 200, "body": "example page content"})
    direct_vm.mock_llm(r".*JSON.*", json.dumps({"label": "solid", "score": 80, "reasoning": "ok"}))
    c.evaluate(0)
    item = c.get_item(0)
    assert item["label"] == "solid"
    assert bool(item["done"]) is True


def test_evaluate_rejects_invalid_id(direct_vm, direct_deploy, direct_alice):
    c = direct_deploy(CONTRACT)
    direct_vm.sender = direct_alice
    with direct_vm.expect_revert("invalid item id"):
        c.evaluate(0)
