from buyermoment.api import demo, experiment


def test_demo_and_experiment_flow():
    payload = demo()
    business_id = payload["businesses"][0]["id"]
    moment_id = payload["moments"][business_id][0]["id"]
    generated = experiment({"business_id": business_id, "buyer_moment_id": moment_id})
    assert generated.channel == "chatgpt_ads"
    assert generated.disclaimer.startswith("Hypothesis")
