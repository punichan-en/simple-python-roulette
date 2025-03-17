import tkinter as tk
from tkinter import Canvas, Toplevel, colorchooser, messagebox
import random
import time
import math

class Roulette:
    def __init__(self, master):
        self.master = master
        self.master.geometry("500x600")
        self.master.title("ルーレット")
        
        # ルーレットの各数字の色とポケット情報
        self.number_colors = {
            0: "green",
            # 赤いポケットの数字
            1: "red", 3: "red", 5: "red", 7: "red", 9: "red", 12: "red",
            14: "red", 16: "red", 18: "red", 19: "red", 21: "red", 23: "red",
            25: "red", 27: "red", 30: "red", 32: "red", 34: "red", 36: "red",
            # 黒いポケットの数字
            2: "black", 4: "black", 6: "black", 8: "black", 10: "black", 11: "black",
            13: "black", 15: "black", 17: "black", 20: "black", 22: "black", 24: "black",
            26: "black", 28: "black", 29: "black", 31: "black", 33: "black", 35: "black"
        }
        
        # 各数字の表示テキスト
        self.number_texts = {num: str(num) for num in self.number_colors.keys()}
        
        # ルーレット盤面用のキャンバス
        self.canvas = Canvas(
            master, 
            width=300, 
            height=300, 
            bg="darkgreen"
        )
        self.canvas.pack(pady=10)
        
        # 回転角度
        self.rotation_angle = 0
        # ボールの位置
        self.ball_pos = None
        # ボールオブジェクト
        self.ball = None
        
        # ルーレット描画
        self.draw_roulette()
        
        # 結果表示用ラベル
        self.result_label = tk.Label(
            master,
            text="?",
            font=("Helvetica", 72)
        )
        self.result_label.pack(pady=10)
        
        # 入力フレーム
        self.input_frame = tk.Frame(master)
        self.input_frame.pack(pady=10)
        
        # 停止させたい数値を入力するフィールド
        self.stop_label = tk.Label(
            self.input_frame,
            text="停止させたい数値:"
        )
        self.stop_label.pack(side=tk.LEFT, padx=5)
        
        self.stop_value = tk.Entry(
            self.input_frame,
            width=5
        )
        self.stop_value.pack(side=tk.LEFT)
        
        # ボタンフレーム
        self.button_frame = tk.Frame(master)
        self.button_frame.pack(pady=10)
        
        # スタートボタン
        self.start_button = tk.Button(
            self.button_frame,
            text="Start",
            command=self.spin,
            width=10,
            height=2
        )
        self.start_button.pack(side=tk.LEFT, padx=10)
        
        # 停止ボタン
        self.stop_button = tk.Button(
            self.button_frame,
            text="Stop",
            command=self.stop_spin,
            width=10,
            height=2,
            state='disabled'
        )
        self.stop_button.pack(side=tk.LEFT, padx=10)
        
        # カスタマイズボタン
        self.customize_button = tk.Button(
            self.button_frame,
            text="カスタマイズ",
            command=self.open_customization,
            width=10,
            height=2
        )
        self.customize_button.pack(side=tk.LEFT, padx=10)
        
        # ステータス表示用ラベル
        self.status_label = tk.Label(
            master,
            text="スタートボタンを押してください",
            fg="blue"
        )
        self.status_label.pack(pady=10)
        
        self.is_spinning = False
        self.target_number = None
    
    def draw_roulette(self):
        # キャンバスをクリア
        self.canvas.delete("all")
        
        # ルーレットの円を描画
        center_x, center_y = 150, 150
        outer_radius = 120
        inner_radius = 80
        
        # 外側の円
        self.canvas.create_oval(
            center_x - outer_radius, 
            center_y - outer_radius,
            center_x + outer_radius, 
            center_y + outer_radius,
            fill="darkgreen", width=2
        )
        
        # 内側の円
        self.canvas.create_oval(
            center_x - inner_radius, 
            center_y - inner_radius,
            center_x + inner_radius, 
            center_y + inner_radius,
            fill="darkgreen", width=1
        )
        
        # 数字の配置（実際のルーレットの順序を維持するが数値範囲は可変）
        numbers = list(self.number_colors.keys())
        
        # 各ポケットの角度を計算
        angle_per_pocket = 360 / len(numbers)
        
        for i, number in enumerate(numbers):
            angle = math.radians(i * angle_per_pocket)
            
            # ポケットの中心座標
            pocket_r = (inner_radius + outer_radius) / 2
            pocket_x = center_x + pocket_r * math.sin(angle)
            pocket_y = center_y - pocket_r * math.cos(angle)
            
            # ポケットの色を取得
            color = self.number_colors[number]
            
            # ポケットを描画
            pocket_size = 15
            self.canvas.create_oval(
                pocket_x - pocket_size, pocket_y - pocket_size,
                pocket_x + pocket_size, pocket_y + pocket_size,
                fill=color, outline="white", tags=f"pocket_{number}"
            )
            
            # 数字を描画
            self.canvas.create_text(
                pocket_x, pocket_y,
                text=self.number_texts[number],
                fill="white",
                font=("Helvetica", 9, "bold"),
                tags=f"number_{number}"
            )
        
        # ボールを描画
        self.ball = self.canvas.create_oval(
            center_x - 5, center_y - 5,
            center_x + 5, center_y + 5,
            fill="white", outline="gray", tags="ball"
        )
    
    def spin(self):
        if not self.is_spinning:
            # 停止させたい数値を取得
            try:
                target_value = self.stop_value.get().strip()
                if target_value:
                    try:
                        self.target_number = int(target_value)
                        if self.target_number not in self.number_colors:
                            self.status_label.config(text=f"設定された範囲内の数値を入力してください ({min(self.number_colors.keys())}-{max(self.number_colors.keys())})", fg="red")
                            return
                    except ValueError:
                        # 数値でない場合はテキストで検索
                        found = False
                        for num, text in self.number_texts.items():
                            if text == target_value:
                                self.target_number = num
                                found = True
                                break
                        
                        if not found:
                            self.status_label.config(text="有効な数値またはテキストを入力してください", fg="red")
                            return
                else:
                    self.target_number = None
            except ValueError:
                self.status_label.config(text="有効な数値を入力してください", fg="red")
                return
            
            self.is_spinning = True
            self.start_button.config(state='disabled')
            self.stop_button.config(state='normal')
            self.customize_button.config(state='disabled')
            self.status_label.config(text="回転中...", fg="blue")
            self.animate_spin()
    
    def animate_spin(self):
        if self.is_spinning:
            # ルーレットの回転を表現
            self.rotation_angle += 5
            center_x, center_y = 150, 150
            
            # キャンバスをクリア
            self.canvas.delete("ball")
            
            # ボールの位置を計算
            angle = math.radians(self.rotation_angle)
            ball_r = 100  # ボールの回転半径
            ball_x = center_x + ball_r * math.cos(angle)
            ball_y = center_y + ball_r * math.sin(angle)
            
            # ボールを描画
            self.ball = self.canvas.create_oval(
                ball_x - 5, ball_y - 5,
                ball_x + 5, ball_y + 5,
                fill="white", outline="gray", tags="ball"
            )
            
            # 数字をランダム表示
            available_numbers = list(self.number_colors.keys())
            number = random.choice(available_numbers)
            self.result_label.config(text=self.number_texts[number])
            
            # 目標の数値で停止
            if self.target_number is not None and number == self.target_number:
                self.stop_spin()
                self.status_label.config(text=f"目標の数値 {self.number_texts[self.target_number]} で停止しました！", fg="green")
                # ボールを目標数字のポケットに移動
                self.highlight_number(self.target_number)
            else:
                self.master.after(100, self.animate_spin)
        else:
            self.start_button.config(state='normal')
            self.stop_button.config(state='disabled')
            self.customize_button.config(state='normal')
    
    def stop_spin(self):
        if self.is_spinning:
            self.is_spinning = False
            
            # 現在表示されている数字を取得
            current_text = self.result_label.cget("text")
            current_number = None
            
            # テキストから対応する数字を検索
            for num, text in self.number_texts.items():
                if text == current_text:
                    current_number = num
                    break
            
            # 見つからない場合はランダムな数字を使用
            if current_number is None:
                current_number = random.choice(list(self.number_colors.keys()))
                
            self.status_label.config(text=f"停止しました: {self.number_texts[current_number]}", fg="blue")
            self.start_button.config(state='normal')
            self.stop_button.config(state='disabled')
            self.customize_button.config(state='normal')
            
            # 停止した数字のポケットをハイライト
            self.highlight_number(current_number)
    
    def highlight_number(self, number):
        # キャンバスをクリア
        self.canvas.delete("ball")
        
        # 数字のタグを取得
        number_tag = f"number_{number}"
        
        # 数字の座標を取得
        item = self.canvas.find_withtag(number_tag)
        if item:
            coords = self.canvas.coords(item)
            x, y = coords[0], coords[1]
            
            # ボールを該当する数字のポケットに移動
            self.ball = self.canvas.create_oval(
                x - 5, y - 5,
                x + 5, y + 5,
                fill="white", outline="gold", width=2, tags="ball"
            )
            
            # 数字の色を変更
            self.canvas.itemconfig(item, fill="gold")
    
    def open_customization(self):
        """ルーレットのカスタマイズウィンドウを開く"""
        # カスタマイズウィンドウを作成
        custom_window = Toplevel(self.master)
        custom_window.title("ルーレットカスタマイズ")
        custom_window.geometry("600x500")
        
        # 説明ラベル
        tk.Label(
            custom_window,
            text="ルーレットの内容をカスタマイズ",
            font=("Helvetica", 14, "bold")
        ).pack(pady=10)
        
        # スクロール可能なフレームの作成
        frame_canvas = tk.Frame(custom_window)
        frame_canvas.pack(fill="both", expand=True, padx=10, pady=10)
        
        # キャンバス+スクロールバーの作成
        canvas = tk.Canvas(frame_canvas)
        scrollbar = tk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        frame_canvas.pack(fill="both", expand=True)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 数字とその色を編集するフィールドを作成
        self.custom_entries = {}
        self.color_buttons = {}
        
        # ヘッダー
        tk.Label(scrollable_frame, text="数字", width=5).grid(row=0, column=0, padx=5, pady=5)
        tk.Label(scrollable_frame, text="表示テキスト", width=10).grid(row=0, column=1, padx=5, pady=5)
        tk.Label(scrollable_frame, text="色", width=5).grid(row=0, column=2, padx=5, pady=5)
        
        # 各数字のエントリーを作成
        sorted_numbers = sorted(self.number_colors.keys())
        for i, number in enumerate(sorted_numbers):
            # 数字ラベル
            tk.Label(scrollable_frame, text=str(number)).grid(row=i+1, column=0, padx=5, pady=2)
            
            # テキスト入力フィールド
            text_var = tk.StringVar(value=self.number_texts[number])
            text_entry = tk.Entry(scrollable_frame, textvariable=text_var, width=10)
            text_entry.grid(row=i+1, column=1, padx=5, pady=2)
            
            # 色選択ボタン
            color = self.number_colors[number]
            color_button = tk.Button(
                scrollable_frame,
                bg=color,
                width=5,
                command=lambda num=number: self.choose_color(num)
            )
            color_button.grid(row=i+1, column=2, padx=5, pady=2)
            
            self.custom_entries[number] = text_var
            self.color_buttons[number] = color_button
        
        # 数値範囲変更フレーム
        range_frame = tk.LabelFrame(custom_window, text="数値範囲設定", padx=10, pady=10)
        range_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(range_frame, text="最小値:").grid(row=0, column=0, padx=5, pady=5)
        self.min_value = tk.IntVar(value=min(self.number_colors.keys()))
        tk.Entry(range_frame, textvariable=self.min_value, width=5).grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(range_frame, text="最大値:").grid(row=0, column=2, padx=5, pady=5)
        self.max_value = tk.IntVar(value=max(self.number_colors.keys()))
        tk.Entry(range_frame, textvariable=self.max_value, width=5).grid(row=0, column=3, padx=5, pady=5)
        
        # ボタンフレーム
        button_frame = tk.Frame(custom_window)
        button_frame.pack(pady=10)
        
        # 変更適用ボタン
        tk.Button(
            button_frame,
            text="適用して閉じる",
            command=lambda: self.apply_customization(custom_window)
        ).pack(side=tk.LEFT, padx=10)
        
        # キャンセルボタン
        tk.Button(
            button_frame,
            text="キャンセル",
            command=custom_window.destroy
        ).pack(side=tk.LEFT, padx=10)
    
    def choose_color(self, number):
        """色選択ダイアログを表示"""
        current_color = self.color_buttons[number].cget("bg")
        color_code = colorchooser.askcolor(color=current_color, title=f"数字 {number} の色を選択")
        
        if color_code[1]:  # 色が選択された場合
            self.color_buttons[number].config(bg=color_code[1])
    
    def apply_customization(self, window):
        """カスタマイズ内容を適用"""
        try:
            min_val = self.min_value.get()
            max_val = self.max_value.get()
            
            if min_val >= max_val:
                messagebox.showerror("エラー", "最小値は最大値より小さく設定してください。")
                return
            
            # 数値範囲の変更があった場合は新しい数字を追加
            new_number_colors = {}
            
            for num in range(min_val, max_val + 1):
                # 既存の数字の場合はその色を使う
                if num in self.number_colors:
                    color = self.color_buttons[num].cget("bg")
                else:
                    # 新しい数字はデフォルトで黒にする
                    color = "black"
                
                new_number_colors[num] = color
            
            # 表示テキストの更新
            self.number_texts = {}
            for num in new_number_colors.keys():
                if num in self.custom_entries:
                    self.number_texts[num] = self.custom_entries[num].get()
                else:
                    self.number_texts[num] = str(num)
            
            # 値を更新
            self.number_colors = new_number_colors
            
            # ルーレットを再描画
            self.canvas.delete("all")
            self.draw_roulette()
            
            window.destroy()
            
            # 状態メッセージの更新
            self.status_label.config(text="ルーレットをカスタマイズしました", fg="blue")
            
        except Exception as e:
            messagebox.showerror("エラー", f"設定の適用中にエラーが発生しました: {str(e)}")

# アプリケーションの起動
if __name__ == "__main__":
    root = tk.Tk()
    app = Roulette(root)
    root.mainloop()