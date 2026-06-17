# TimeRecord Bot - Setup Guide

คู่มือสำหรับผู้ใช้ใหม่ที่ต้องการรัน `TimeRecord Bot.py` ผ่าน Kiro  
รองรับทั้ง **Windows** และ **macOS**

---

## Quick Start (สรุปสั้น ๆ)

```bash
# 1. Clone repo
git clone <repo-url>
cd "MSC - Auto Time Record"

# 2. ติดตั้ง dependencies
pip install -r requirements.txt
python -m playwright install chromium

# 3. สร้างไฟล์ .env
cp .env.example .env
# แก้ไข .env ใส่ username/password ของตัวเอง

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
git clone <repo-url>
cd "MSC - Auto Time Record"
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

1. คัดลอกไฟล์ `.env.example` เป็น `.env`

```bash
cp .env.example .env        # macOS
copy .env.example .env      # Windows
```

2. เปิดไฟล์ `.env` แล้วแก้ไข:

```env
USERNAME=your_username
PASSWORD=your_password
```

> ⚠️ ไฟล์ `.env` จะไม่ถูก commit ขึ้น Git (อยู่ใน `.gitignore` แล้ว)

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
MSC - Auto Time Record/
├── TimeRecord Bot.py       # ตัว Bot หลัก
├── requirements.txt        # รายการ dependencies
├── .env.example            # ตัวอย่างไฟล์ config (commit ได้)
├── .env                    # config จริง (ไม่ commit)
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

## สำหรับคนที่จะ Push ขึ้น Git (เจ้าของ Repo)

```bash
# เริ่ม Git repo (ถ้ายังไม่ได้ init)
git init

# เพิ่มไฟล์ที่ต้องการ
git add "TimeRecord Bot.py" requirements.txt .env.example .gitignore SETUP.md

# Commit
git commit -m "Initial commit: TimeRecord Bot"

# เชื่อม remote repo (สร้างบน GitHub/GitLab ก่อน)
git remote add origin <repo-url>

# Push
git push -u origin main
```

> สิ่งที่ **ไม่ควร** commit: `.env`, `browser-data/`, `__pycache__/`  
> `.gitignore` จัดการให้แล้ว

---

## หมายเหตุด้านความปลอดภัย

- ❌ ห้าม commit ไฟล์ `.env` ขึ้น Git (มี password)
- ✅ ใช้ `.env.example` เป็นตัวอย่างให้คนอื่น copy ไปใช้
- ✅ โฟลเดอร์ `browser-data/` ถูก ignore แล้ว ไม่ต้องกังวล
