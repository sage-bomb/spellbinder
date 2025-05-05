from llm.prompt_manager import PromptManager
from llm.prompt_templates import PROMPT_TEMPLATES

def test_prompt_cost_tracking():
    print("\n🧪 Testing prompt cost tracking...")

    pm = PromptManager()
    template_name = "Voxa.SassyComment"

    assert template_name in PROMPT_TEMPLATES
    configured_model = PROMPT_TEMPLATES[template_name]["model"]
    print(f"📄 Template requests model: {configured_model}")

    metadata = {
        "test": "costs",
        "allow_expensive": True  # let Voxa go wild
    }

    response = pm.run_template(
        name=template_name,
        variables={"input": "Tell me why AI won't cook my dinner."},
        metadata=metadata
    )

    print(f"\n🗯 Voxa's reply:\n{response.strip()}\n")

    records = pm.db.all()
    assert records, "❌ No records found in DB."
    latest = records[-1]

    usage = latest.get("usage", {})
    cost = latest.get("estimated_cost")

    assert usage, "❌ Missing usage data."
    assert cost is not None, "❌ Missing cost estimate."

    print(f"💬 Token usage: {usage}")
    print(f"💰 Estimated cost: ${cost:.4f}")
    print(f"✅ Prompt tracking and cost estimation successful.")


if __name__ == "__main__":
    test_prompt_cost_tracking()
