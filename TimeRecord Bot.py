import os
import re
import random
from dotenv import load_dotenv
from playwright.sync_api import Playwright, sync_playwright, expect

load_dotenv(".env.wi")
load_dotenv(".env.template")   # โหลด environment variables จากไฟล์ .env.template

# ตั้งค่า login (อ่านจากไฟล์ .env.template)
duo_username = os.getenv("DUO_USERNAME")
duo_password = os.getenv("DUO_PASSWORD")
ess_username = os.getenv("ESS_USERNAME")
ess_password = os.getenv("ESS_PASSWORD")

if not duo_username or not duo_password:
    raise SystemExit("❌ กรุณาตั้งค่า USERNAME และ PASSWORD ในไฟล์ .env ก่อนรัน")

# ตั้งค่าหมายเหตุ
causes = ["Work from home", "ไปพบลูกค้า", "ไม่ได้แสกนบัตร"]  # หมายเหตุที่คุณต้องการ
cause_weights = [5, 25, 70]                             # น้ําหนักของหมายเหตุ


def select_page_size(page, grid_selector: str, size: str = "100"):
    """Open the Kendo pager dropdown inside a grid and select the given page size."""
    pager_dropdown = page.locator(f"{grid_selector} .k-pager-sizes .k-dropdownlist")
    expect(pager_dropdown).to_be_visible(timeout=10000)
    page.wait_for_timeout(500)

    # Get the aria-controls attribute to find the specific listbox for this dropdown
    listbox_id = pager_dropdown.get_attribute("aria-controls")

    def _is_open():
        if listbox_id:
            return page.evaluate(f"""() => {{
                const el = document.getElementById('{listbox_id}');
                return el && el.getAttribute('aria-hidden') === 'false';
            }}""")
        return pager_dropdown.get_attribute("aria-expanded") == "true"

    # Try multiple strategies to open the dropdown
    dropdown_opened = False
    for attempt in range(3):
        # Strategy 1: Click the dropdown arrow button
        arrow_btn = pager_dropdown.locator(".k-input-button")
        if arrow_btn.is_visible():
            print(f"🔽 Attempt {attempt + 1} - Strategy 1: Clicking arrow button...")
            arrow_btn.click()
            page.wait_for_timeout(500)

        if _is_open():
            print(f"✅ Dropdown opened with Strategy 1 (arrow button) on attempt {attempt + 1}")
            dropdown_opened = True
            break

        # Strategy 2: Click the combobox element itself
        print(f"🔽 Attempt {attempt + 1} - Strategy 2: Clicking combobox container...")
        pager_dropdown.click()
        page.wait_for_timeout(500)

        if _is_open():
            print(f"✅ Dropdown opened with Strategy 2 (combobox click) on attempt {attempt + 1}")
            dropdown_opened = True
            break

        # Strategy 3: Force click with JavaScript
        print(f"🔽 Attempt {attempt + 1} - Strategy 3: JavaScript force click...")
        pager_dropdown.evaluate("el => el.click()")
        page.wait_for_timeout(500)

        if _is_open():
            print(f"✅ Dropdown opened with Strategy 3 (JS click) on attempt {attempt + 1}")
            dropdown_opened = True
            break

        print(f"⚠️ All strategies failed on attempt {attempt + 1}, retrying...")
        page.wait_for_timeout(1000)

    if not dropdown_opened:
        # Last resort: use Kendo widget API to open dropdown
        print("🔽 Last resort: Using Kendo widget API to open dropdown...")
        page.evaluate(f"""() => {{
            const select = document.querySelector('{grid_selector} .k-pager-sizes select[data-role="dropdownlist"]');
            if (select) {{
                const widget = $(select).data('kendoDropDownList');
                if (widget) widget.open();
            }}
        }}""")
        page.wait_for_timeout(500)
        print("✅ Dropdown opened with Kendo widget API (last resort)")

    # Select the desired page size from the specific listbox
    if listbox_id:
        page.locator(f"#{listbox_id}").get_by_role("option", name=size).click()
    else:
        page.get_by_role("option", name=size).click()

    print(f"📄 Page size set to {size}")


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False, channel="chrome")
    context = browser.new_context(
        no_viewport=True
    )
    page = context.new_page()
    page.goto("https://mschrmi.metrosystems.co.th/ESS8/ApproveCenter/FixTimeRequest/List")
    page.wait_for_load_state("networkidle")

    # Check if redirected to Duo Security login
    if "duosecurity.com" in page.url:
        print("🔐 Duo Security login detected, entering credentials...")
        page.get_by_role("textbox", name="Email Address").fill(duo_username + "@metrosystems.co.th")
        page.get_by_role("button", name="Next").click()
        page.get_by_role("textbox", name="Password").click()
        page.get_by_role("textbox", name="Password").fill(duo_password)
        page.get_by_role("button", name="Log in").click()

        # Wait for page to load, then check for "Skip for now" text
        page.wait_for_timeout(10000)
        skip_btn = page.get_by_text("Skip for now")
        if skip_btn.is_visible():
            print("⏭️ 'Skip for now' page detected, clicking skip...")
            skip_btn.click()
        else:
            print("✅ No 'Skip for now' page, continuing...")
    else:
        print("✅ No Duo Security login needed, skipping...")

    # Wait for internal login page or DUO auth to complete
    # Keep checking until we reach the Signin page
    print("⏳ Waiting for DUO auth to complete and reach Signin page...")
    page.wait_for_url("**/ESS8/Member/Signin*", timeout=120000)
    print("✅ Reached Signin page")

    # Now handle internal login
    page.wait_for_load_state("networkidle")
    if page.locator("#signin a").is_visible(timeout=5000):
        print("🔐 Internal login detected, entering credentials...")
        page.get_by_role("textbox", name="Username").click()
        page.get_by_role("textbox", name="Username").fill(ess_username)
        page.get_by_role("textbox", name="Username").press("Tab")
        page.get_by_role("textbox", name="Password").fill(ess_password)
        page.get_by_role("textbox", name="Password").press("Enter")
        page.wait_for_load_state("networkidle")
    else:
        print("✅ No internal login needed, skipping...")

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

    select_page_size(page, "#GridFixTimeRequestDetail", "100")

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
