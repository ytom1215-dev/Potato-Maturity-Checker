import streamlit as st
import os

# ==========================================
# 0. アプリの基本設定とカスタムCSS
# ==========================================
st.set_page_config(page_title="ジャガイモ黄化度判定トレーニング", page_icon="🥔", layout="centered")

st.markdown("""
    <style>
    .ref-table { font-size: 0.85em; color: #666; background: #fff; padding: 10px; border-radius: 5px; border: 1px solid #eee; margin-top: 15px; margin-bottom: 15px;}
    .feedback-box { padding: 15px; border-radius: 10px; margin-top: 15px; border-left: 8px solid; text-align: left; }
    .correct { background-color: #e8f8f1; border-left-color: #27ae60; color: #1e8449; }
    .near { background-color: #fef9e7; border-left-color: #f1c40f; color: #9a7d0a; }
    .incorrect { background-color: #fdedec; border-left-color: #e74c3c; color: #943126; }
    </style>
""", unsafe_allow_html=True)

# Streamlitのバージョン差異吸収関数
def safe_rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()

# ==========================================
# 1. 研修用データの設定 (全12枚)
# ==========================================
expert_data =[
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
# 2. セッションステート初期化
# ==========================================
if 'current_idx' not in st.session_state:
    st.session_state.current_idx = 0
    st.session_state.has_answered = False
    st.session_state.correct_count = 0
    st.session_state.finished = False
    st.session_state.user_score_val = 1

# ==========================================
# 3. UIの構築 (Web・スマホ向けの縦並びレイアウト)
# ==========================================
st.title("🥔 ジャガイモ黄化度判定研修")
st.markdown("---")

if not st.session_state.finished:
    st.markdown(f"### 画像: {st.session_state.current_idx + 1} / {total_q}")
    
    # 画像の読み込みと表示（強制的に横幅を350pxに制限して小さく表示）
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        current_dir = os.getcwd()
        
    img_filename = expert_data[st.session_state.current_idx]["image_file"]
    img_path = os.path.join(current_dir, img_filename)

    if os.path.exists(img_path):
        st.image(img_path, width=350)
    else:
        st.warning(f"画像が見つかりません: {img_filename} を同じフォルダに配置してください。")
        # 画像がない場合でもテストできるようにダミー画像を表示します
        st.image(f"https://placehold.co/350x250/eeeeee/999999?text=Image+{st.session_state.current_idx + 1}", width=350)

    # ユーザー入力
    user_choice = st.radio(
        "判定スコアを選択:", 
        options=list(score_map.keys()),
        horizontal=True,
        disabled=st.session_state.has_answered,
        key=f"q_{st.session_state.current_idx}"
    )
    
    # 判定ボタン
    if not st.session_state.has_answered:
        if st.button("判定を確定する", type="primary", use_container_width=True):
            st.session_state.user_score_val = score_map[user_choice]
            true_val = expert_data[st.session_state.current_idx]["true_score"]
            if st.session_state.user_score_val == true_val:
                st.session_state.correct_count += 1
            st.session_state.has_answered = True
            safe_rerun()
    
    # 次へボタンとフィードバック
    else:
        true_val = expert_data[st.session_state.current_idx]["true_score"]
        diff = abs(st.session_state.user_score_val - true_val)
        
        if diff == 0:
            status_class, res_msg = "correct", "✅ 正解！"
        elif diff == 1:
            status_class, res_msg = "near", "⚠️ 惜しい（1段ズレ）"
        else:
            status_class, res_msg = "incorrect", "❌ 不正解"
            
        explanation = expert_data[st.session_state.current_idx]["explanation"]
        
        st.markdown(f"""
        <div class="feedback-box {status_class}">
            <h3 style="margin-top:0;">{res_msg}</h3>
            <p><b>あなたの判定:</b> {romans[st.session_state.user_score_val - 1]}</p>
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
            safe_rerun()

    # リファレンス表示
    st.markdown("""
    <div class="ref-table">
        <b>【リファレンス指標】</b><br>
        Ⅰ: 黄変なし / Ⅱ: 下葉わずか / Ⅲ: 約1/3黄変 / Ⅳ: 約2/3黄変 / Ⅴ: 株全体黄変 / Ⅵ: 地上部枯死
    </div>
    """, unsafe_allow_html=True)

else:
    # 最終結果表示
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
        
        # セッションに残っている過去の選択状態(q_0 ~ q_11)をクリアする
        for key in list(st.session_state.keys()):
            if key.startswith("q_"):
                del st.session_state[key]
                
        safe_rerun()
