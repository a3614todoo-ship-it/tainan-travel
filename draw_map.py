# -*- coding: utf-8 -*-
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter


ROOT = Path(__file__).resolve().parent
BACKUP_DIR = ROOT / "backups"
FONT_REGULAR = Path("C:/Windows/Fonts/msjh.ttc")
FONT_BOLD = Path("C:/Windows/Fonts/msjhbd.ttc")


def f(size, bold=False):
    path = FONT_BOLD if bold and FONT_BOLD.exists() else FONT_REGULAR
    return ImageFont.truetype(str(path), size)


def text(draw, xy, value, size, fill="#2c211a", bold=False, anchor=None):
    draw.text(xy, value, font=f(size, bold), fill=fill, anchor=anchor)


def wrap(value, count):
    lines = []
    for raw in value.split("\n"):
        buf = ""
        for ch in raw:
            buf += ch
            if len(buf) >= count:
                lines.append(buf)
                buf = ""
        if buf:
            lines.append(buf)
    return lines


def paper(size):
    img = Image.new("RGB", size, "#fbf4e4")
    px = img.load()
    for y in range(size[1]):
        for x in range(size[0]):
            if (x * 17 + y * 31) % 61 == 0:
                r, g, b = px[x, y]
                px[x, y] = (max(0, r - 7), max(0, g - 6), max(0, b - 4))
    return img


def rounded_shadow(draw, box, radius, fill, outline="#d9b675", width=2):
    x1, y1, x2, y2 = box
    draw.rounded_rectangle((x1 + 6, y1 + 8, x2 + 6, y2 + 8), radius=radius, fill="#d6be91")
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def brush_label(draw, box, color, label):
    x1, y1, x2, y2 = box
    draw.rounded_rectangle(box, radius=18, fill=color)
    for i in range(8):
        draw.line((x1 - 16 + i * 8, y1 + 8 + (i % 3) * 8, x1 + 30 + i * 10, y1 + 4), fill=color, width=8)
        draw.line((x2 - 40 + i * 8, y2 - 8, x2 + 12, y2 - 15 + (i % 3) * 8), fill=color, width=8)
    text(draw, ((x1 + x2) // 2, (y1 + y2) // 2 - 1), label, 34, "#ffffff", True, "mm")


def compass(draw, x, y):
    draw.ellipse((x, y, x + 90, y + 90), fill="#ead3a7", outline="#6a4a2e", width=3)
    text(draw, (x + 45, y + 11), "N", 18, "#6a4a2e", True, "mm")
    draw.polygon([(x + 45, y + 18), (x + 55, y + 48), (x + 45, y + 42), (x + 35, y + 48)], fill="#c95f45", outline="#6a4a2e")
    draw.polygon([(x + 45, y + 72), (x + 55, y + 42), (x + 45, y + 48), (x + 35, y + 42)], fill="#fff6de", outline="#6a4a2e")
    draw.ellipse((x + 39, y + 39, x + 51, y + 51), fill="#6a4a2e")


def camera(draw, x, y):
    draw.rounded_rectangle((x, y + 18, x + 92, y + 82), radius=10, fill="#9b6d43", outline="#4b321f", width=3)
    draw.rectangle((x + 15, y + 6, x + 40, y + 22), fill="#9b6d43", outline="#4b321f", width=3)
    draw.ellipse((x + 31, y + 28, x + 75, y + 72), fill="#f4ecd5", outline="#4b321f", width=3)
    draw.ellipse((x + 43, y + 40, x + 63, y + 60), fill="#2d4053")


def suitcase(draw, x, y):
    draw.rounded_rectangle((x, y + 30, x + 88, y + 125), radius=12, fill="#c78442", outline="#5d351e", width=3)
    draw.arc((x + 24, y, x + 64, y + 44), 180, 360, fill="#5d351e", width=5)
    draw.line((x + 24, y + 54, x + 24, y + 112), fill="#8a542d", width=3)
    draw.line((x + 64, y + 54, x + 64, y + 112), fill="#8a542d", width=3)


def icon(draw, kind, x, y, color="#0b63ad"):
    if kind == "clock":
        draw.ellipse((x, y, x + 58, y + 58), fill="#fff7e5", outline="#765f43", width=3)
        draw.line((x + 29, y + 29, x + 29, y + 12), fill="#765f43", width=3)
        draw.line((x + 29, y + 29, x + 44, y + 34), fill="#765f43", width=3)
    elif kind == "car":
        draw.rounded_rectangle((x, y + 24, x + 70, y + 58), radius=9, fill=color)
        draw.polygon([(x + 14, y + 24), (x + 26, y + 6), (x + 50, y + 6), (x + 62, y + 24)], fill="#d7ecf2", outline=color)
        draw.ellipse((x + 10, y + 52, x + 26, y + 68), fill="#25313a")
        draw.ellipse((x + 48, y + 52, x + 64, y + 68), fill="#25313a")
    elif kind == "food":
        draw.ellipse((x, y + 8, x + 58, y + 58), outline="#9a7141", width=4)
        draw.ellipse((x + 14, y + 22, x + 44, y + 48), fill="#fff5d9", outline="#9a7141", width=2)
        draw.line((x - 14, y + 8, x - 14, y + 62), fill="#9a7141", width=5)
        draw.line((x + 73, y + 8, x + 73, y + 62), fill="#9a7141", width=5)
    elif kind == "hotel":
        draw.rectangle((x + 8, y + 4, x + 58, y + 70), fill="#77a8c8", outline="#2e5972", width=3)
        for yy in (16, 34):
            for xx in (18, 38):
                draw.rectangle((x + xx, y + yy, x + xx + 10, y + yy + 10), fill="#fff4c6")
        draw.rectangle((x + 28, y + 52, x + 40, y + 70), fill="#2e5972")
    elif kind == "bed":
        draw.rectangle((x + 2, y + 34, x + 78, y + 60), fill="#2f6db2")
        draw.rectangle((x + 2, y + 18, x + 20, y + 60), fill="#2f6db2")
        draw.rectangle((x + 23, y + 24, x + 50, y + 38), fill="#cfe1f3")
        draw.line((x + 2, y + 64, x + 2, y + 72), fill="#2f6db2", width=4)
        draw.line((x + 78, y + 64, x + 78, y + 72), fill="#2f6db2", width=4)
    elif kind == "museum":
        draw.polygon([(x + 36, y), (x + 72, y + 24), (x, y + 24)], fill="#d7bd7c", outline="#6f5b34")
        draw.rectangle((x + 8, y + 24, x + 64, y + 70), fill="#efe6ca", outline="#6f5b34", width=2)
        for xx in (17, 33, 49):
            draw.rectangle((x + xx, y + 34, x + xx + 8, y + 70), fill="#aac6c8")
    elif kind == "hotpot":
        draw.ellipse((x, y + 22, x + 86, y + 64), fill="#39434a", outline="#20262a", width=3)
        draw.ellipse((x + 10, y + 28, x + 76, y + 54), fill="#d95b45")
        for cx, cy in [(28, 38), (45, 50), (61, 36)]:
            draw.ellipse((x + cx - 7, y + cy - 7, x + cx + 7, y + cy + 7), fill="#ffd66d")
    elif kind == "tree":
        draw.rectangle((x + 35, y + 40, x + 45, y + 78), fill="#7b5431")
        draw.ellipse((x + 5, y + 8, x + 45, y + 48), fill="#8ab77b")
        draw.ellipse((x + 32, y, x + 76, y + 46), fill="#8ab77b")
    elif kind == "jar":
        draw.rounded_rectangle((x + 18, y + 10, x + 66, y + 76), radius=12, fill="#f2b75e", outline="#6a4b29", width=3)
        draw.rectangle((x + 28, y, x + 56, y + 14), fill="#8c6a45", outline="#6a4b29", width=2)
        text(draw, (x + 42, y + 43), "蜜", 22, "#6a4b29", True, "mm")
    elif kind == "buddha":
        draw.ellipse((x + 31, y, x + 57, y + 26), fill="#d9b26a", outline="#6b5837", width=2)
        draw.rounded_rectangle((x + 18, y + 24, x + 70, y + 78), radius=20, fill="#d9b26a", outline="#6b5837", width=3)


def map_shape(draw, box, labels, route_color):
    x1, y1, x2, y2 = box
    land = [
        (x1 + 210, y1 + 20), (x2 - 50, y1 + 90), (x2 - 20, y1 + 235),
        (x2 - 90, y2 - 65), (x1 + 250, y2 - 20), (x1 + 110, y2 - 95),
        (x1 + 65, y1 + 250), (x1 + 120, y1 + 95),
    ]
    draw.rounded_rectangle(box, radius=20, fill="#dceff2", outline="#3d82bd", width=3)
    draw.polygon(land, fill="#e8efd0", outline="#99b47a")
    for gx, gy in [(x1 + 220, y1 + 195), (x1 + 310, y1 + 320), (x1 + 180, y2 - 95), (x2 - 95, y2 - 135)]:
        draw.polygon([(gx, gy), (gx + 35, gy - 50), (gx + 75, gy)], fill="#9fc18d")
        draw.line((gx, gy, gx + 35, gy - 50, gx + 75, gy), fill="#78a06e", width=2)
    route = []
    for item in labels:
        px, py = item["pos"]
        route.append((x1 + px, y1 + py))
    draw.line(route, fill=route_color, width=8, joint="curve")
    for i in range(0, len(route) - 1):
        x_a, y_a = route[i]
        x_b, y_b = route[i + 1]
        for t in (0.35, 0.65):
            draw.ellipse((x_a + (x_b - x_a) * t - 3, y_a + (y_b - y_a) * t - 3,
                          x_a + (x_b - x_a) * t + 3, y_a + (y_b - y_a) * t + 3), fill="#fff7e6")
    for item in labels:
        px, py = item["pos"]
        x, y = x1 + px, y1 + py
        draw.ellipse((x - 11, y - 11, x + 11, y + 11), fill="#fffdf5", outline=route_color, width=5)
        if "icon" in item:
            icon(draw, item["icon"], x + item.get("dx", 22), y + item.get("dy", -40), item.get("color", route_color))
        rounded_shadow(draw, (x + item.get("lx", 22), y + item.get("ly", -34), x + item.get("lx", 22) + 135, y + item.get("ly", -34) + 55), 18, "#fffdf5", "#c9d7b6", 1)
        text(draw, (x + item.get("lx", 22) + 68, y + item.get("ly", -34) + 27), item["name"], 20, "#1f1f1f", True, "mm")
    text(draw, (x1 + 42, y1 + 95), "N", 25, "#174b83", True, "mm")
    draw.polygon([(x1 + 42, y1 + 115), (x1 + 27, y1 + 170), (x1 + 42, y1 + 155), (x1 + 57, y1 + 170)], fill="#174b83")
    text(draw, (x1 + 55, y1 + 330), "台\n灣\n海\n峽", 24, "#2373b0", True)


def timeline_row(draw, x, y, w, h, n, time_value, title, right, kind, color):
    rounded_shadow(draw, (x, y, x + w, y + h), 14, "#fffdf8", "#9bbbe0" if color == "#0b63ad" else "#efc08b", 2)
    draw.line((x, y + h, x + w, y + h), fill="#e4d2ad", width=1)
    draw.ellipse((x - 42, y + 20, x + 4, y + 66), fill=color)
    text(draw, (x - 19, y + 43), str(n), 24, "#ffffff", True, "mm")
    icon(draw, kind, x + 34, y + 20, color)
    text(draw, (x + 135, y + 22), time_value, 30, color, True)
    text(draw, (x + 135, y + 56), title, 25, "#151515", True)
    draw.line((x + w - 190, y + 8, x + w - 190, y + h - 8), fill="#c8d8eb" if color == "#0b63ad" else "#efd2aa", width=2)
    for i, line in enumerate(wrap(right, 7)):
        text(draw, (x + w - 94, y + 27 + i * 28), line, 21, color, True, "ma")


def section(draw, y, label, color, map_labels, rows, note, note_icon=None):
    brush_label(draw, (520, y + 10, 1138, y + 72), color, label)
    map_shape(draw, (28, y + 75, 470, y + 610), map_labels, color)
    if note:
        rounded_shadow(draw, (50, y + 495, 330, y + 588), 8, "#fff4df", "#d6a56d", 2)
        text(draw, (84, y + 526), note, 21, "#5e351d", True)
    x = 520
    row_y = y + 105
    draw.line((x - 16, row_y + 18, x - 16, row_y + len(rows) * 96 - 30), fill=color, width=6)
    for idx, row in enumerate(rows, start=1):
        timeline_row(draw, x, row_y + (idx - 1) * 96, 600, 82, idx, row["time"], row["title"], row["right"], row["icon"], color)


def create_fri_sat_map():
    img = paper((1200, 1720))
    draw = ImageDraw.Draw(img)
    compass(draw, 28, 14)
    camera(draw, 1078, 18)
    text(draw, (600, 58), "三天二夜行程時間軸與路線", 48, "#3a1d10", True, "mm")
    text(draw, (600, 110), "週五、週六南下行程（最新版）", 25, "#6d4b34", True, "mm")

    friday_labels = [
        {"name": "台北", "pos": (310, 168), "icon": "car", "dx": 18, "dy": 16},
        {"name": "新竹", "pos": (248, 330), "icon": "museum", "dx": 38, "dy": -44, "lx": 30},
        {"name": "台中\n逢甲", "pos": (180, 520), "icon": "car", "dx": 36, "dy": -44, "lx": 38, "ly": -75},
    ]
    friday_rows = [
        {"time": "16:00", "title": "台北出發往新竹", "right": "車程\n1小時30分", "icon": "clock"},
        {"time": "17:30", "title": "新竹晚餐", "right": "停留\n1小時30分", "icon": "food"},
        {"time": "19:00", "title": "前往逢甲入住", "right": "車程\n1小時30分", "icon": "car"},
        {"time": "20:30", "title": "逢甲入住／休息", "right": "住宿\n長輩休息", "icon": "hotel"},
    ]
    section(draw, 120, "週五（台北 → 新竹 → 台中）", "#0b63ad", friday_labels, friday_rows, "北往南\n一路玩下去！")

    saturday_labels = [
        {"name": "台中\n逢甲", "pos": (255, 122), "icon": "car", "dx": 35, "dy": -40},
        {"name": "嘉義\n檜意森活村", "pos": (205, 300), "icon": "tree", "dx": 48, "dy": -48, "lx": 36},
        {"name": "台南", "pos": (165, 505), "icon": "hotpot", "dx": 30, "dy": -56, "lx": 40, "ly": -90},
    ]
    saturday_rows = [
        {"time": "09:30", "title": "台中出發往嘉義", "right": "車程\n1小時45分", "icon": "car"},
        {"time": "11:15", "title": "檜意森活村散步", "right": "停留\n1小時30分", "icon": "tree"},
        {"time": "12:45", "title": "午餐：輕食／雞肉飯", "right": "用餐\n1小時", "icon": "food"},
        {"time": "13:45", "title": "前往臺灣歷史博物館", "right": "車程\n1小時", "icon": "car"},
        {"time": "14:45", "title": "臺灣歷史博物館參觀", "right": "停留\n2小時15分", "icon": "museum"},
        {"time": "17:00", "title": "飯店 Check-in 與休息", "right": "移動\n30分鐘", "icon": "hotel"},
        {"time": "18:15", "title": "四季溫體牛肉火鍋", "right": "晚餐\n已訂位", "icon": "hotpot"},
    ]
    section(draw, 810, "週六（台中 → 嘉義 → 台南）", "#df6b13", saturday_labels, saturday_rows, "慢遊南台灣，\n美食與文化一次滿足！")

    rounded_shadow(draw, (250, 1640, 950, 1696), 12, "#fff7df", "#dfb06b", 2)
    text(draw, (600, 1668), "★ 實際時間可依路況彈性調整", 27, "#6a4a24", True, "mm")
    img.save(ROOT / "tainan_trip_fri_sat_map.png")
    img.save(BACKUP_DIR / "tainan_trip_fri_sat_map.png")


def create_sun_map():
    img = paper((1200, 1500))
    draw = ImageDraw.Draw(img)
    compass(draw, 28, 14)
    camera(draw, 1078, 18)
    suitcase(draw, 36, 960)
    text(draw, (600, 58), "週日安平北返時間軸與路線", 46, "#3a1d10", True, "mm")
    text(draw, (600, 110), "安平樹屋、老街蜜餞、安平午餐，再到八卦山", 24, "#6d4b34", True, "mm")

    labels = [
        {"name": "永康", "pos": (270, 520), "icon": "hotel", "dx": 35, "dy": -48},
        {"name": "安平\n樹屋", "pos": (220, 410), "icon": "tree", "dx": 38, "dy": -60, "lx": 35},
        {"name": "安平\n老街", "pos": (190, 315), "icon": "jar", "dx": 45, "dy": -54, "lx": 36},
        {"name": "彰化\n八卦山", "pos": (250, 185), "icon": "buddha", "dx": 35, "dy": -52, "lx": 36},
        {"name": "新竹", "pos": (310, 120), "icon": "car", "dx": 30, "dy": 20, "lx": 30},
    ]
    map_shape(draw, (28, 170, 470, 1140), labels, "#4a8b64")
    rounded_shadow(draw, (50, 1025, 348, 1115), 8, "#fff4df", "#d6a56d", 2)
    text(draw, (84, 1055), "蜜餞買舊李合興，", 21, "#5e351d", True)
    text(draw, (84, 1087), "午餐留在安平附近！", 21, "#5e351d", True)

    brush_label(draw, (520, 150, 1138, 212), "#4a8b64", "週日（台南 → 安平 → 彰化 → 新竹 → 台北）")
    rows = [
        {"time": "08:30", "title": "飯店早餐＋退房", "right": "整理\n1小時", "icon": "hotel"},
        {"time": "09:30", "title": "永康出發往安平樹屋", "right": "車程\n25-30分", "icon": "car"},
        {"time": "10:00", "title": "安平樹屋／德記洋行", "right": "停留\n50分鐘", "icon": "tree"},
        {"time": "10:50", "title": "安平老街＋舊李合興", "right": "採買\n1小時", "icon": "jar"},
        {"time": "12:00", "title": "安平附近午餐", "right": "用餐\n1小時15分", "icon": "food"},
        {"time": "14:00", "title": "出發往彰化八卦山", "right": "車程\n1小時20分", "icon": "car"},
        {"time": "15:20", "title": "彰化八卦山大佛", "right": "停留\n1小時", "icon": "buddha"},
        {"time": "16:20", "title": "八卦山出發往新竹", "right": "車程\n1小時25分", "icon": "car"},
        {"time": "17:45", "title": "新竹晚餐休息", "right": "用餐\n1小時30分", "icon": "food"},
        {"time": "19:15", "title": "新竹出發回台北", "right": "車程\n1小時15分", "icon": "car"},
        {"time": "20:30", "title": "抵達台北", "right": "返家\n休息", "icon": "bed"},
    ]
    x = 520
    row_y = 240
    step = 96
    draw.line((x - 16, row_y + 18, x - 16, row_y + len(rows) * step - 28), fill="#4a8b64", width=6)
    for idx, row in enumerate(rows, start=1):
        timeline_row(draw, x, row_y + (idx - 1) * step, 600, 82, idx, row["time"], row["title"], row["right"], row["icon"], "#4a8b64")

    rounded_shadow(draw, (250, 1420, 950, 1472), 12, "#fff7df", "#dfb06b", 2)
    text(draw, (600, 1446), "★ 安平老街人多，鎖定蜜餞與伴手禮快買快休息", 23, "#6a4a24", True, "mm")
    img.save(ROOT / "tainan_trip_sun_map.png")
    img.save(BACKUP_DIR / "tainan_trip_sun_map.png")


if __name__ == "__main__":
    create_fri_sat_map()
    create_sun_map()
    print("Success: static timeline map images generated")
