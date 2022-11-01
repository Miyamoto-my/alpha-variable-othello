# ====================
# 人とAIの対戦
# ====================

# 可変マスにリファクタリング

# パッケージのインポート
from dual_network import HEIGHT, WIDTH
from game import State
from pv_mcts import pv_mcts_action
from tensorflow.keras.models import load_model
from pathlib import Path
from threading import Thread
import tkinter as tk

# ベストプレイヤーのモデルの読み込み
model = load_model('./model/best.h5')

HEIGHT = 6
WIDTH = 6

# ゲームUIの定義
class GameUI(tk.Frame):
    # 初期化
    def __init__(self, master=None, model=None):
        tk.Frame.__init__(self, master)
        self.master.title('リバーシ')
        
        # 盤面幅
        self.height = HEIGHT
        self.width = WIDTH
        self.area = self.height * self.width

        self.size = 100
   
        # ゲーム状態の生成
        self.state = State(height=HEIGHT, width=WIDTH)

        # PV MCTSで行動選択を行う関数の生成
        self.next_action = pv_mcts_action(model, 0.0)

        # キャンバスの生成
        self.c = tk.Canvas(self, width = self.width * self.size, height = self.height * self.size, highlightthickness = 0)
        self.c.bind('<Button-1>', self.turn_of_human)
        self.c.pack()

        # 描画の更新
        self.on_draw()

    # 人間のターン
    def turn_of_human(self, event):
        # ゲーム終了時
        if self.state.is_done():
            self.state = State()
            self.on_draw()
            return

        # 先手でない時
        if not self.state.is_first_player():
            return

        # クリック位置を行動に変換
        x = int(event.x/self.size)
        y = int(event.y/self.size)
        if x < 0 or self.width-1 < x or y < 0 or self.height-1 < y: # 範囲外
            return
        action = x + y * self.width

        # 合法手でない時
        legal_actions = self.state.legal_actions()
        if legal_actions == [self.area]:
            action = self.area # パス
        if action != self.area and not (action in legal_actions):
            return

        # 次の状態の取得
        self.state = self.state.next(action)
        self.on_draw()

        # AIのターン
        self.master.after(1, self.turn_of_ai)

    # AIのターン
    def turn_of_ai(self):
        # ゲーム終了時
        if self.state.is_done():
            return

        # 行動の取得
        action = self.next_action(self.state)

        # 次の状態の取得
        self.state = self.state.next(action)
        self.on_draw()

    # 石の描画
    def draw_piece(self, index, first_player):
        x = (index%self.width)*self.size+5
        y = int(index/self.width)*self.size+5
        if first_player:
            self.c.create_oval(x, y, x+(self.size-10), y+(self.size-10), width = 1.0, outline = '#00591c', fill = '#000000')
        else:
            self.c.create_oval(x, y, x+(self.size-10), y+(self.size-10), width = 1.0, outline = '#00591c', fill = '#FFFFFF')

    # 描画の更新
    def on_draw(self):
        self.c.delete('all')
        self.c.create_rectangle(0, 0, self.width*self.size, self.height*self.size, width = 0.0, fill = '#06a800')
        for i in range(1, 8):# ここのrangeの値の設定要確認
            self.c.create_line(0, i*self.size, self.width*self.size, i*self.size, width = 1.0, fill = '#000000')
            self.c.create_line(i*self.size, 0, i*self.size, self.height*self.size, width = 1.0, fill = '#000000')
        for i in range(self.area):
            if self.state.pieces[i] == 1:
                self.draw_piece(i, self.state.is_first_player())
            if self.state.enemy_pieces[i] == 1:
                self.draw_piece(i, not self.state.is_first_player())

# ゲームUIの実行
f = GameUI(model=model)
f.pack()
f.mainloop()
