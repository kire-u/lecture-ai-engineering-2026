from types import SimpleNamespace

from app import ask as ask_module


def test_ask_passes_temperature_to_generation_config(monkeypatch):
    calls = {}

    class FakeModels:
        def generate_content(self, **kwargs):
            calls.update(kwargs)
            return SimpleNamespace(usage_metadata=None, text="answer")

    class FakeClient:
        models = FakeModels()

    monkeypatch.setattr(ask_module.genai, "Client", lambda **_: FakeClient())
    monkeypatch.setattr(ask_module, "get_api_key", lambda: "test-key")

    assert ask_module.ask("question", temperature=0.7) == "answer"
    assert calls["config"].temperature == 0.7


def test_ask_omits_config_when_temperature_is_not_set(monkeypatch):
    calls = {}

    class FakeModels:
        def generate_content(self, **kwargs):
            calls.update(kwargs)
            return SimpleNamespace(usage_metadata=None, text="answer")

    class FakeClient:
        models = FakeModels()

    monkeypatch.setattr(ask_module.genai, "Client", lambda **_: FakeClient())
    monkeypatch.setattr(ask_module, "get_api_key", lambda: "test-key")

    assert ask_module.ask("question") == "answer"
    assert "config" not in calls


def test_main_passes_temperature_option(monkeypatch, capsys):
    received = {}

    def fake_ask(question, temperature=None):
        received["question"] = question
        received["temperature"] = temperature
        return "answer"

    monkeypatch.setattr(ask_module, "ask", fake_ask)
    monkeypatch.setattr(
        "sys.argv",
        ["app.ask", "--temperature", "0.4", "question"],
    )

    ask_module.main()

    assert received == {"question": "question", "temperature": 0.4}
    assert "[temperature] 0.4" in capsys.readouterr().out
