#!/usr/bin/env python3
# ============================================
# Compile ESP32-S3 Code via API
# ============================================

import requests

# 🌐 API endpoint - SỬA LẠI ĐÚNG ENDPOINT
API_URL = "http://3.27.151.15:20111/api/esp32s3/compile"

# 🔧 Board config
BOARD_CONFIG = "esp32:esp32:esp32s3:FlashSize=16M,PSRAM=opi,PartitionScheme=app3M_fat9M_16MB,CDCOnBoot=cdc,USBMode=hwcdc"

# 📝 Arduino code
CODE = '''
#include <Arduino.h>
#include <Wire.h>

#define SDA0 13
#define SCL0 14
#define SDA1 15
#define SCL1 16

#define TCA_ADDR 0x70
#define PORT_COUNT 12

const uint8_t I2C_ADDRS[] = {
  0x29, 0x39, 0x3C, 0x40, 0x44, 0x77
};
const uint8_t ADDR_COUNT = sizeof(I2C_ADDRS) / sizeof(I2C_ADDRS[0]);

TwoWire* buses[2] = { &Wire, &Wire1 };

#define SAMPLES 256

const uint8_t D_MINUS_PINS[PORT_COUNT] = {
  1,2,3,4,5,6,7,8,9,10,11,12
};

const uint8_t D_PLUS_PINS[PORT_COUNT] = {
  48,47,46,45,42,41,40,39,38,37,36,35
};

const uint16_t boundaries[17] = {
  600,800,1000,1200,1400,
  1600,1800,2000,2200,2400,
  2600,2800,3000,3200,3400,
  3600,3800
};

bool    i2cDetected[PORT_COUNT];
uint8_t i2cBus[PORT_COUNT];
uint8_t i2cCh[PORT_COUNT];
uint8_t i2cAddr[PORT_COUNT];
String  i2cDeviceName[PORT_COUNT];

void tcaSelect(TwoWire& i2c, uint8_t ch) {
  if (ch > 7) return;
  i2c.beginTransmission(TCA_ADDR);
  i2c.write(1 << ch);
  i2c.endTransmission();
}

bool devicePresent(TwoWire& i2c, uint8_t addr) {
  i2c.beginTransmission(addr);
  return (i2c.endTransmission() == 0);
}

String detectDeviceName(TwoWire& i2c, uint8_t addr) {
  uint8_t id;

  if (addr == 0x77) {
    i2c.beginTransmission(0x77);
    i2c.write(0xD0);
    if (i2c.endTransmission(false) == 0) {
      i2c.requestFrom(0x77, (uint8_t)1);
      if (i2c.available()) {
        id = i2c.read();
        if (id == 0x61) return "BME680";
      }
    }
  }

  if (addr == 0x29) {
    i2c.beginTransmission(0x29);
    i2c.write(0x00);
    i2c.write(0x00);
    if (i2c.endTransmission(false) == 0) {
      i2c.requestFrom(0x29, (uint8_t)1);
      if (i2c.available()) {
        id = i2c.read();
        if (id == 0xB4) return "VL6180";
      }
    }
  }

  if (addr == 0x3C || addr == 0x3D) {
    return "SSD1306";
  }

  if (addr == 0x29) {
    i2c.beginTransmission(0x29);
    i2c.write(0x92);
    if (i2c.endTransmission(false) == 0) {
      delayMicroseconds(200);
      i2c.requestFrom(0x29, (uint8_t)1);
      if (i2c.available()) {
        id = i2c.read();
        if (id == 0x44 || id == 0x4D) return "TCS3472";
      }
    }
  }

  char buf[20];
  sprintf(buf, "I2C_0x%02X_UNKNOWN", addr);
  return String(buf);
}

uint16_t readAvg(uint8_t pin) {
  analogSetPinAttenuation(pin, ADC_11db);
  uint32_t sum = 0;
  for (int i = 0; i < SAMPLES; i++) {
    sum += analogRead(pin);
  }
  return sum / SAMPLES;
}

void scanAll() {
  memset(i2cDetected, 0, sizeof(i2cDetected));

  for (uint8_t p = 0; p < PORT_COUNT; p++) {
    uint8_t bus = (p < 8) ? 0 : 1;
    uint8_t ch  = (p < 8) ? p : (p - 8);

    TwoWire& i2c = *buses[bus];
    tcaSelect(i2c, ch);
    delay(3);

    for (uint8_t i = 0; i < ADDR_COUNT; i++) {
      uint8_t addr = I2C_ADDRS[i];
      if (devicePresent(i2c, addr)) {
        i2cDetected[p] = true;
        i2cBus[p]     = bus;
        i2cCh[p]      = ch;
        i2cAddr[p]    = addr;
        i2cDeviceName[p] = detectDeviceName(i2c, addr);
        break;
      }
    }
  }

  Serial.println("{");
  Serial.println("  \\"devices\\": [");

  bool first = true;

  for (uint8_t p = 0; p < PORT_COUNT; p++) {
    if (i2cDetected[p]) {
      if (!first) Serial.println(",");
      first = false;

      Serial.printf(
        "    {\\"port\\":%u,\\"commtype\\":\\"i2c\\",\\"bus\\":%u,\\"channel\\":%u,"
        "\\"i2c_address\\":%u,\\"device_name\\":\\"%s\\",\\"found\\":true}",
        p + 1, i2cBus[p], i2cCh[p], i2cAddr[p], i2cDeviceName[p].c_str()
      );
      continue;
    }

    uint16_t adc = readAvg(D_MINUS_PINS[p]);
    int device_id = -1;

    if (adc > 400 && adc < 3800) {
      for (int i = 0; i < 17; i++) {
        if (adc < boundaries[i]) {
          device_id = i + 1;
          break;
        }
      }
    }

    if (device_id == -1) continue;

    if (!first) Serial.println(",");
    first = false;

    Serial.printf(
      "    {\\"port\\":%u,\\"commtype\\":\\"adc\\",\\"d_plus\\":%u,\\"d_minus\\":%u,"
      "\\"adc_raw\\":%u,\\"device_id\\":%d,\\"found\\":true}",
      p + 1, D_PLUS_PINS[p], D_MINUS_PINS[p], adc, device_id
    );
  }

  Serial.println();
  Serial.println("  ]");
  Serial.println("}");
}

void setup() {
  Serial.begin(115200);
  Wire.begin(SDA0, SCL0);
  Wire1.begin(SDA1, SCL1);

  analogReadResolution(12);
  analogSetAttenuation(ADC_11db);

  Serial.println("READY");
}

void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\\n');
    cmd.trim();
    if (cmd == "scan") {
      scanAll();
    }
  }
}
'''

# ============================================
# 📤 COMPILE CODE
# ============================================

print("📤 Sending code to compile...")

response = requests.post(
    API_URL,
    json={
        'code': CODE,
        'board': BOARD_CONFIG,
        'libraries': []  # Thêm libraries nếu cần, ví dụ: ['Adafruit_BME680']
    },
    timeout=300  # 5 phút timeout vì compile có thể lâu
)

# 📊 Kiểm tra response
print(f"Status code: {response.status_code}")
print(f"Content-Type: {response.headers.get('Content-Type', 'unknown')}")

if response.status_code == 200:
    content_type = response.headers.get('Content-Type', '')
    
    if 'application/zip' in content_type:
        # Lưu file ZIP
        with open('bins.zip', 'wb') as f:
            f.write(response.content)
        
        print(f"✅ Compile successful!")
        print(f"📦 Saved: bins.zip ({len(response.content)} bytes)")
        
        # Liệt kê nội dung ZIP
        import zipfile
        try:
            with zipfile.ZipFile('bins.zip', 'r') as zf:
                print("\n📁 ZIP contents:")
                for info in zf.infolist():
                    print(f"   - {info.filename} ({info.file_size} bytes)")
        except Exception as e:
            print(f"⚠️ Could not read ZIP: {e}")
    else:
        # Response là JSON (có thể là lỗi)
        print(f"Response: {response.text}")
else:
    print(f"❌ Compile failed!")
    print(f"Response: {response.text}")
