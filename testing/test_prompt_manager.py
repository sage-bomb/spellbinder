from llm.prompt_manager import PromptManager


def test_prompt_manager_basic():
    print("🧪 Running PromptManager test...")

    pm = PromptManager(use_db=True)

    # Direct chat test
    direct_response = pm.chat("What does a lantern represent in mourning rituals?")
    assert isinstance(direct_response, str) and len(direct_response) > 0
    print("✅ Direct chat passed.")

    # Template prompt test
    template_response = pm.run_template(
        name="Voxa.SassyComment",
        variables={"input": "I think magic is overrated."},
        metadata={"test": "true", "origin": "test_prompt_manager_basic"}
    )
    assert isinstance(template_response, str) and len(template_response) > 0
    print("✅ Template prompt passed.")

    print("🎉 PromptManager test complete.\n")



from llm.model_resolver import ModelResolver

def test_model_resolver():
    print("🧪 Running ModelResolver tests...")

    resolver = ModelResolver()

    all_models = resolver.list_models()
    assert isinstance(all_models, list) and len(all_models) > 0, "❌ Failed to fetch model list"

    test_cases = [
        "gpt-4",
        "gpt-3.5-turbo",
        "gpt-4:latest",
        "gpt-3.5:stable",
        "gpt-4:preview",
        "gpt-9999",  # nonsense fallback test
        None
    ]

    for case in test_cases:
        resolved = resolver.resolve(case)
        print(f"🔎 {case or '<default>'} → {resolved}")
        assert resolved in all_models, f"❌ Resolved model '{resolved}' not in available models"

    print("✅ ModelResolver passed all cases.\n")


if __name__ == "__main__":
    test_model_resolver()
    #test_prompt_manager_basic()
