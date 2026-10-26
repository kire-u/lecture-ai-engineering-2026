"""第1回: 素のLLMに質問するスクリプト。

使い方:
    uv run python -m app.ask "LoRAとは何ですか？"
    uv run python -m app.ask --temperature 0.7 "LoRAとは何ですか？"
    uv run python -m app.ask --interactive
    uv run python -m app.ask            # 質問を省略すると、講座に固有の質問をする

ツールも会話履歴も持たない「素の」呼び出し。
講座に固有のことを聞くと、「分からない」と答えるか、一般論でもっともらしく答える
（講座の実際とは違う）ことを確かめよう。
（第3回で、用語集を検索できるエージェントにして改善する）
"""

import argparse

from google import genai
from google.genai.chats import Chat
from google.genai import errors
from google.genai import types

from app.config import MODEL, api_error_message, get_api_key

# 講座に固有の質問。正しい答えは data/glossary.json の homework-levels にある
DEFAULT_QUESTION = "AIE2026の講座の宿題にある「3レベル」とは何ですか？"


def ask(question: str, temperature: float | None = None) -> str:
    client = genai.Client(api_key=get_api_key())
    config = types.GenerateContentConfig(temperature=temperature) if temperature is not None else None
    response = client.models.generate_content(
        model=MODEL,
        contents=question,
        **({"config": config} if config is not None else {}),
    )

    _print_usage(response)

    return response.text


def chat(question: str | None = None, temperature: float | None = None) -> None:
    """複数の質問を同じチャットセッションに送り、会話履歴を維持する。"""
    client = genai.Client(api_key=get_api_key())
    config = types.GenerateContentConfig(temperature=temperature) if temperature is not None else None
    session = client.chats.create(
        model=MODEL,
        **({"config": config} if config is not None else {}),
    )

    if question:
        _send_message(session, question)

    print("会話を開始します。終了するには exit または quit を入力してください。")
    while True:
        try:
            message = input("\nあなた> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if message.casefold() in {"exit", "quit"}:
            break
        if message:
            _send_message(session, message)


def _send_message(session: Chat, message: str) -> None:
    response = session.send_message(message)
    _print_usage(response)
    print(f"AI> {response.text}")


def _print_usage(response) -> None:
    usage = response.usage_metadata
    if usage is not None:
        print(
            "[トークン] "
            f"入力: {usage.prompt_token_count or 0} / "
            f"出力: {usage.candidates_token_count or 0}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="素のLLMに質問する")
    parser.add_argument("question", nargs="?")
    parser.add_argument("--temperature", type=float, help="生成時の temperature を指定する")
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="会話履歴を保ちながら続けて質問する",
    )
    args = parser.parse_args()

    print(f"[model] {MODEL}")
    if args.temperature is not None:
        print(f"[temperature] {args.temperature}")
    try:
        if args.interactive:
            chat(args.question, temperature=args.temperature)
        else:
            question = args.question or DEFAULT_QUESTION
            print(f"[質問] {question}\n")
            print(ask(question, temperature=args.temperature))
    except errors.APIError as e:
        print(api_error_message(e.code, e.message))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
