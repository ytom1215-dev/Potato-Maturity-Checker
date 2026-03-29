import streamlit as st
import os
import random # ランダム機能を追加

# ==========================================
# 0. アプリの基本設定とカスタムCSS
# ==========================================
st.set_page_config(page_title="Potato Maturity Checker", page_icon="🥔", layout="centered")

st.markdown("""
    <style>
    .ref-table { font-size: 0.85em; color: #666; background: #fff; padding: 10px; border-radius: 5px; border: 1px solid #eee; margin-top: 15px; margin-bottom: 15px;}
    .feedback-box { padding: 15px; border-radius: 10px; margin-top: 15px; border-left: 8px solid; text-align: left; }
    .correct { background-color: #e8f8f1; border-left-color: #27ae60; color: #1e8449; }
    .near { background-color: #fef9e7; border-left-color: #f1c40f; color: #9a7d0a; }
    .incorrect { background-color: #fdedec; border-left-color: #e74c3c; color: #943126; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 1. 研修用データの設定 (全12枚のベースデータ)
# ==========================================
expert_data = [
    {"image_file": "p1.jpg", "true_score": 1, "explanation": "【指標 Ⅰ】黄変なし。葉は完全に緑色を呈しており、健全な状態です。"},
    {"image_file": "p2.jpg", "true_score": 2, "explanation": "【指標 Ⅱ】下葉がわずかに黄変。初期の生理的変化またはストレスサインです。"},
    {"image_file": "p3.jpg", "true_score": 3, "explanation": "【指標 Ⅲ】葉の約1/3が黄変。中程度の症状が認められます。"},
    {"image_file": "p4.jpg", "true_score": 4, "explanation": "【指標 Ⅳ】約2/3が黄変。光合成能力が大幅に低下しています。"},
    {"image_file": "p5.jpg", "true_score": 5, "explanation": "【指標 Ⅴ】株全体が黄変。生理的機能がほぼ停止しています。"},
    {"image_file": "p6.jpg", "true_score": 6, "explanation": "【指標 Ⅵ】地上部が枯死（枯凋）。植物体としての活動が終了した状態です。"},
    {"image_file": "p7.jpg", "true_score": 1, "explanation": "【指標 Ⅰ】黄変なし。葉は完全に緑色を呈しており、健全な状態です。"},
    {"image_file": "p8.jpg", "true_score": 2, "explanation": "【指標 Ⅱ】下葉がわずかに黄変。初期の生理的変化またはストレスサインです。"},
    {"image_file": "p9.jpg", "true_score": 3, "explanation": "【指標 Ⅲ】葉の約1/3が黄変。中程度の症状が認められます。"},
    {"image_file": "p10.jpg", "true_score": 4, "explanation": "【指標 Ⅳ】約2/3が黄変。光合成能力が大幅に低下しています。"},
    {"image_file": "p11.jpg", "true_score": 5, "explanation": "【指標 Ⅴ】株全体が黄変。生理的機能がほぼ停止しています。"},
    {"image_file": "p12.jpg", "true_score": 6, "explanation": "【指標 Ⅵ】地上部が枯死（枯凋）。植物体としての活動が終了した状態です。"}
]

total_q = len(expert_data)
romans = ["Ⅰ", "Ⅱ", "Ⅲ", "Ⅳ", "Ⅴ", "Ⅵ"]
score_map = {"Ⅰ": 1, "Ⅱ": 2, "Ⅲ": 3, "Ⅳ": 4, "Ⅴ": 5, "Ⅵ": 6}

# ==========================================
# 2. セッションステート初期化（ここでランダム化！）
# ==========================================
if 'current_idx' not in st.session_state:
    st.session_state.current_idx = 0
    st.session_state.has_answered = False
    st.session_state.correct_count = 0
    st.session_state.finished = False
    st.session_state.user_score_val = 1
    
    # 初回起動時にリストをシャッフルして記憶させる
    shuffled = expert_data.copy()
    random.shuffle(shuffled)
    st.session_state.shuffled_data = shuffled

# ==========================================
# 3. UIの構築
# ==========================================
st.title("🥔 Potato Maturity Checker")
st.markdown("---")

if not st.session_state.finished:
    st.markdown(f"### 画像: {st.session_state.current_idx + 1} / {total_q}")
    
    # ★ここから下は、シャッフルされたデータ（shuffled_data）を使います
    current_data = st.session_state.shuffled_data[st.session_state.current_idx]
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    img_filename = current_data["image_file"]
    img_path = os.path.join(current_dir, img_filename)

    if os.path.exists(img_path):
        st.image(img_path, width=350)
    else:
        st.warning(f"画像が見つかりません: {img_filename} を配置してください。")

    user_choice = st.radio(
        "判定スコアを選択:", 
        options=list(score_map.keys()),
        horizontal=True,
        disabled=st.session_state.has_answered,
        key=f"q_{st.session_state.current_idx}"
    )
    
    if not st.session_state.has_answered:
        if st.button("判定を確定する", type="primary", use_container_width=True):
            st.session_state.user_score_val = score_map[user_choice]
            true_val = current_data["true_score"]
            if st.session_state.user_score_val == true_val:
                st.session_state.correct_count += 1
            st.session_state.has_answered = True
            st.rerun()
    
    else:
        true_val = current_data["true_score"]
        diff = abs(st.session_state.user_score_val - true_val)
        
        if diff == 0:
            status_class, res_msg = "correct", "✅ 正解！"
        elif diff == 1:
            status_class, res_msg = "near", "⚠️ 惜しい（1段ズレ）"
        else:
            status_class, res_msg = "incorrect", "❌ 不正解"
            
        explanation = current_data["explanation"]
        
        st.markdown(f"""
        <div class="feedback-box {status_class}">
            <h3 style="margin-top:0;">{res_msg}</h3>
            <p><b>熟練者の判定:</b> {romans[true_val - 1]}</p>
            <p><b>リファレンス解説:</b> {explanation}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        btn_label = "次の画像へ" if st.session_state.current_idx < total_q - 1 else "最終結果を見る"
        if st.button(btn_label, type="secondary", use_container_width=True):
            if st.session_state.current_idx < total_q - 1:
                st.session_state.current_idx += 1
                st.session_state.has_answered = False
            else:
                st.session_state.finished = True
            st.rerun()

    st.markdown("""
    <div class="ref-table">
        <b>【リファレンス指標】</b><br>
        Ⅰ: 黄変なし / Ⅱ: 下葉わずか / Ⅲ: 約1/3黄変 / Ⅳ: 約2/3黄変 / Ⅴ: 株全体黄変 / Ⅵ: 地上部枯死
    </div>
    """, unsafe_allow_html=True)

else:
    perc = round((st.session_state.correct_count / total_q) * 100, 1)
    st.markdown(f"""
    <div style="text-align:center; padding:30px; background:white; border-radius:15px; border:1px solid #ddd;">
        <h2>🏆 研修終了！お疲れ様でした</h2>
        <hr>
        <h3>正解数: {st.session_state.correct_count} / {total_q}</h3>
        <h3>正解率: {perc} %</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("もう一度受ける", type="primary", use_container_width=True):
        st.session_state.current_idx = 0
        st.session_state.has_answered = False
        st.session_state.correct_count = 0
        st.session_state.finished = False
        
        # もう一度受けるときに、再びシャッフルし直す！
        shuffled = expert_data.copy()
        random.shuffle(shuffled)
        st.session_state.shuffled_data = shuffled
        
        st.rerun()
