import random
import tkinter as tk
import webbrowser
from pathlib import Path
from tkinter import font, ttk


TRIGRAMS = {
    "乾": (1, 1, 1),
    "兑": (0, 1, 1),
    "离": (1, 0, 1),
    "震": (0, 0, 1),
    "巽": (1, 1, 0),
    "坎": (0, 1, 0),
    "艮": (1, 0, 0),
    "坤": (0, 0, 0),
}

GUA_LIST = [
    ("乾", "乾为天", "乾上乾下"),
    ("坤", "坤为地", "坤上坤下"),
    ("屯", "水雷屯", "坎上震下"),
    ("蒙", "山水蒙", "艮上坎下"),
    ("需", "水天需", "坎上乾下"),
    ("讼", "天水讼", "乾上坎下"),
    ("师", "地水师", "坤上坎下"),
    ("比", "水地比", "坎上坤下"),
    ("小畜", "风天小畜", "巽上乾下"),
    ("履", "天泽履", "乾上兑下"),
    ("泰", "地天泰", "坤上乾下"),
    ("否", "天地否", "乾上坤下"),
    ("同人", "天火同人", "乾上离下"),
    ("大有", "火天大有", "离上乾下"),
    ("谦", "地山谦", "坤上艮下"),
    ("豫", "雷地豫", "震上坤下"),
    ("随", "泽雷随", "兑上震下"),
    ("蛊", "山风蛊", "艮上巽下"),
    ("临", "地泽临", "坤上兑下"),
    ("观", "风地观", "巽上坤下"),
    ("噬嗑", "火雷噬嗑", "离上震下"),
    ("贲", "山火贲", "艮上离下"),
    ("剥", "山地剥", "艮上坤下"),
    ("复", "地雷复", "坤上震下"),
    ("无妄", "天雷无妄", "乾上震下"),
    ("大畜", "山天大畜", "艮上乾下"),
    ("颐", "山雷颐", "艮上震下"),
    ("大过", "泽风大过", "兑上巽下"),
    ("坎", "坎为水", "坎上坎下"),
    ("离", "离为火", "离上离下"),
    ("咸", "泽山咸", "兑上艮下"),
    ("恒", "雷风恒", "震上巽下"),
    ("遁", "天山遁", "乾上艮下"),
    ("大壮", "雷天大壮", "震上乾下"),
    ("晋", "火地晋", "离上坤下"),
    ("明夷", "地火明夷", "坤上离下"),
    ("家人", "风火家人", "巽上离下"),
    ("睽", "火泽睽", "离上兑下"),
    ("蹇", "水山蹇", "坎上艮下"),
    ("解", "雷水解", "震上坎下"),
    ("损", "山泽损", "艮上兑下"),
    ("益", "风雷益", "巽上震下"),
    ("夬", "泽天夬", "兑上乾下"),
    ("姤", "天风姤", "乾上巽下"),
    ("萃", "泽地萃", "兑上坤下"),
    ("升", "地风升", "坤上巽下"),
    ("困", "泽水困", "兑上坎下"),
    ("井", "水风井", "坎上巽下"),
    ("革", "泽火革", "兑上离下"),
    ("鼎", "火风鼎", "离上巽下"),
    ("震", "震为雷", "震上震下"),
    ("艮", "艮为山", "艮上艮下"),
    ("渐", "风山渐", "巽上艮下"),
    ("归妹", "雷泽归妹", "震上兑下"),
    ("丰", "雷火丰", "震上离下"),
    ("旅", "火山旅", "离上艮下"),
    ("巽", "巽为风", "巽上巽下"),
    ("兑", "兑为泽", "兑上兑下"),
    ("涣", "风水涣", "巽上坎下"),
    ("节", "水泽节", "坎上兑下"),
    ("中孚", "风泽中孚", "巽上兑下"),
    ("小过", "雷山小过", "震上艮下"),
    ("既济", "水火既济", "坎上离下"),
    ("未济", "火水未济", "离上坎下"),
]

PALACE_TO_GUA = {palace: (index, name, full_name) for index, (name, full_name, palace) in enumerate(GUA_LIST, start=1)}
TRIGRAM_BY_LINES = {lines: name for name, lines in TRIGRAMS.items()}
LINE_TYPES = {
    6: ("老阴", 0, True),
    7: ("少阳", 1, False),
    8: ("少阴", 0, False),
    9: ("老阳", 1, True),
}

QUESTION_HINTS = {
    "感情": ("感情", "关系宜慢热观察，重在沟通边界与真实态度。"),
    "恋爱": ("感情", "关系宜慢热观察，重在沟通边界与真实态度。"),
    "婚姻": ("感情", "关系宜慢热观察，重在沟通边界与真实态度。"),
    "复合": ("感情", "关系宜慢热观察，重在沟通边界与真实态度。"),
    "事业": ("事业", "事务宜先稳住节奏，再看机会与责任是否匹配。"),
    "工作": ("事业", "事务宜先稳住节奏，再看机会与责任是否匹配。"),
    "升职": ("事业", "事务宜先稳住节奏，再看机会与责任是否匹配。"),
    "财": ("财运", "财务宜守正避险，先看现金流和可控成本。"),
    "钱": ("财运", "财务宜守正避险，先看现金流和可控成本。"),
    "投资": ("财运", "财务宜守正避险，先看现金流和可控成本。"),
    "考试": ("学业", "学习宜按计划推进，先补短板，再争取突破。"),
    "学习": ("学业", "学习宜按计划推进，先补短板，再争取突破。"),
    "健康": ("健康", "身体相关宜保守对待，留意作息和及时寻求专业意见。"),
    "病": ("健康", "身体相关宜保守对待，留意作息和及时寻求专业意见。"),
}

HEXAGRAM_TONES = {
    "乾": "势头强，重在主动担当，但忌逞强冒进。",
    "坤": "形势宜顺势承载，重在耐心、配合与长期积累。",
    "屯": "开局多阻，先理清条件，稳住基础再推进。",
    "蒙": "信息尚未明朗，宜先学习求证，不宜凭猜测定局。",
    "需": "时机未足，等待中要准备资源和退路。",
    "讼": "有争执之象，宜减少对抗，保留证据，寻求调和。",
    "师": "需要组织和纪律，先定规则再行动。",
    "比": "有依附合作之象，关键在选择可信之人。",
    "泰": "上下相通，形势较顺，但仍需守住节制。",
    "否": "气机不通，宜收缩调整，避免硬推。",
    "同人": "利于结盟同行，公开透明更容易成事。",
    "大有": "资源较足，宜善用优势，也要防止骄满。",
    "谦": "以退为进，低调稳健反而更有利。",
    "豫": "有动意和机会，先防松散，再借势推进。",
    "随": "宜顺势而行，但不能失去自己的判断。",
    "蛊": "旧问题需要清理，先修补根因。",
    "临": "机会渐近，宜主动靠近目标。",
    "观": "先观察局势，不急于表态或下注。",
    "噬嗑": "问题需要决断，规则和边界要清楚。",
    "贲": "外在条件可修饰，但根本实力更重要。",
    "剥": "有削弱之象，宜保守防耗。",
    "复": "有回转复起之机，适合重新开始。",
    "无妄": "宜守真实，不宜投机取巧。",
    "大畜": "积累已成，但仍需克制等待。",
    "颐": "重在养正，入口之言与投入之物都要谨慎。",
    "大过": "压力偏重，需找支撑，避免独自硬扛。",
    "坎": "险中求稳，先处理风险。",
    "离": "事情逐渐显明，宜看清依附关系。",
    "咸": "有感应互动，真诚比技巧更关键。",
    "恒": "贵在持久，短期波动不宜轻易放弃。",
    "遁": "宜退守避锋，保存实力。",
    "大壮": "力量上升，行动要合规有度。",
    "晋": "有上升光明之象，适合展示能力。",
    "明夷": "明处受损，宜低调保护自己。",
    "家人": "内部秩序重要，先安内再对外。",
    "睽": "意见相左，求同存异更实际。",
    "蹇": "前路有阻，宜绕行或求助。",
    "解": "困局有松动，宜趁机化解旧结。",
    "损": "先减后得，舍弃不必要消耗。",
    "益": "有增益之象，适合互惠合作。",
    "夬": "需要果断决裂或定案，但忌情绪化。",
    "姤": "突遇变化，先辨别来意。",
    "萃": "资源聚集，宜借团队或平台。",
    "升": "循序上升，不可急躁。",
    "困": "受限明显，先求脱困再求发展。",
    "井": "资源稳定，重在持续经营。",
    "革": "变革之象，旧法不适用时要换思路。",
    "鼎": "更新立制，适合整合资源。",
    "震": "有惊动变化，先稳心神再行动。",
    "艮": "止而不动，宜暂停审视。",
    "渐": "渐进有成，宜按步骤推进。",
    "归妹": "关系或条件不够正位，需谨慎承诺。",
    "丰": "声势较盛，盛中防过。",
    "旅": "不宜久留，适合短线应对。",
    "巽": "柔顺渗透，沟通和细节能成事。",
    "兑": "悦动交流，利谈判表达，忌轻诺。",
    "涣": "涣散需聚，先统一人心和目标。",
    "节": "节制有度，规则越清楚越有利。",
    "中孚": "诚信为本，真意能打动对方。",
    "小过": "小事可行，大事宜缓。",
    "既济": "阶段已成，防收尾疏忽。",
    "未济": "尚未完成，仍需补足最后条件。",
}

COLORS = {
    "paper": "#f4f1e8",
    "paper_deep": "#e8e1d2",
    "paper_edge": "#d5cab7",
    "ink": "#141414",
    "ink_soft": "#4a4740",
    "ink_faint": "#8b8578",
    "wash": "#c9c1b1",
    "white": "#fbfaf5",
}


class YijingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("简易卦象")
        self._set_window_icon()
        self._set_initial_geometry()
        self.minsize(520, 620)
        self.resizable(True, True)
        self.configure(bg=COLORS["paper"])

        self.gua_number = tk.StringVar(value="--")
        self.gua_name = tk.StringVar(value="尚未抽卦")
        self.gua_detail = tk.StringVar(value="点击按钮生成卦象")
        self.change_lines = tk.StringVar(value="变爻：--")
        self.method_detail = tk.StringVar(value="方法：三枚铜钱逐爻生成，自下而上。")
        self.changed_gua = tk.StringVar(value="变卦：--")
        self.copy_preview = tk.StringVar(value="复制内容：尚未抽卦")
        self.question_var = tk.StringVar()
        self.lines = [1, 1, 1, 1, 1, 1]
        self.changed_lines = [1, 1, 1, 1, 1, 1]
        self.line_values = [7, 7, 7, 7, 7, 7]
        self.active_changes = []
        self.current_copy_text = ""
        self.copy_summary = "尚未抽卦"
        self.online_status = "需要联网解卦时，先写下要算什么，再抽卦并点击“联网解卦”。"
        self.current_base_gua = None
        self.current_changed_gua = None
        self.is_compact = False

        self._setup_fonts()
        self._setup_style()
        self._build_ui()
        self.bind("<Configure>", self._handle_resize)
        self.after_idle(self._apply_layout)

    def _set_window_icon(self):
        icon_path = Path(__file__).with_name("E-915966-53726DA1-2种尺寸.ico")
        if icon_path.exists():
            self.iconbitmap(str(icon_path))

    def _set_initial_geometry(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        width = min(1040, max(screen_width - 120, 520))
        height = min(900, max(screen_height - 140, 620))
        x = max((screen_width - width) // 2, 0)
        y = max((screen_height - height) // 2, 0)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def _setup_fonts(self):
        self.title_font = font.Font(family="KaiTi", size=25, weight="bold")
        self.caption_font = font.Font(family="Microsoft YaHei UI", size=10)
        self.number_font = font.Font(family="Segoe UI", size=44, weight="bold")
        self.name_font = font.Font(family="KaiTi", size=22, weight="bold")
        self.detail_font = font.Font(family="Microsoft YaHei UI", size=12)
        self.button_font = font.Font(family="Microsoft YaHei UI", size=12, weight="bold")

    def _setup_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Root.TFrame", background=COLORS["paper"])
        style.configure(
            "Panel.TFrame",
            background=COLORS["white"],
            bordercolor=COLORS["paper_edge"],
            relief="solid",
            borderwidth=1,
        )
        style.configure("Header.TFrame", background=COLORS["paper"])
        style.configure("Title.TLabel", background=COLORS["paper"], foreground=COLORS["ink"], font=self.title_font)
        style.configure("Caption.TLabel", background=COLORS["paper"], foreground=COLORS["ink_faint"], font=self.caption_font)
        style.configure("PanelCaption.TLabel", background=COLORS["white"], foreground=COLORS["ink_faint"], font=self.caption_font)
        style.configure("Number.TLabel", background=COLORS["white"], foreground=COLORS["ink"], font=self.number_font)
        style.configure("Name.TLabel", background=COLORS["white"], foreground=COLORS["ink"], font=self.name_font)
        style.configure("Detail.TLabel", background=COLORS["white"], foreground=COLORS["ink_soft"], font=self.detail_font)
        style.configure("Change.TLabel", background=COLORS["white"], foreground=COLORS["ink"], font=self.detail_font)
        style.configure("Muted.TLabel", background=COLORS["white"], foreground=COLORS["ink_faint"], font=self.caption_font)
        style.configure("Result.TLabel", background=COLORS["white"], foreground=COLORS["ink_soft"], font=self.detail_font)
        style.configure("CopyPreview.TLabel", background=COLORS["paper"], foreground=COLORS["ink_faint"], font=self.caption_font)
        style.configure(
            "Ink.TEntry",
            fieldbackground=COLORS["paper"],
            foreground=COLORS["ink"],
            bordercolor=COLORS["paper_edge"],
            lightcolor=COLORS["paper_edge"],
            darkcolor=COLORS["paper_edge"],
            insertcolor=COLORS["ink"],
            padding=(10, 8),
        )
        style.configure(
            "Primary.TButton",
            background=COLORS["ink"],
            foreground=COLORS["white"],
            borderwidth=1,
            bordercolor=COLORS["ink"],
            focusthickness=0,
            font=self.button_font,
            padding=(18, 12),
        )
        style.map("Primary.TButton", background=[("active", "#333333"), ("pressed", "#000000")])
        style.configure(
            "Secondary.TButton",
            background=COLORS["white"],
            foreground=COLORS["ink"],
            borderwidth=1,
            bordercolor=COLORS["ink"],
            focusthickness=0,
            font=self.button_font,
            padding=(16, 12),
        )
        style.map("Secondary.TButton", background=[("active", COLORS["paper_deep"]), ("pressed", COLORS["paper_edge"])])

    def _build_ui(self):
        self.container = ttk.Frame(self, style="Root.TFrame", padding=24)
        self.container.pack(fill="both", expand=True, side="top")
        self.container.columnconfigure(0, weight=3, minsize=250)
        self.container.columnconfigure(1, weight=4, minsize=260)
        self.container.rowconfigure(1, weight=1)

        header = ttk.Frame(self.container, style="Header.TFrame")
        header.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 18))
        header.columnconfigure(0, weight=1)

        ttk.Label(header, text="简易卦象", style="Title.TLabel").grid(row=0, column=0, sticky="w")
        self.header_caption = ttk.Label(
            header,
            text="三枚铜钱起卦，展示本卦、变爻与变卦；可复制卦象或跳转智谱清言联网解卦。",
            style="Caption.TLabel",
        )
        self.header_caption.grid(row=1, column=0, sticky="w", pady=(4, 0))

        self.info_panel = ttk.Frame(self.container, style="Panel.TFrame", padding=22)
        self.info_panel.grid(row=1, column=0, sticky="nsew", padx=(0, 14))
        self.info_panel.columnconfigure(0, weight=1)
        self.info_panel.rowconfigure(11, weight=1)

        ttk.Label(self.info_panel, text="卦序", style="PanelCaption.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(self.info_panel, textvariable=self.gua_number, style="Number.TLabel").grid(row=1, column=0, sticky="w", pady=(0, 8))
        ttk.Label(self.info_panel, text="卦名", style="PanelCaption.TLabel").grid(row=2, column=0, sticky="w")
        self.name_label = ttk.Label(self.info_panel, textvariable=self.gua_name, style="Name.TLabel", wraplength=260)
        self.name_label.grid(row=3, column=0, sticky="ew", pady=(2, 8))
        self.detail_label = ttk.Label(self.info_panel, textvariable=self.gua_detail, style="Detail.TLabel", wraplength=260)
        self.detail_label.grid(row=4, column=0, sticky="ew")
        self.method_label = ttk.Label(self.info_panel, textvariable=self.method_detail, style="Muted.TLabel", wraplength=260)
        self.method_label.grid(row=5, column=0, sticky="ew", pady=(10, 0))
        self.change_label = ttk.Label(self.info_panel, textvariable=self.change_lines, style="Change.TLabel", wraplength=260)
        self.change_label.grid(row=6, column=0, sticky="ew", pady=(8, 0))
        self.changed_label = ttk.Label(self.info_panel, textvariable=self.changed_gua, style="Result.TLabel", wraplength=260)
        self.changed_label.grid(row=7, column=0, sticky="ew", pady=(6, 0))
        ttk.Label(self.info_panel, text="要算什么（联网解卦用）", style="PanelCaption.TLabel").grid(row=8, column=0, sticky="w", pady=(14, 0))
        self.question_entry = ttk.Entry(self.info_panel, textvariable=self.question_var, style="Ink.TEntry")
        self.question_entry.grid(row=9, column=0, sticky="ew", pady=(6, 0))
        self.question_entry.bind("<Return>", lambda _event: self.open_online_interpretation())
        ttk.Label(self.info_panel, text="联网状态", style="PanelCaption.TLabel").grid(row=10, column=0, sticky="w", pady=(12, 0))
        self.online_status_text = tk.Text(
            self.info_panel,
            height=5,
            wrap="word",
            bg=COLORS["paper"],
            fg=COLORS["ink_soft"],
            relief="flat",
            padx=10,
            pady=10,
            font=("Microsoft YaHei UI", 10),
            insertbackground=COLORS["ink"],
        )
        self.online_status_text.grid(row=11, column=0, sticky="nsew", pady=(6, 0))
        self._set_online_status(self.online_status)

        self.visual_panel = ttk.Frame(self.container, style="Panel.TFrame", padding=16)
        self.visual_panel.grid(row=1, column=1, sticky="nsew")
        self.visual_panel.columnconfigure(0, weight=1)
        self.visual_panel.rowconfigure(0, weight=1)

        self.canvas = tk.Canvas(self.visual_panel, bg=COLORS["white"], highlightthickness=0, height=390)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.canvas.bind("<Configure>", lambda _event: self._draw_hexagram())

        self.action_bar = ttk.Frame(self, style="Root.TFrame", padding=(24, 0, 24, 24))
        self.action_bar.pack(fill="x", side="bottom", before=self.container)
        self.action_bar.columnconfigure(0, weight=0)
        self.action_bar.columnconfigure(1, weight=0)
        self.action_bar.columnconfigure(2, weight=1)
        self.action_bar.columnconfigure(3, weight=0)
        self.cast_button = ttk.Button(self.action_bar, text="抽一卦", style="Primary.TButton", command=self.cast_hexagram)
        self.cast_button.grid(row=0, column=0, sticky="w")
        self.online_button = ttk.Button(
            self.action_bar,
            text="联网解卦",
            style="Secondary.TButton",
            command=self.open_online_interpretation,
        )
        self.online_button.grid(row=0, column=1, sticky="w", padx=(10, 0))
        self.copy_preview_label = ttk.Label(
            self.action_bar,
            textvariable=self.copy_preview,
            style="CopyPreview.TLabel",
            anchor="e",
        )
        self.copy_preview_label.grid(row=0, column=2, sticky="ew", padx=14)
        self.copy_button = ttk.Button(
            self.action_bar,
            text="复制卦象信息",
            style="Secondary.TButton",
            command=self.copy_hexagram_info,
        )
        self.copy_button.grid(row=0, column=3, sticky="e")

        self._draw_hexagram()

    def _handle_resize(self, event):
        if event.widget is not self:
            return
        self._apply_layout()

    def _apply_layout(self):
        width = self.winfo_width()
        height = self.winfo_height()
        is_narrow = width < 560
        is_compact = width < 820
        is_dense = height < 620
        self.is_compact = is_compact
        padding = 10 if is_narrow or is_dense else 16 if is_compact else 24
        self.container.configure(padding=padding)
        action_padding = (10, 0, 10, 10) if is_narrow or is_dense else (16, 0, 16, 16) if is_compact else (24, 0, 24, 24)
        self.action_bar.configure(padding=action_padding)
        self.header_caption.configure(wraplength=max(width - padding * 2, 260))

        if is_compact:
            self.container.columnconfigure(0, weight=1, minsize=0)
            self.container.columnconfigure(1, weight=1, minsize=0)
            self.info_panel.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=0, pady=(0, 12))
            self.visual_panel.grid(row=2, column=0, columnspan=2, sticky="nsew")
            self.action_bar.columnconfigure(0, weight=1, minsize=0)
            self.action_bar.columnconfigure(1, weight=1, minsize=0)
            self.action_bar.columnconfigure(2, weight=1, minsize=0)
            self.action_bar.columnconfigure(3, weight=0, minsize=0)
            self.container.rowconfigure(1, weight=1, minsize=220 if is_dense else 280)
            self.container.rowconfigure(2, weight=1, minsize=180)
            panel_padding = 14 if is_dense else 16
            visual_padding = 10
            title_size, name_size, number_size = 18, 20, 30
            detail_size, caption_size, button_size = 10, 9, 10

            if is_narrow:
                self.cast_button.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0, 6))
                self.online_button.grid(row=1, column=0, columnspan=3, sticky="ew", padx=0, pady=(0, 6))
                self.copy_button.grid(row=2, column=0, columnspan=3, sticky="ew", padx=0, pady=0)
                self.copy_preview_label.grid(row=3, column=0, columnspan=3, sticky="ew", padx=0, pady=(8, 0))
                self.copy_preview_label.configure(wraplength=max(width - 28, 240), justify="left", anchor="w")
            else:
                self.cast_button.grid(row=0, column=0, columnspan=1, sticky="ew")
                self.online_button.grid(row=0, column=1, columnspan=1, sticky="ew", padx=(10, 0), pady=0)
                self.copy_button.grid(row=0, column=2, columnspan=1, sticky="ew", padx=(10, 0), pady=0)
                self.copy_preview_label.grid(row=1, column=0, columnspan=3, sticky="ew", padx=0, pady=(8, 0))
            self.copy_preview_label.configure(wraplength=max(width - 36, 320), justify="left", anchor="w")
        else:
            self.container.columnconfigure(0, weight=3, minsize=250)
            self.container.columnconfigure(1, weight=4, minsize=260)
            self.info_panel.grid(row=1, column=0, columnspan=1, sticky="nsew", padx=(0, 14), pady=0)
            self.visual_panel.grid(row=1, column=1, columnspan=1, sticky="nsew")
            self.action_bar.columnconfigure(0, weight=0, minsize=0)
            self.action_bar.columnconfigure(1, weight=0, minsize=0)
            self.action_bar.columnconfigure(2, weight=1, minsize=0)
            self.action_bar.columnconfigure(3, weight=0, minsize=0)
            self.cast_button.grid(row=0, column=0, columnspan=1, sticky="w")
            self.online_button.grid(row=0, column=1, columnspan=1, sticky="w", padx=(10, 0), pady=0)
            self.copy_preview_label.grid(row=0, column=2, columnspan=1, sticky="e", padx=(16, 10), pady=0)
            self.copy_button.grid(row=0, column=3, sticky="e", pady=0)
            self.copy_preview_label.configure(wraplength=max(width * 0.38, 300), justify="right", anchor="e")
            self.container.rowconfigure(1, weight=1, minsize=0)
            self.container.rowconfigure(2, weight=0, minsize=0)
            panel_padding = 18 if is_dense else 22
            visual_padding = 12 if is_dense else 16
            title_size = 22 if is_dense else 24
            name_size = 19 if is_dense else 21
            number_size = 34 if is_dense else 38
            detail_size, caption_size, button_size = (10, 9, 11) if is_dense else (11, 9, 12)

        self.info_panel.configure(padding=panel_padding)
        self.visual_panel.configure(padding=visual_padding)
        self.title_font.configure(size=title_size)
        self.name_font.configure(size=name_size)
        self.number_font.configure(size=number_size)
        self.detail_font.configure(size=detail_size)
        self.caption_font.configure(size=caption_size)
        self.button_font.configure(size=button_size)
        text_height = 3 if is_dense else 4 if is_compact else 5
        self.online_status_text.configure(font=("Microsoft YaHei UI", max(9, detail_size - 1)), height=text_height)
        self._update_wraplengths()
        self._refresh_result_texts()
        self._draw_hexagram()

    def _update_wraplengths(self):
        padding = 28 if self.is_compact else 44
        width = max(self.info_panel.winfo_width() - padding, 140)
        self.name_label.configure(wraplength=width)
        self.detail_label.configure(wraplength=width)
        self.method_label.configure(wraplength=width)
        self.change_label.configure(wraplength=width)
        self.changed_label.configure(wraplength=width)

    def cast_hexagram(self):
        self.line_values = [self._cast_coin_line() for _ in range(6)]
        self.lines = [LINE_TYPES[value][1] for value in self.line_values]
        self.changed_lines = [1 - line if LINE_TYPES[value][2] else line for line, value in zip(self.lines, self.line_values)]
        self.active_changes = [index for index, value in enumerate(self.line_values, start=1) if LINE_TYPES[value][2]]

        index, name, full_name, palace = self._gua_from_lines(self.lines)
        changed_index, changed_name, changed_full_name, changed_palace = self._gua_from_lines(self.changed_lines)
        self.current_base_gua = (index, name, full_name, palace)
        self.current_changed_gua = (changed_index, changed_name, changed_full_name, changed_palace)

        self.gua_number.set(f"{index:02d}")
        self.gua_name.set(f"{name} · {full_name}")
        self.gua_detail.set(palace)
        self._refresh_result_texts()
        self._update_copy_text(index, name, full_name, palace, changed_index, changed_name, changed_full_name, changed_palace)
        self._set_online_status("卦象已生成。需要联网解卦时，点击“联网解卦”。")
        self._draw_hexagram()

    def open_online_interpretation(self):
        if not self.current_base_gua:
            self._set_online_status("请先抽一卦，再联网解卦。")
            self.copy_preview.set("复制内容：请先抽一卦")
            return

        prompt = self._build_online_query()
        self.clipboard_clear()
        self.clipboard_append(prompt)
        self.update()
        webbrowser.open("https://chatglm.cn/")
        self._set_online_status("已打开智谱清言，并复制联网解卦提示词。\n\n打开网页后粘贴并发送。")

    def _build_online_query(self):
        index, name, full_name, palace = self.current_base_gua
        changed_index, changed_name, changed_full_name, changed_palace = self.current_changed_gua
        question = self.question_var.get().strip() or "综合运势"
        moving = "无变爻" if not self.active_changes else "变爻第" + "、".join(map(str, self.active_changes)) + "爻"
        return (
            "请以周易为体，六爻为用为参考，为下面的问题做一段清晰、具体、可执行的解卦。"
            "请说明本卦含义、变爻影响、变卦趋势、当前建议和需要避免的风险。"
            "不要夸大确定性，也不要替代医疗、法律、投资等专业意见。最后进行总结\n\n"
            f"所问之事：{question}\n"
            f"本卦：{index:02d} {name} · {full_name}（{palace}）\n"
            f"变爻：{moving}\n"
            f"变卦：{changed_index:02d} {changed_name} · {changed_full_name}（{changed_palace}）"
        )

    def _set_online_status(self, text):
        self.online_status_text.configure(state="normal")
        self.online_status_text.delete("1.0", "end")
        self.online_status_text.insert("1.0", text)
        self.online_status_text.configure(state="disabled")

    def copy_hexagram_info(self):
        if not self.current_copy_text:
            self.copy_preview.set("复制内容：请先抽一卦")
            return

        self.clipboard_clear()
        self.clipboard_append(self.current_copy_text)
        self.update()
        self.copy_preview.set(f"已复制：{self.copy_summary}")

    def _update_copy_text(self, index, name, full_name, palace, changed_index, changed_name, changed_full_name, changed_palace):
        self.current_copy_text = "\n".join(
            [
                f"本卦：{index:02d} {name} · {full_name}（{palace}）",
                self.method_detail.get(),
                self.change_lines.get(),
                f"变卦：{changed_index:02d} {changed_name} · {changed_full_name}（{changed_palace}）",
            ]
        )
        self.copy_summary = f"{index:02d} {full_name} → {changed_index:02d} {changed_full_name}"
        self.copy_preview.set(f"复制内容：{self.copy_summary}")

    def _gua_from_lines(self, lines):
        lower = TRIGRAM_BY_LINES[tuple(lines[:3])]
        upper = TRIGRAM_BY_LINES[tuple(lines[3:])]
        palace = f"{upper}上{lower}下"
        index, name, full_name = PALACE_TO_GUA[palace]
        return index, name, full_name, palace

    def _cast_coin_line(self):
        return sum(random.choice((2, 3)) for _ in range(3))

    def _format_method_detail(self):
        values = []
        for index, value in enumerate(self.line_values, start=1):
            line_name = LINE_TYPES[value][0]
            values.append(f"{index}:{value}{line_name}")
        if self.is_compact:
            rows = ["  ".join(values[index:index + 2]) for index in range(0, len(values), 2)]
            return "起卦：\n" + "\n".join(rows)
        rows = ["  ".join(values[:3]), "  ".join(values[3:])]
        return "起卦：" + rows[0] + "\n" + rows[1]

    def _format_change_lines(self):
        if not self.active_changes:
            return "变爻：无"
        if self.is_compact and len(self.active_changes) >= 3:
            return f"变爻：{len(self.active_changes)} 个\n位置：{', '.join(map(str, self.active_changes))}"
        return f"变爻：{len(self.active_changes)} 个，位置 {', '.join(map(str, self.active_changes))}"

    def _format_changed_gua(self, index, name, full_name, palace):
        prefix = "变卦"
        if not self.active_changes:
            prefix = "变卦同本卦"
        if self.is_compact:
            return f"{prefix}：{index:02d} {name} · {full_name}\n{palace}"
        return f"{prefix}：{index:02d} {name} · {full_name}\n{palace}"

    def _refresh_result_texts(self):
        self.method_detail.set(self._format_method_detail())
        self.change_lines.set(self._format_change_lines())
        if self.current_changed_gua:
            self.changed_gua.set(self._format_changed_gua(*self.current_changed_gua))

    def _draw_hexagram(self):
        self.canvas.delete("all")

        width = max(self.canvas.winfo_width(), 180)
        height = max(self.canvas.winfo_height(), 190)
        self._draw_ink_wash(width, height)

        if width < 430 and height >= 330:
            gap = round(min(29, max(21, height / 17)))
            line_width = round(min(width * 0.58, 190))
            stroke = max(8, min(12, round(line_width / 17)))
            top_start_y = round(max(gap * 6.6, height * 0.38))
            bottom_start_y = round(min(height - 40, top_start_y + gap * 6.9))

            self.canvas.create_text(
                width / 2,
                26,
                text="本卦  ↓  变卦",
                fill=COLORS["ink_faint"],
                font=("Microsoft YaHei UI", 12, "bold"),
            )
            self._draw_single_hexagram(width / 2, top_start_y, gap, line_width, stroke, self.lines, "本卦", show_line_names=False)
            self._draw_single_hexagram(width / 2, bottom_start_y, gap, line_width, stroke, self.changed_lines, "变卦", show_line_names=False)
            return

        center_y = round(height / 2 + 10)
        line_width = round(min(width * 0.34, height * 0.72, 240))
        stroke = max(11, min(18, round(line_width / 18)))
        gap = round(min(48, max(34, height / 7.4)))
        start_y = round(center_y + gap * 2.5)
        left_center = width * 0.3
        right_center = width * 0.7
        show_line_names = width >= 360

        if width < 430:
            line_width = round(min(width * 0.25, 140))
            stroke = max(8, min(12, round(line_width / 17)))
            gap = round(min(36, max(24, height / 8.8)))
            start_y = round(center_y + gap * 2.5)
            left_center = width * 0.29
            right_center = width * 0.73

        self.canvas.create_text(
            width / 2,
            max(26, center_y - gap * 3.3),
            text="本卦  →  变卦",
            fill=COLORS["ink_faint"],
            font=("Microsoft YaHei UI", max(12, int(width / 46)), "bold"),
        )

        self._draw_single_hexagram(left_center, start_y, gap, line_width, stroke, self.lines, "本卦", show_line_names=show_line_names)
        self._draw_single_hexagram(right_center, start_y, gap, line_width, stroke, self.changed_lines, "变卦", show_line_names=False)

    def _draw_ink_wash(self, width, height):
        self.canvas.create_rectangle(0, 0, width, height, fill=COLORS["white"], outline="")
        self.canvas.create_rectangle(8, 8, width - 8, height - 8, outline=COLORS["paper_edge"], width=1)

        wash_shapes = [
            (-0.18, -0.12, 0.56, 0.46, COLORS["paper_deep"]),
            (0.58, 0.02, 1.14, 0.40, "#ded7c8"),
            (0.42, 0.58, 1.12, 1.18, "#e2dbcd"),
            (-0.12, 0.62, 0.38, 1.10, "#ebe5d8"),
        ]
        for x1, y1, x2, y2, color in wash_shapes:
            self.canvas.create_oval(
                width * x1,
                height * y1,
                width * x2,
                height * y2,
                fill=color,
                outline="",
                stipple="gray25",
            )

        for offset in range(0, int(width), 34):
            color = COLORS["paper_deep"] if offset % 68 == 0 else "#eee8dc"
            self.canvas.create_line(offset, 12, offset - 80, height - 12, fill=color, width=1)

        self.canvas.create_text(
            width - 30,
            height - 34,
            text="易",
            fill=COLORS["ink"],
            font=("KaiTi", 20, "bold"),
        )
        self.canvas.create_rectangle(width - 46, height - 52, width - 14, height - 18, outline=COLORS["ink"], width=2)

    def _draw_single_hexagram(self, center_x, start_y, gap, line_width, stroke, lines, title, show_line_names):
        title_y = start_y - gap * 5.75
        self.canvas.create_text(
            center_x,
            title_y,
            text=title,
            fill=COLORS["ink"],
            font=("KaiTi", max(14, int(stroke * 1.2)), "bold"),
        )

        for yao_index, solid in enumerate(lines, start=1):
            y = round(start_y - (yao_index - 1) * gap)
            is_changed = yao_index in self.active_changes
            line_name = LINE_TYPES[self.line_values[yao_index - 1]][0]
            line_color = COLORS["ink"] if title == "本卦" else COLORS["ink_soft"]
            label_color = COLORS["ink"] if is_changed else COLORS["ink_faint"]
            x1 = round(center_x - line_width / 2)
            x2 = round(center_x + line_width / 2)

            if solid:
                self._draw_brush_segment(x1, y, x2, y, stroke, line_color)
            else:
                segment = round(line_width * 0.36)
                self._draw_brush_segment(x1, y, x1 + segment, y, stroke, line_color)
                self._draw_brush_segment(x2 - segment, y, x2, y, stroke, line_color)

            if is_changed and title == "本卦":
                marker_size = max(9, stroke)
                self.canvas.create_oval(
                    x2 + 12,
                    y - marker_size / 2,
                    x2 + 12 + marker_size,
                    y + marker_size / 2,
                    fill=COLORS["white"],
                    outline=COLORS["ink"],
                    width=2,
                )

            if show_line_names:
                self.canvas.create_text(
                    x1 - 28,
                    y,
                    text=line_name,
                    fill=label_color,
                    font=("Microsoft YaHei UI", max(11, int(stroke * 0.9)), "bold"),
                    anchor="e",
                )
            else:
                self.canvas.create_text(
                    x2 + 22,
                    y,
                    text="变" if is_changed else "",
                    fill=COLORS["ink"],
                    font=("Microsoft YaHei UI", max(11, int(stroke * 0.9)), "bold"),
                    anchor="w",
                )

    def _draw_brush_segment(self, x1, y1, x2, y2, stroke, color):
        self.canvas.create_line(
            x1,
            y1 + 2,
            x2,
            y2 + 2,
            width=stroke + 3,
            fill=COLORS["wash"],
            capstyle="round",
        )
        self.canvas.create_line(
            x1,
            y1,
            x2,
            y2,
            width=stroke,
            fill=color,
            capstyle="round",
        )
        self.canvas.create_line(
            x1 + 4,
            y1 - max(1, stroke // 5),
            x2 - 4,
            y2 - max(1, stroke // 5),
            width=max(1, stroke // 5),
            fill=COLORS["ink_faint"],
            capstyle="round",
        )


if __name__ == "__main__":
    app = YijingApp()
    app.mainloop()
