const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const EVIDENCE_DIR = path.join(__dirname, '..', 'evidence');

const dirs = [
  'web-login',
  'web-register',
  'admin-login',
  'admin-category',
  'mobile-login'
];

dirs.forEach(d => {
  const dirPath = path.join(EVIDENCE_DIR, d);
  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath, { recursive: true });
  }
});

async function runExecution() {
  const browser = await chromium.launch({ headless: true });
  console.log('🚀 Starting GUI Execution & Screenshot Capture...');

  // 1. Web Login Evidence (BUG-GUI-01)
  console.log('--- Executing Web Login Tests ---');
  const webContext = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const pageWeb = await webContext.newPage();
  await pageWeb.goto('http://localhost:5173/login');
  await pageWeb.waitForTimeout(1000);

  // Capture BUG-GUI-01 (Web Login defects)
  const loginTitle = await pageWeb.textContent('h2');
  console.log('Web Login Title found:', loginTitle);
  await pageWeb.screenshot({
    path: path.join(EVIDENCE_DIR, 'web-login', 'BUG-GUI-01_web-login.png'),
    fullPage: true
  });

  // 2. Web Register Evidence (BUG-GUI-02)
  console.log('--- Executing Web Register Tests ---');
  await pageWeb.goto('http://localhost:5173/register');
  await pageWeb.waitForTimeout(1000);

  // Fill registration form with Password123! to trigger regex defect
  const inputs = await pageWeb.$$('input');
  if (inputs.length >= 3) {
    await inputs[0].fill('Dang Dang Khoa');
    await inputs[1].fill('23127207_gui_01@hcmus.edu.vn');
    await inputs[2].fill('Password123!');
  }
  await pageWeb.click('button[type="submit"]');
  await pageWeb.waitForTimeout(1000);

  // Capture BUG-GUI-02 (Register password regex defect & UI Mismatch)
  await pageWeb.screenshot({
    path: path.join(EVIDENCE_DIR, 'web-register', 'BUG-GUI-02_web-register.png'),
    fullPage: true
  });

  // 3. Admin Login Evidence (BUG-GUI-03)
  console.log('--- Executing Admin Login Tests ---');
  const adminContext = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const pageAdmin = await adminContext.newPage();
  
  // Set up dialog handler to capture alert text
  pageAdmin.on('dialog', async dialog => {
    console.log('Captured Admin Dialog:', dialog.message());
    await dialog.accept();
  });

  await pageAdmin.goto('http://localhost:5174/');
  await pageAdmin.waitForTimeout(1000);

  // Fill wrong password to trigger browser alert
  const adminInputs = await pageAdmin.$$('input');
  if (adminInputs.length >= 2) {
    await adminInputs[0].fill('admin@eshop.com');
    await adminInputs[1].fill('WrongPass123');
  }
  
  await pageAdmin.screenshot({
    path: path.join(EVIDENCE_DIR, 'admin-login', 'BUG-GUI-03_admin-login.png'),
    fullPage: true
  });

  // Now login as Admin
  if (adminInputs.length >= 2) {
    await adminInputs[0].fill('admin@eshop.com');
    await adminInputs[1].fill('Admin123!');
  }
  await pageAdmin.click('button');
  await pageAdmin.waitForTimeout(1500);

  // 4. Admin Category Management Evidence (BUG-GUI-04)
  console.log('--- Executing Admin Category Management Tests ---');
  // Click on "Danh mục" tab
  const categoryTab = await pageAdmin.locator('li:has-text("Danh mục")');
  await categoryTab.click();
  await pageAdmin.waitForTimeout(1000);

  // Capture Admin Category screen (showing missing edit button, immediate delete buttons)
  await pageAdmin.screenshot({
    path: path.join(EVIDENCE_DIR, 'admin-category', 'BUG-GUI-04_admin-category.png'),
    fullPage: true
  });

  // 5. Mobile Login Evidence (BUG-GUI-05)
  console.log('--- Executing Mobile Login Tests ---');
  const mobileContext = await browser.newContext({
    viewport: { width: 390, height: 844 },
    deviceScaleFactor: 2,
    isMobile: true,
    hasTouch: true
  });
  const pageMobile = await mobileContext.newPage();
  await pageMobile.goto('http://localhost:8081');
  await pageMobile.waitForTimeout(2000);

  // Navigate to Mobile Login if needed
  const loginNav = pageMobile.locator('text=Đăng nhập');
  if (await loginNav.count() > 0) {
    await loginNav.click();
    await pageMobile.waitForTimeout(1000);
  }

  await pageMobile.screenshot({
    path: path.join(EVIDENCE_DIR, 'mobile-login', 'BUG-GUI-05_mobile-login.png'),
    fullPage: true
  });

  await browser.close();
  console.log('✅ GUI Execution & Screenshot Capture Complete!');
}

runExecution().catch(err => {
  console.error('Execution Error:', err);
  process.exit(1);
});
