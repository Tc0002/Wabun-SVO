import json
import os

class SVOProcessor:
    def __init__(self, config_path="../configs/mapping.json"):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        # 置換ルールを優先順位（文字列の長さ）順に整理
        # 長いもの（"である"等）を先に置換しないと、一文字の助詞（"で"）に食われるため
        all_rules = {
            **self.config['particles'], 
            **self.config['conjugations'], 
            **self.config['verbs_core']
        }
        self.sorted_rules = dict(sorted(all_rules.items(), key=lambda x: len(x[0]), reverse=True))

    def encode(self, text):
        processed = text
        for k, v in self.sorted_rules.items():
            processed = processed.replace(k, v)
        
        # 文末処理
        processed = processed.replace("。", self.config['structure']['terminator'])
        if not processed.endswith(self.config['structure']['terminator']):
            processed += self.config['structure']['terminator']
        return processed

    def decode(self, text):
        reversed_rules = {v: k for k, v in self.sorted_rules.items()}
        # 逆変換も同様に長い記号から
        sorted_rev = dict(sorted(reversed_rules.items(), key=lambda x: len(x[0]), reverse=True))
        
        processed = text
        for k, v in sorted_rev.items():
            processed = processed.replace(k, v)
        
        processed = processed.replace(self.config['structure']['terminator'], "。")
        return processed

if __name__ == "__main__":
    # パス解決を柔軟に
    base_dir = os.path.dirname(__file__)
    config_p = os.path.abspath(os.path.join(base_dir, '../configs/mapping.json'))
    
    proc = SVOProcessor(config_p)
    sample = "私はAIを開発できる。"
    encoded = proc.encode(sample)
    print(f"Original: {sample}")
    print(f"Encoded : {encoded}")
    print(f"Decoded : {proc.decode(encoded)}")