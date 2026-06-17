import os
import re
import random
from dotenv import load_dotenv
from playwright.sync_api import Playwright, sync_playwright, expect

load_dotenv(".env.wi")  # โหลดไฟล์ส่วนตัวก่อน (ถ้ามี)
load_dotenv()          # fallback ไป .env (ถ้า .env.wi ไม่มี)

# ตั้งค่า login (อ่านจากไฟล์ .env)
username = os.getenv("USERNAME", "your_username")
password = os.getenv("PASSWORD", "your_password")

# ตั้งค่าหมายเหตุ
causes = ["Work from home", "ไปพบลูกค้า", "ไม่ได้แสกนบัตร"]  # หมายเหตุที่คุณต้องการ
cause_weights = [5, 25, 70]                             # น้ําหนักของหมายเหตุ


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(
        no_viewport=True
    )
    page = context.new_page()
    page.goto("https://mschrmi.metrosystems.co.th/ESS8/ApproveCenter/FixTimeRequest/List")
    page.get_by_role("textbox", name="Email Address").fill(username + "@metrosystems.co.th")
    page.get_by_role("button", name="Next").click()
    page.get_by_role("textbox", name="Password").click()
    page.get_by_role("textbox", name="Password").fill(password)

    page.get_by_role("button", name="Log in").click()
    page.get_by_role("button", name="Skip for now").click()
    page.get_by_role("textbox", name="Username").click()
    expect(page.locator("#signin a")).to_be_visible(timeout=60000)
    page.get_by_role("textbox", name="Username").click()
    page.get_by_role("textbox", name="Username").fill(username)
    page.get_by_role("textbox", name="Username").press("Tab")
    page.get_by_role("textbox", name="Password").fill(password)
    page.wait_for_load_state("networkidle")
    page.get_by_role("textbox", name="Password").press("Enter")
    page.wait_for_load_state("networkidle")

    page.wait_for_timeout(5000)

    page.goto("https://mschrmi.metrosystems.co.th/ESS8/ApproveCenter/FixTimeRequest/List")
    expect(page.get_by_title("ขอแก้ไข/ปรับปรุงเวลา")).to_be_visible(timeout=60000)
    page.get_by_title("เพิ่ม").click()
    expect(page.get_by_text("เพิ่มการขอบันทึกแก้ไข/ปรับปรุงเวลา")).to_be_visible()
    page.locator("#redio").get_by_role("insertion").click()
    expect(page.locator("#content10")).to_be_visible()
    page.locator("#RangeStartDate").click()
    page.locator("div:nth-child(38) > .datepicker-days > .table-condensed > thead > tr > .prev > .glyphicon").click()
    page.get_by_role("cell", name="16").click()
    page.locator("div:nth-child(39) > .datepicker-days > .table-condensed > thead > tr > .next > .glyphicon").click()
    page.get_by_role("cell", name="15").click()
    page.get_by_text("แสดงข้อมูลการมาทำงาน").click()

    expect(page.locator("#GridFixTimeRequestDetail").get_by_role("combobox", name="Page sizes drop down")).to_be_visible()
    page.locator("#GridFixTimeRequestDetail").get_by_role("combobox", name="Page sizes drop down").click()
    page.wait_for_timeout(500)
    page.get_by_role("option", name="100").click()

    page.wait_for_timeout(2000)

    # Target the edit icon span directly (icon-edit-s edit-fix-time)
    edit_icons = page.locator("span.icon-edit-s.edit-fix-time")
    count = edit_icons.count()
    print(f"Found {count} edit buttons")

    for i in range(count):
        # Click the edit icon in the i-th row
        page.locator("span.icon-edit-s.edit-fix-time").nth(i).click()
        page.wait_for_timeout(1000)

        # Read the date from the edit form's DateIn1 field
        date_text = page.locator("#DateIn1").input_value()

        cause = random.choices(causes, weights=cause_weights)[0]
        print(f"[{i+1}/{count}] Editing row date: {date_text} | เหตุผล: {cause}")

        page.locator("#txtCauseType").select_option(cause)
        page.get_by_role("button", name="บันทึก").click()
        page.wait_for_timeout(2000)
        
    page.pause()
    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
