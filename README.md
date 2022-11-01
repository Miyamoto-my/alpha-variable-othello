# alpha-variable-othello
# ~ 可変マスオセロ用ゲームAIの製作 ~


## 学習サイクルの流れについて
1. セルフプレイ部
    学習データ（対局データ）を作成する
1. モデル学習・パラメータ更新部
    対局データを用いて，モデルを学習させる
1. モデル評価部
    学習前のモデルと学習後のモデルを対戦させ，学習後のモデルを評価する


## 学習サイクルの実行について
- Google Colab を用いる場合

- 自PCを用いる場合




## 盤面サイズの変更
~~~python
WIDTH = int
HEIGHT = int

"""
The range of numbers is
4, 6, 8, 10.
"""
~~~

- 変更箇所
    - [ ] dual_network. py
    - [ ] evaluate_network. py
    - [ ] self_play. py


## パラメータ変更
- [ ] dual_network. py
~~~python
DN_FILTERS = 128        # 畳み込み層のカーネル数（本家は256）
DN_RESIDUAL_NUM = 16    # 残差ブロックの数（本家は19）
~~~

- [ ] evaluate_network. py
~~~python
EN_GAME_COUNT = 20      # 1評価あたりのゲーム数（本家は400）
~~~

- [ ] pv_mets. py
~~~python
PV_EVALUATE_COUNT = 80  # 1推論あたりのシミュレーション回数（本家は1600）
~~~

- [ ] self_play. py
~~~python
SP_GAME_COUNT = 750     # セルフプレイを行うゲーム数（本家は25000）
~~~

- [ ] train_cycle. py
~~~python
for i in range(10):     # 学習回数
~~~


- [ ] train_network. py
~~~python
RN_EPOCHS = 100         # 学習回数
~~~


## 参考文献
[AlphaZero 深層学習・強化学習・探索 人工知能プログラミング実践入門](https://www.borndigital.co.jp/book/14383.html)
