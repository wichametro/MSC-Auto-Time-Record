# TimeRecord Bot - Quick Setup

## Quick Start

```bash
# 1. Clone
git clone https://github.com/wichametro/MSC-Auto-Time-Record.git
cd MSC-Auto-Time-Record

# 2. Install
pip install -r requirements.txt
python -m playwright install chromium

# 3. Config — copy template แล้วใส่ค่าของตัวเอง
cp .env.template .env.wi

# 4. Run
python "TimeRecord Bot.py"
```

---

## Setup by OS

### macOS

```bash
# ถ้ายังไม่มี Python
brew install python

# Install dependencies
pip3 install -r requirements.txt
python3 -m playwright install chromium

# Config
cp .env.template .env.wi
# แก้ไฟล์ .env.wi ใส่ username/password ของตัวเอง

# Run
python3 "TimeRecord Bot.py"
```

### Windows

1. ติดตั้ง Python จาก https://www.python.org/downloads/ — **ติ๊ก "Add Python to PATH"**
2. เปิด PowerShell:

```powershell
pip install -r requirements.txt
python -m playwright install chromium

# Config
copy .env.template .env.wi
# แก้ไฟล์ .env.wi ใส่ username/password ของตัวเอง

# Run
python "TimeRecord Bot.py"
```

---

## Config (.env.wi)

Copy จาก `.env.template` แล้วแก้ค่า:

```env
DUO_USERNAME=your_duo_username
DUO_PASSWORD=your_duo_password

ESS_USERNAME=your_ess_username
ESS_PASSWORD=your_ess_password
```

> ⚠️ ไฟล์ `.env.wi` ถูก gitignore แล้ว — ไม่ต้องกลัว commit password

---

## ใช้ผ่าน Kiro

Copy prompt นี้แปะในแชท:

> รัน `python3 "TimeRecord Bot.py"` ใน terminal ให้หน่อย (macOS) หรือ `python "TimeRecord Bot.py"` (Windows)

---

## Troubleshooting

| ปัญหา | วิธีแก้ |
|---|---|
| `python: command not found` | ใช้ `python3` (macOS) หรือติดตั้ง Python ใหม่ + Add to PATH (Windows) |
| `No module named 'playwright'` | `pip install -r requirements.txt` |
| `Executable doesn't exist` | `python -m playwright install chromium` |
| Browser ค้าง | ตรวจสอบ VPN — ต้องเข้าถึง `mschrmi.metrosystems.co.th` ได้ |
| Login ไม่ผ่าน | ตรวจค่าใน `.env.wi` |

---

## โครงสร้างไฟล์

```
MSC-Auto-Time-Record/
├── TimeRecord Bot.py    # Bot หลัก
├── requirements.txt     # Dependencies
├── .env.template        # Template config (commit ได้)
├── .env.wi              # Config จริง (gitignored)
├── SETUP.md             # คู่มือนี้
└── browser-data/        # Browser session (gitignored)
```
