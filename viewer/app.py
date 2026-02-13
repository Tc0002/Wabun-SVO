import streamlit as st
import os
import sys

# プロセッサをインポート可能にする
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.svo_processor import SVOProcessor

st.set_page_config(page_title="Wabun-SVO Engine Viewer", layout="wide")

st.title("🚀 Wabun-SVO High-Density Engine")
st.caption("v1.1 - Token Compression & Logical SVO Structuring")

# 初期化
config_p = os.path.abspath(os.path.join(os.path.dirname(__file__), '../configs/mapping.json'))
proc = SVOProcessor(config_p)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Input (Natural Japanese)")
    input_text = st.text_area("日本語を入力してください", "私は高性能なAIを開発している。これは重要な課題である。", height=200)
    
    if st.button("Encode ⚡"):
        encoded = proc.encode(input_text)
        st.session_state.encoded = encoded

with col2:
    st.subheader("Output (Wabun-SVO)")
    if 'encoded' in st.session_state:
        st.code(st.session_state.encoded, language="text")
        
        # 簡易メトリクス表示
        orig_len = len(input_text)
        enc_len = len(st.session_state.encoded)
        reduction = (1 - enc_len / orig_len) * 100
        
        st.metric("Character Reduction", f"{enc_len} chars", f"-{reduction:.1f}%")
        st.info("💡 LLMはこのSVO構造を『英語の論理』として高速に処理します。")

st.divider()

st.subheader("Reverse Lookup (Decode Test)")
decode_input = st.text_input("SVO形式の文章を入れて復元テスト", st.session_state.get('encoded', ""))
if decode_input:
    st.success(f"Decoded: {proc.decode(decode_input)}")