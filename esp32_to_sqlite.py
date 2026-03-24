import serial
import sqlite3
import time

# 請將這裡的 COM 埠號改為你的 ESP32 實際連接在電腦上的埠號 (例如: 'COM3', 'COM4' 等)
SERIAL_PORT = 'COM4' 
BAUD_RATE = 115200

# SQLite 資料庫名稱
DB_NAME = 'aiotdb.db'

def setup_database():
    """初始化並建立 SQLite 資料庫與資料表"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # 建立一個名為 datalog 的資料表，並儲存自動遞增 ID、時間戳記、溫度與濕度
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS datalog (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            temp TEXT,
            humd TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print(f"資料庫 {DB_NAME} 準備就緒。")

def main():
    setup_database()
    
    try:
        # 開啟與 ESP32 的序列埠連線
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"成功連接 {SERIAL_PORT}，正在等待 ESP32 傳送資料...")
        
        while True:
            # 判斷是否接收到序列資料
            if ser.in_waiting > 0:
                # 讀取資料並轉為字串
                line = ser.readline().decode('utf-8').strip()
                if line:
                    print(f"收到來自 ESP32 的資料: {line}")
                    
                    # 假設我們將 ESP32 改為用逗號分隔輸出，例如 "30,60" (溫度,濕度)
                    if ',' in line:
                        parts = line.split(',')
                        if len(parts) == 2:
                            temp = parts[0].strip()
                            humd = parts[1].strip()
                            
                            # 連線到 SQLite 並將溫濕度寫入 aiotdb.db
                            conn = sqlite3.connect(DB_NAME)
                            cursor = conn.cursor()
                            cursor.execute("INSERT INTO datalog (temp, humd) VALUES (?, ?)", (temp, humd))
                            conn.commit()
                            conn.close()
                            
                            print(f"已寫入資料庫 -> 溫度: {temp}, 濕度: {humd}\n")
            time.sleep(0.1)

    except serial.SerialException as e:
        print(f"無法開啟序列埠 {SERIAL_PORT}，請檢查 ESP32 是否連接或埠號是否正確！錯誤訊息: {e}")
    except KeyboardInterrupt:
        print("\n停止讀取資料。")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("序列埠已關閉。")

if __name__ == '__main__':
    main()
