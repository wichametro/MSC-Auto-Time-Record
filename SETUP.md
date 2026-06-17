# TimeRecord Bot - Setup Guide

คู่มือสำหรับผู้ใช้ใหม่ที่ต้องการรัน `TimeRecord Bot.py` ผ่าน Kiro  
รองรับทั้ง **Windows** และ **macOS**

---

## Quick Start (สรุปสั้น ๆ)

```bash
# 1. Clone repo
git clone https://github.com/wichametro/MSC-Auto-Time-Record.git
cd MSC-Auto-Time-Record

# 2. ติดตั้ง dependencies
pip install -r requirements.txt
python -m playwright install chromium

# 3. แก้ไข .env ใส่ username/password ของตัวเอง

# 4. รัน
python "TimeRecord Bot.py"
```

---

## รายละเอียดทีละ Step

### Step 1: ติดตั้ง Python (3.9+)

#### macOS

```bash
# ตรวจสอบว่ามี Python หรือยัง
python3 --version

# ถ้ายังไม่มี ให้ติดตั้งผ่าน Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python
```

#### Windows

1. ไปที่ https://www.python.org/downloads/
2. ดาวน์โหลด Python เวอร์ชันล่าสุด (3.9 ขึ้นไป)
3. ตอนติดตั้ง **ติ๊กช่อง "Add Python to PATH"** (สำคัญมาก!)
4. กด Install Now

```powershell
# ตรวจสอบว่าติดตั้งสำเร็จ
python --version
```

---

### Step 2: Clone โปรเจกต์จาก Git

```bash
git clone https://github.com/wichametro/MSC-Auto-Time-Record.git
cd MSC-Auto-Time-Record
```

---

### Step 3: ติดตั้ง Dependencies

#### macOS

```bash
pip3 install -r requirements.txt
python3 -m playwright install chromium
```

#### Windows

```powershell
pip install -r requirements.txt
python -m playwright install chromium
```

---

### Step 4: ตั้งค่า Username & Password

เปิดไฟล์ `.env` แล้วแก้ไขใส่ค่าของตัวเอง:

```env
USERNAME=your_username
PASSWORD=your_password
```

> ⚠️ หลังแก้แล้ว อย่า commit กลับขึ้น Git (เพราะมี password จริง)

---

### Step 5: รัน Bot

#### ผ่าน Terminal ใน Kiro

เปิด Terminal (`Ctrl+\`` หรือ `Cmd+\`` บน macOS):

**macOS:**
```bash
python3 "TimeRecord Bot.py"
```

**Windows:**
```powershell
python "TimeRecord Bot.py"
```

#### ผ่าน Kiro Chat

พิมพ์ในแชท:
> "รัน TimeRecord Bot.py ให้หน่อย"

---

## โครงสร้างไฟล์ใน Repo

```
MSC-Auto-Time-Record/
├── TimeRecord Bot.py       # ตัว Bot หลัก
├── requirements.txt        # รายการ dependencies
├── .env                    # ไฟล์ config (clone มาแล้วแก้ username/password ได้เลย)
├── .gitignore              # ไฟล์ที่ไม่ให้ Git track
├── SETUP.md                # คู่มือนี้
└── browser-data/           # ข้อมูล browser session (ไม่ commit)
```

---

## Troubleshooting

| ปัญหา | วิธีแก้ |
|---|---|
| `python: command not found` | ลอง `python3` แทน (macOS) หรือติดตั้ง Python ใหม่แล้วติ๊ก Add to PATH (Windows) |
| `No module named 'playwright'` | รัน `pip install -r requirements.txt` |
| `No module named 'dotenv'` | รัน `pip install python-dotenv` |
| `Executable doesn't exist` | รัน `python -m playwright install chromium` |
| Browser เปิดแล้วค้าง | ตรวจสอบ VPN — ต้องเข้าถึง `mschrmi.metrosystems.co.th` ได้ |
| Login ไม่ผ่าน | ตรวจสอบ USERNAME/PASSWORD ในไฟล์ `.env` |

---

## Repository

- **GitHub:** https://github.com/wichametro/MSC-Auto-Time-Record
- **Visibility:** Public (ใครก็ clone ได้)

---

## หมายเหตุด้านความปลอดภัย

- ⚠️ หลัง clone มาแล้วแก้ `.env` ใส่ password จริง อย่า push กลับขึ้น Git
- ✅ โฟลเดอร์ `browser-data/` ถูก ignore แล้ว ไม่ต้องกังวล
