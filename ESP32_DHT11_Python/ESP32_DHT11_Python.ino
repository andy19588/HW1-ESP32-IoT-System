#include <SimpleDHT.h>

// 定義 DHT11 連接的腳位
int pinDHT11 = 15; // ESP32 GPIO15
SimpleDHT11 dht11;

void setup() {
  // 將鮑率設定為 115200，與 Python 程式碼保持一致
  Serial.begin(115200);
  delay(10);
  Serial.println("ESP32 Sensor Started...");
}

void loop() {
  byte temperature = 0;
  byte humidity = 0;
  int err = SimpleDHTErrSuccess;

  // 讀取感測器資料
  if ((err = dht11.read(pinDHT11, &temperature, &humidity, NULL)) != SimpleDHTErrSuccess) {
    // 如果讀取失敗，印出錯誤訊息 (Python 讀到這個不會寫入，因為沒有逗號或格式不符)
    Serial.print("Read DHT11 failed, err=");
    Serial.println(err);
    delay(2000);
    return;
  }

  // ============== 關鍵修改 ==============
  // 為了讓 Python 程式能輕鬆讀取，我們只輸出「溫度,濕度」這樣的純粹格式
  // 例如： 30,60
  Serial.print((int)temperature);
  Serial.print(",");
  Serial.println((int)humidity);

  // 每 3 秒讀取並傳送一次
  delay(3000);
}
