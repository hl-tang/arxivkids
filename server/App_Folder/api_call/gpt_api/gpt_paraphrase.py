# 環境変数にAPIキーを設定
import os
from dotenv import load_dotenv
import openai
from pathlib import Path
import json
import time

load_dotenv(Path(__file__).parent.parent.joinpath(".env"))
openai.api_key = os.environ["OPENAI_API_KEY"]

# テキストを受け取って平易に言い換えたテキストを返す
def paraphrase(content):
  time_sta = time.time()
  schema = {
    "type": "object",
    "properties": {
      "plain_abstract": { "type": "string" }
    },
    "required": ["plain_abstract"]
  }
  prompt = """
           Task: Rephrase following abstract into plain text that even children can understand. in Japanese. The description should be approximately 200 Japanese characters.
           Format example:
           [
             {
               'keyword_title':"keyword_1_title",
               'keyword_description':"keyword_1_description
             },
            {
               'keyword_title':"keyword_2_title",
               'keyword_description':"keyword_2_description
             },
            {
               'keyword_title':"keyword_3_title",
               'keyword_description':"keyword_3_description
             }
            ,,,
            {
               'keyword_title':"keyword_n_title",
               'keyword_description':"keyword_n_description
             }           ]
           """\
          + content
          
  completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613",
    messages=[
      {"role": "system", "content": "You are a professional translator."},
      {"role": "user", "content": prompt}
    ],
    functions=[{"name": "set_plain_abstract", "parameters": schema}],
    function_call={"name": "set_plain_abstract"},
    temperature=0.5,
  )
  try:
    result = json.loads(completion.choices[0].message.function_call.arguments)
  except:
    print("error")
    result = "gpt error"
    print(completion.choices[0].message.function_call.arguments)
    
  time_end = time.time()
  # 経過時間（秒）
  tim = time_end- time_sta
  print(tim)
  # print(result)
  return(result["plain_abstract"])

# # Example Usage
Text = 'シーケンスの長さをスケーリングすることは、大規模言語モデルの時代において重要な要求となっている。\nしかし、既存の方法は、計算の複雑さとモデルの表現力のどちらか\n計算の複雑さとモデルの表現力のどちらにも苦戦しており、最大配列長\nを制限している。本研究では、Transformerの変種であるLongNetを紹介する。\nより短いシーケンスの性能を犠牲にすることなく、シーケンスの長さを10億トークン以上に拡張できる\nを導入する。具体的には、拡張注意（dilated attention）を提案する、\nこれは距離が長くなるにつれて、注意フィールドを指数関数的に拡大する。ロングネット\nには大きな利点がある：1)計算の複雑さは線形で、トークン間の依存関係は対数である。\nトークン間の依存性が対数である。\n3）その拡張された注意は、標準的な注意に取って代わることができる。\n標準的なアテンションとシームレスに統合できる。\n既存のTransformerベースの最適化とシームレスに統合できる。実験の結果\nLongNetは、長シーケンスモデリングと一般的な言語タスクの両方において強力な性能を発揮する。\n言語タスクの両方で強力な性能を発揮することが実証された。我々の研究は、非常に長いシーケンスのモデリングに新たな可能性を開く。\n例えば、コーパス全体やインターネット全体をシーケンスのように扱うことができる。'
print(paraphrase(Text))
