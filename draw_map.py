# -*- coding: utf-8 -*-
import os
from PIL import Image, ImageDraw, ImageFont

# 設定字型路徑（Windows 內建微軟正黑體）
FONT_PATH = "C:\\Windows\\Fonts\\msjh.ttc"
if not os.path.exists(FONT_PATH):
    FONT_PATH = "C:\\Windows\\Fonts\\msjh.ttf"  # 備用路徑

def create_fri_sat_map():
    # 創建畫布 (寬 1200, 高 750)，使用高雅溫暖的米色背景
    width, height = 1200, 750
    img = Image.new("RGB", (width, height), "#FDFBF7")
    draw = ImageDraw.Draw(img)
    
    # 載入字型
    title_font = ImageFont.truetype(FONT_PATH, 32)
    subtitle_font = ImageFont.truetype(FONT_PATH, 20)
    card_title_font = ImageFont.truetype(FONT_PATH, 22)
    card_time_font = ImageFont.truetype(FONT_PATH, 16)
    card_body_font = ImageFont.truetype(FONT_PATH, 15)
    
    # 1. 繪製頂部標題欄
    draw.rectangle([(0, 0), (width, 85)], fill="#B85A38") # 磚紅色
    draw.text((width // 2, 42), "台南輕旅行 ➔ 週五與週六路線規劃", font=title_font, fill="#FFFFFF", anchor="mm")
    
    # 2. 繪製路線背景連接線 (圓角彎曲折線)
    # 座標點：台北 -> 新竹 -> 台中 -> 嘉義 -> 歷史博 -> 牛肉鍋
    points = [
        (180, 200), (580, 200), (980, 200),
        (980, 500), (580, 500), (180, 500)
    ]
    # 畫主動線
    draw.line(points, fill="#E6DCD2", width=12) # 質感沙色底線
    # 畫去程方向指示線
    draw.line(points[0:3], fill="#C06C50", width=6) # 磚紅去程
    draw.line(points[2:4], fill="#C06C50", width=6)
    # 畫第二天方向指示線
    draw.line(points[3:6], fill="#4A664A", width=6) # 墨綠第二天
    
    # 3. 景點資料定義
    # 上排：週五 (從左至右)
    # 下排：週六 (從右至左)
    events = [
        {
            "num": "1",
            "title": "台北出發 (自駕起點)",
            "time": "⏰ 週五 16:00 - 17:30",
            "desc": "🚗 提早出發避開下班尖峰\n🚗 開車前往新竹享用晚餐\n💡 行車約 1.5 小時",
            "pos": (180, 200),
            "color": "#C06C50"
        },
        {
            "num": "2",
            "title": "新竹晚餐 (中繼站)",
            "time": "⏰ 週五 17:30 - 19:00",
            "desc": "🍴 推薦「草根廚房」烤鴨\n🍴 或「新竹巨城」吹冷氣\n💡 方便停車與長輩如廁",
            "pos": (580, 200),
            "color": "#C06C50"
        },
        {
            "num": "3",
            "title": "台中逢甲 (週五住宿)",
            "time": "⏰ 週五 20:30 入住飯店",
            "desc": "🛌 辦理入住與行李整理\n⚠️ 逢甲夜市人多且久站累\n💡 長輩休息，年輕人外帶",
            "pos": (980, 200),
            "color": "#C06C50"
        },
        {
            "num": "4",
            "title": "嘉義檜意森活村 (午餐)",
            "time": "⏰ 週六 11:15 - 13:45",
            "desc": "🌳 全台最大日式木造園區\n🌳 地勢極平緩、無階梯\n🍴 午餐：園區輕食/雞肉飯",
            "pos": (980, 500),
            "color": "#4A664A"
        },
        {
            "num": "5",
            "title": "國立臺灣歷史博物館",
            "time": "⏰ 週六 14:45 - 17:00",
            "desc": "🏛️ 懷舊雜貨店與老街景\n🏛️ 冷氣強，動線寬敞平緩\n♿ 免費登記借用輪椅",
            "pos": (580, 500),
            "color": "#4A664A"
        },
        {
            "num": "6",
            "title": "四季溫體牛肉火鍋",
            "time": "⏰ 週六 18:15 (已訂位)",
            "desc": "🍲 台南必吃！鮮嫩溫體牛\n🚗 停海安路地下停車場\n♿ 搭乘無障礙電梯直達",
            "pos": (180, 500),
            "color": "#F4A261" # 橘黃色代表主目的地
        }
    ]
    
    # 4. 繪製卡片與節點
    for ev in events:
        x, y = ev["pos"]
        
        # 繪製發光呼吸節點圓圈
        draw.ellipse([(x - 20, y - 20), (x + 20, y + 20)], fill="#FFFFFF", outline=ev["color"], width=4)
        draw.ellipse([(x - 8, y - 8), (x + 8, y + 8)], fill=ev["color"])
        
        # 繪製序號文字
        draw.text((x, y), ev["num"], font=subtitle_font, fill="#FFFFFF", anchor="mm")
        
        # 繪製卡片背景 (圓角矩形)
        # 上排卡片在節點下方，下排卡片在節點上方
        if y < 350:
            card_box = [(x - 160, y + 35), (x + 160, y + 215)]
        else:
            card_box = [(x - 160, y - 215), (x + 160, y - 35)]
            
        draw.rounded_rectangle(card_box, radius=12, fill="#FFFFFF", outline="#E6DCD2", width=2)
        
        # 繪製卡片頂部小色條
        bar_y = card_box[0][1]
        draw.rounded_rectangle([(card_box[0][0], bar_y), (card_box[1][0], bar_y + 8)], radius=4, fill=ev["color"])
        
        # 寫入卡片內容
        text_x = card_box[0][0] + 15
        text_y = card_box[0][1] + 20
        
        # 景點名稱 (粗體色)
        draw.text((text_x, text_y), ev["title"], font=card_title_font, fill="#2C3B32")
        # 時間
        draw.text((text_x, text_y + 32), ev["time"], font=card_time_font, fill="#C06C50" if ev["color"] != "#4A664A" else "#4A664A")
        # 特色說明
        draw.text((text_x, text_y + 58), ev["desc"], font=card_body_font, fill="#555555", spacing=6)

    # 保存圖片到專案根目錄
    img.save("tainan_trip_fri_sat_map.png")
    print("Success: tainan_trip_fri_sat_map.png generated")

def create_sun_map():
    # 創建畫布 (寬 1200, 高 750)，使用高雅溫暖的米色背景
    width, height = 1200, 750
    img = Image.new("RGB", (width, height), "#FDFBF7")
    draw = ImageDraw.Draw(img)
    
    # 載入字型
    title_font = ImageFont.truetype(FONT_PATH, 32)
    subtitle_font = ImageFont.truetype(FONT_PATH, 20)
    card_title_font = ImageFont.truetype(FONT_PATH, 22)
    card_time_font = ImageFont.truetype(FONT_PATH, 16)
    card_body_font = ImageFont.truetype(FONT_PATH, 15)
    
    # 1. 繪製頂部標題欄
    draw.rectangle([(0, 0), (width, 85)], fill="#4A664A") # 墨綠色
    draw.text((width // 2, 42), "台南輕旅行 ➔ 週日北返路線規劃", font=title_font, fill="#FFFFFF", anchor="mm")
    
    # 2. 繪製路線背景連接線 (圓角彎曲折線)
    # 座標點：台南古蹟 -> 台菜午餐 -> 古坑咖啡 -> 新竹晚餐 -> 台北終點
    points = [
        (180, 200), (580, 200), (980, 200),
        (980, 500), (580, 500)
    ]
    # 畫主動線
    draw.line(points, fill="#E6DCD2", width=12) # 質感沙色底線
    # 畫回程方向指示線 (綠色)
    draw.line(points, fill="#4A664A", width=6)
    
    # 3. 景點資料定義
    events = [
        {
            "num": "1",
            "title": "台南古蹟慢遊",
            "time": "⏰ 週日 10:00 - 12:30",
            "desc": "🏛️ 文學館、林百貨、美二館\n🏛️ 近距離散步，有指針電梯\n💡 多室內冷氣，長輩輕鬆",
            "pos": (180, 200),
            "color": "#F4A261" # 橘黃
        },
        {
            "num": "2",
            "title": "老字號台菜午餐",
            "time": "⏰ 週日 12:30 - 14:00",
            "desc": "🏮 推薦「筑馨居」無菜單台菜\n🏮 百年老厝，軟嫩好入口\n💡 請務必提前預訂桌位",
            "pos": (580, 200),
            "color": "#4A664A"
        },
        {
            "num": "3",
            "title": "彰化八卦山大佛",
            "time": "⏰ 週日 15:20 - 16:20",
            "desc": "⛰️ 俯瞰彰化市景，懷舊地標\n⚠️ 大佛前有階梯，請走斜坡\n💡 可開車至停車場，極近大佛",
            "pos": (980, 200),
            "color": "#4A664A"
        },
        {
            "num": "4",
            "title": "新竹晚餐 (回程休息)",
            "time": "⏰ 週日 17:45 - 19:15",
            "desc": "🍴 北返中繼，吃飽再上路\n🍴 推薦草根廚房烤鴨或巨城\n💡 充足休息，舒緩坐車疲累",
            "pos": (980, 500),
            "color": "#4A664A"
        },
        {
            "num": "5",
            "title": "台北 (溫馨返家)",
            "time": "⏰ 週日 20:30 抵達台北",
            "desc": "🏠 結束3天2夜豐富旅程\n🏠 返回台北溫馨的家\n💡 行程平緩，長輩不費力",
            "pos": (580, 500),
            "color": "#B85A38" # 磚紅
        }
    ]
    
    # 4. 繪製卡片與節點
    for ev in events:
        x, y = ev["pos"]
        
        # 繪製發光呼吸節點圓圈
        draw.ellipse([(x - 20, y - 20), (x + 20, y + 20)], fill="#FFFFFF", outline=ev["color"], width=4)
        draw.ellipse([(x - 8, y - 8), (x + 8, y + 8)], fill=ev["color"])
        
        # 繪製序號文字
        draw.text((x, y), ev["num"], font=subtitle_font, fill="#FFFFFF", anchor="mm")
        
        # 繪製卡片背景 (圓角矩形)
        if y < 350:
            card_box = [(x - 160, y + 35), (x + 160, y + 215)]
        else:
            card_box = [(x - 160, y - 215), (x + 160, y - 35)]
            
        draw.rounded_rectangle(card_box, radius=12, fill="#FFFFFF", outline="#E6DCD2", width=2)
        
        # 繪製卡片頂部小色條
        bar_y = card_box[0][1]
        draw.rounded_rectangle([(card_box[0][0], bar_y), (card_box[1][0], bar_y + 8)], radius=4, fill=ev["color"])
        
        # 寫入卡片內容
        text_x = card_box[0][0] + 15
        text_y = card_box[0][1] + 20
        
        # 景點名稱
        draw.text((text_x, text_y), ev["title"], font=card_title_font, fill="#2C3B32")
        # 時間
        draw.text((text_x, text_y + 32), ev["time"], font=card_time_font, fill="#4A664A" if ev["color"] != "#B85A38" else "#B85A38")
        # 特色說明
        draw.text((text_x, text_y + 58), ev["desc"], font=card_body_font, fill="#555555", spacing=6)

    # 保存圖片到專案根目錄
    img.save("tainan_trip_sun_map.png")
    print("Success: tainan_trip_sun_map.png generated")

if __name__ == "__main__":
    create_fri_sat_map()
    create_sun_map()
