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

- 取り組んだレベル：基礎
- やったこと：
  - agent.INSTRUCTIONSの「答えを書くな」の指示を削除 
  - agent.INSTRUCTIONSの「必ず search_glossary で用語集を確認する」の指示を削除
  - 本講座と関連のない単語を質問
- 結果：
  - agent.INSTRUCTIONSの「答えを書くな」の指示を削除
    - 問題とともに答えも出力する
  - agent.INSTRUCTIONSの「必ず search_glossary で用語集を確認する」の指示を削除 
    - 削除後も「xxとは」の質問に search_glossary を呼び出す
  - 本講座と関連のない単語を質問
    - 「生成AIとは」、「東京大学松尾研とは」には、用語集にはないことに触れた上で、 
      LLMの知識を元に回答する 
    - 「メロンとは」「東京大学とは」の質問には、「AIに関する質問をしろ」として. 
      LLMの知識を元にした回答はしない 
- 気づき・疑問：
  - 答えを出力しろとも指示していないのになぜ出力する？
  - 本講座と関連のない質問にLLMの知識から回答しないのは  
    agent.INSTRUCTIONSの「あなたはAIエンジニアリング講座（AIE2026）の学習支援エージェントです」  
    が効いているのだろう