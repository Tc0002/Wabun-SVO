import json
import os

class SVOProcessor:
    def __init__(self, config_path="../configs/mapping.json"):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        # 高速化のため、置換用辞書をマージ
        self.rules = {**self.config['particles'], **self.config['verbs']}

    def encode(self, text):
        # 簡易的な置換（本来は形態素解析で語順制御を行うが、まずはここから）
        processed = text
        for k, v in self.rules.items():
            processed = processed.replace(k, v)
        # 文末処理
        if not processed.endswith(self.config['structure']['terminator']):
            processed += self.config['structure']['terminator']
        return processed

    def decode(self, text):
        # 逆変換（Viewer用）
        reversed_rules = {v: k for k, v in self.rules.items()}
        processed = text
        for k, v in reversed_rules.items():
            processed = processed.replace(k, v)
        return processed

if __name__ == "__main__":
    # 動作テスト用
    proc = SVOProcessor(os.path.join(os.path.dirname(__file__), '../configs/mapping.json'))
    sample = "私はAIを開発する。"
    encoded = proc.encode(sample)
    print(f"Original: {sample}")
    print(f"Encoded : {encoded}")