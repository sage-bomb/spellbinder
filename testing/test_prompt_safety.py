from llm.prompt_manager import PromptManager
from llm.prompt_templates import PROMPT_TEMPLATES

def test_prompt_model_blocking():
    print("🧪 Testing model fallback logic for blocked expensive models...")

    metadata = {
        "test": "safety",
        "allow_expensive": False  # or False
    }
    pm = PromptManager()
    template_name = "Voxa.SassyComment"

    assert template_name in PROMPT_TEMPLATES
    configured_model = PROMPT_TEMPLATES[template_name]["model"]
    print(f"📄 Template requests model: {configured_model}")

    # Run template WITHOUT allowing expensive models
    response = pm.run_template(
        name=template_name,
        variables={"input": "OpenAI should cook my dinner."},
        metadata=metadata
    )

    assert isinstance(response, str) and len(response.strip()) > 0
    print(f"\n🗯 Voxa's reply:\n{response.strip()}\n")

    # Confirm model used was NOT an expensive one
    records = pm.db.all()  # or pm.db.list_all(), depending on your version
    assert records, "❌ No prompt records found in DB."
    used_model = records[-1]["model"]
    # Determine intent
    allow_expensive = metadata.get("allow_expensive", False)

    if allow_expensive:
        assert used_model.startswith("gpt-4"), f"❌ Expected expensive model, got: {used_model}"
        print(f"✅ Expensive model used as allowed: {used_model}")
    else:
        assert not used_model.startswith("gpt-4"), f"❌ Blocked model used despite restriction: {used_model}"
        print(f"✅ Expensive model was blocked correctly. Used: {used_model}")


if __name__ == "__main__":
    test_prompt_model_blocking()
