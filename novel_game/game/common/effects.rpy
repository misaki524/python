## engine/effects.rpy — 汎用ビジュアルエフェクト
##
## 他プロジェクトでも再利用可能な画面演出エフェクト集。
## 使用例:
##   show screen flash_effect("#ffffff", 0.1, 0.05)
##   show screen color_overlay("#ff0000", 0.15, 0.08)
##   show screen blackout_effect(0.5)

# ============================================================
# 汎用フラッシュエフェクト
# ============================================================
# 任意の色・透明度・持続時間でフラッシュを表示する。
#
# 引数:
#   flash_color (str): フラッシュの色 (例: "#ffffff")
#   flash_alpha (float): 透明度 0.0〜1.0
#   flash_duration (float): 表示秒数

screen flash_effect(flash_color="#ffffff", flash_alpha=0.1, flash_duration=0.05):
    zorder 150
    add Solid(flash_color) alpha flash_alpha
    timer flash_duration action Hide("flash_effect")

# ============================================================
# 汎用カラーオーバーレイ
# ============================================================
# フラッシュより強めの色被せ。ホラー演出などに。

screen color_overlay(overlay_color="#ff0000", overlay_alpha=0.15, overlay_duration=0.08):
    zorder 150
    add Solid(overlay_color) alpha overlay_alpha
    timer overlay_duration action Hide("color_overlay")

# ============================================================
# 汎用ブラックアウト
# ============================================================
# 完全暗転 → 自動復帰。

screen blackout_effect(blackout_duration=0.5):
    zorder 200
    add Solid("#000000")
    timer blackout_duration action Hide("blackout_effect")

# ============================================================
# 画面揺れトランジション定義
# ============================================================

# ============================================================
# ブラックアウト（手動非表示版）
# ============================================================
# scene 切り替え前の暗転など、スクリプト側で制御する場合に使用。

screen blackout():
    zorder 200
    add Solid("#000000")

# ============================================================
# ノイズエフェクト（軽度）
# ============================================================
# 砂嵐のようなちらつき演出。ホラー & 異常検知向け。

screen noise_effect():
    zorder 150
    add Solid("#ffffff") alpha 0.03
    timer 0.05 action Hide("noise_effect") repeat False

# ============================================================
# ノイズエフェクト（重度）
# ============================================================
# より強い視覚ノイズ。緊迫シーン向け。

screen heavy_noise_effect():
    zorder 150
    add Solid("#ff0000") alpha 0.08
    timer 0.1 action Hide("heavy_noise_effect") repeat False

# ============================================================
# 画面揺れトランジション定義
# ============================================================

# 短い画面揺れ（衝撃演出用）
transform short_shake:
    linear 0.05 offset (8, 8)
    linear 0.05 offset (-8, -8)
    linear 0.05 offset (8, 8)
    linear 0.05 offset (-8, -8)
    linear 0.05 offset (4, 4)
    linear 0.05 offset (0, 0)

# 長い画面揺れ（地震演出用）
transform long_shake:
    linear 0.05 offset (12, 12)
    linear 0.05 offset (-12, -12)
    linear 0.05 offset (12, 12)
    linear 0.05 offset (-12, -12)
    linear 0.05 offset (8, 8)
    linear 0.05 offset (-8, -8)
    linear 0.05 offset (8, 8)
    linear 0.05 offset (-8, -8)
    linear 0.05 offset (4, 4)
    linear 0.05 offset (-4, -4)
    linear 0.05 offset (4, 4)
    linear 0.05 offset (0, 0)
