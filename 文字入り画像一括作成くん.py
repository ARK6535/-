import tkinter as tk
from tkinter import filedialog, messagebox, ttk, colorchooser
from PIL import Image, ImageDraw, ImageFont

class ImageGeneratorApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("文字入り画像一括作成くん")
        self.root.geometry("480x270")
        self.root.protocol("WM_DELETE_WINDOW", lambda: self.root.destroy())

        self.width = 1200
        self.height = 675
        self.default_background_color = (255, 255, 255)
        self.img = Image.new("RGB", (self.width, self.height), self.default_background_color)
        self.draw = ImageDraw.Draw(self.img)
        self.selecting_background = False
        self.textfile_path = ""
        self.fontfile_path = ""

        self.font_path = "YuGothR.ttc"
        self.max_char_num = tk.StringVar()
        self.max_char_num.set("5")
        self.colorRGB = (0,0,0)
        self.agreed = False
        self.nomoregenerate = False
        self.font_size = int(self.height / int(self.max_char_num.get()))  # Initial font size
        self.root.focus_force()
        self.create_widgets()
        self.style_widgets()

    def create_widgets(self):
        button_frame_1 = tk.Frame(self.root)
        button_frame_1.pack(pady = 20)
        
        select_font_button = ttk.Button(button_frame_1, text="フォントファイルを選択", command=self.select_font)
        select_font_button.pack(side=tk.LEFT, padx=5)

        select_background_button = ttk.Button(button_frame_1, text="背景を選択", command=self.select_background)
        select_background_button.pack(side=tk.LEFT, padx=5)

        reset_background_button = ttk.Button(button_frame_1, text="背景をリセット", command=self.reset_background)
        reset_background_button.pack(side=tk.LEFT, padx=5)

        button_frame_2 = tk.Frame(self.root)
        button_frame_2.pack(pady = 10)

        batch_generate_button = ttk.Button(button_frame_2, text="テキストファイルから画像を生成", command=self.batch_generate_images)
        batch_generate_button.pack(side=tk.LEFT, padx=5)
        
        color_select_button = ttk.Button(button_frame_2, text="文字色を変更",command=self.select_color)
        color_select_button.pack(side=tk.LEFT, padx=5)

        button_frame_3 = tk.Frame(self.root)
        button_frame_3.pack(pady = 10)
        
        text_select_button = ttk.Button(button_frame_3, text="テキストファイルを選択",command=self.select_text)
        text_select_button.pack(side=tk.LEFT, padx=5)
        
        label_entry1 = ttk.Label(button_frame_3,text="一行あたりの文字数/行数")
        label_entry1.pack(side=tk.LEFT,padx=5,)
        
        entry1 = ttk.Entry(button_frame_3, width=4, textvariable=self.max_char_num)
        entry1.pack(side=tk.LEFT, padx=5)

    def style_widgets(self):
        style = ttk.Style()
        style.configure("TButton", padding=5, relief="flat", background="#000000", foreground="black")
        style.map("TButton", foreground=[('pressed', 'black'), ('active', 'black')])
        
    def select_font(self):
        fontfile_path = filedialog.askopenfilename()
        if fontfile_path:
            self.font_path = fontfile_path
            
    def select_color(self):
        self.colorRGB = colorchooser.askcolor()[0]

    def select_background(self):
        imagefile_path = filedialog.askopenfilename(filetypes=[("画像ファイル", "*.jpg;*.jpeg;*.png")])
        if imagefile_path:
            self.background_img = Image.open(imagefile_path)
            self.background_img = self.background_img.resize((self.width, self.height), Image.ANTIALIAS)
            self.selecting_background = True

    def reset_background(self):
        self.img = Image.new("RGB", (self.width, self.height), self.default_background_color)
        self.selecting_background = False

    def calculate_font_size(self, line):
        if len(line) >= 5:
            return self.height // len(line)
        else:
            return self.font_size

    def generate_image_from_data(self, data, fontsize):
        if self.selecting_background:
            self.img.paste(self.background_img)
        else:
            self.img = Image.new("RGB", (self.width, self.height), self.default_background_color)

        self.draw = ImageDraw.Draw(self.img)  # 新しい ImageDraw.Draw オブジェクトを作成

        font = ImageFont.truetype(self.font_path, fontsize)
        total_text_height = len(data) * fontsize
        y = (self.height - total_text_height) // 2

        for text in data:
            text_width, text_height = self.draw.textsize(text, font=font)
            x = (self.width - text_width) // 2
            # textsizeメソッドがテキストの上端と下端の高さを返すため、その差分を引いて調整する
            self.draw.text((x, y + (fontsize - text_height) // 2), text, fill=self.colorRGB, font=font)
            y += fontsize
    def generate_test(self, data, fontsize):

        self.draw = ImageDraw.Draw(self.img)  # 新しい ImageDraw.Draw オブジェクトを作成

        font = ImageFont.truetype(self.font_path, fontsize)
        total_text_height = len(data) * fontsize
        y = (self.height - total_text_height) // 2

        for text in data:
            text_width, text_height = self.draw.textsize(text, font=font)
            if ((text_width > self.height) or text_height > self.height) and not self.agreed:
                answer = messagebox.askquestion(
                title="確認",
                icon='warning',
                type='yesnocancel',
                default='cancel',
                message="画像のサムネイルが不自然になる画像が含まれる可能性があります。\n\nフォントサイズを縮小して生成しますか？",
                detail="「はい」を選ぶと、フォントサイズを縮小して生成します。\n「いいえ」を選ぶと、そのまま画像を生成します。\n「キャンセル」を選ぶと、生成をとりやめます。"
                )
                if answer == 'yes':
                    with open(self.textfile_path, 'r', encoding="utf-8") as f:
                        lines = f.readlines()

                    self.max_char_num.set(max(max(len(line.split(",")) for line in lines), max(len(string) for line in lines for string in line.strip().split(","))))
                    self.font_size = int(self.height / int(self.max_char_num.get()))
                    print(self.max_char_num.get())
                elif answer == 'cancel':
                    self.nomoregenerate = True
    def select_text(self):
        self.textfile_path = filedialog.askopenfilename(filetypes=[("テキストファイル", "*.txt")])
        if not self.textfile_path:
            return

    def batch_generate_images(self):
        self.font_size = int(self.height / int(self.max_char_num.get()))

        if self.textfile_path == "":
            messagebox.showwarning("警告","テキストファイルを選択してください"),
            return
        with open(self.textfile_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
        if not lines: 
            messagebox.showwarning("警告", "選択したテキストファイルは空です。")
            return
        print(lines)

        for idx, line in enumerate(lines, start=1):
            data = line.strip().split(",")
            self.generate_test(data, self.font_size)
            if self.nomoregenerate:
                return
        self.nomoregenerate = False
        
        # 保存先のディレクトリの選択
        save_dir = filedialog.askdirectory()
        if not save_dir:
            return

        for idx, line in enumerate(lines, start=1):
            data = line.strip().split(",")
            self.generate_image_from_data(data,self.font_size)
            self.img.save(f"{save_dir}/clueimage_{idx}.png")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ImageGeneratorApp()
    app.run()
