# 第3回 解答

## 演習

- 第1回（素のLLM）とエージェントの回答の違い：
  - 第1回では具体的な内容は自分で確認しろと回答  
    今回が具体的なglossary.jsonの内容を元に回答された
- `--trace` で見えたツール呼び出し（ツール名と引数）：
  - [tool call]   search_glossary({'query': 'LoRA'})
  - [tool call]   search_glossary({'query': 'QLoRA'})
- 1つの質問での LLM 呼び出し回数（`requests`）：
  - requests=2
- 追加したツールと、docstring に書いた説明：
  - 追加したツール
    - tools.make_quiz
  - docstring に書いた説明
    - 指定した回の用語から 1つを選び、確認問題と答えを返す。  
      「第2回の確認問題を出して」のように、復習用の問題を求められたときに使う。

## 宿題

- 取り組んだレベル：発展
- やったこと：
  - ADKで作り直す
    - 宿題資料に従い __init__.py, agent.py を作成
      - ツールはAgent()の引数toolsで関数の配列として渡す
    - 宿題資料に従い uv run --with google-adk adk run ... を実行
- 結果：
  - コマンド実行の引数として質問を渡すのではなく、  
    [user]: プロンプトに対して入力する
  - [glossary_agent]: の後に回答が返る  
    回答の内容はPydantic AI で作るエージェントとほぼ同じ
- 気づき・疑問：
  - まず「第x回」と入力してその回の要点が返され、  
    続けて「用語は」と入力すると第x回の用語が返される
    - 文脈を保持している
