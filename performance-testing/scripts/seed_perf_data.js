const sqlite3 = require('../../backend/node_modules/sqlite3').verbose();
const path = require('path');
const fs = require('fs');

const dbPath = path.resolve(__dirname, '../../backend/database.sqlite');
const dataDir = path.resolve(__dirname, '../data');
const csvPath = path.resolve(dataDir, 'khoa_users.csv');

if (!fs.existsSync(dataDir)) {
  fs.mkdirSync(dataDir, { recursive: true });
}

const db = new sqlite3.Database(dbPath, (err) => {
  if (err) {
    console.error('Error opening database:', err.message);
    process.exit(1);
  }
});

const streetNames = [
  'Nguyen Van Cu', 'Ly Thuong Kiet', 'Cach Mang Thang 8', 'Le Duan',
  'Tran Hung Dao', 'Hai Ba Trung', 'Nguyen Hue', 'Vo Van Kiet',
  'Dien Bien Phu', 'Pasteur', 'Nam Ky Khoi Nghia', 'Pham Ngoc Thach'
];

const productTypes = [
  'Laptop Gaming', 'Ultrabook Pro', 'Smartphone Ultra', 'Wireless Earbuds',
  'Mechanical Keyboard', 'Gaming Mouse', '4K Monitor', 'External SSD',
  'Smartwatch Sport', 'Tablet Max', 'Noise Cancelling Headphone', 'Wi-Fi 6 Router'
];

const baseDescriptions = [
  'Thiet bi cao cap phuc vu nhu cau lam viec chuyen nghiep va giai tri dinh cao voi do ben vuot troi cung thiet ke hien dai.',
  'San pham chinh hang bao hanh 24 thang, ho tro cong nghe moi nhat mang lai trai nghiem nguoi dung muot ma va toi uu.',
  'Hieu nang manh me, thiet ke tinh te sang trong, toi uu hoa dien nang tieu thu va dap ung moi tieu chuan khac khe nhat.',
  'Lua chon hoan hao cho lap trinh vien va game thu voi tinh nang hien dai, vat lieu cao cap cung thoi luong su dung an tuong.'
];

function formatNumber(num, length) {
  return String(num).padStart(length, '0');
}

db.serialize(() => {
  console.log('[seed] Cleaning up previous perf test data...');
  
  db.run("DELETE FROM users WHERE email LIKE 'khoa%@eshop.com'", function(err) {
    if (err) console.error('Error deleting perf users:', err.message);
    const delUsers = this.changes || 0;
    
    db.run("DELETE FROM products WHERE name LIKE 'PERF %'", function(err2) {
      if (err2) console.error('Error deleting perf products:', err2.message);
      const delProducts = this.changes || 0;
      console.log(`[seed] Removed ${delUsers} old perf users, ${delProducts} old perf products`);
      
      // Begin inserting new data in a transaction
      db.run('BEGIN TRANSACTION');
      
      const userStmt = db.prepare(`
        INSERT INTO users (name, email, password, role, login_attempts, locked_until, shipping_address, phone)
        VALUES (?, ?, ?, ?, 0, NULL, ?, ?)
      `);
      
      const usersList = [];
      for (let i = 1; i <= 400; i++) {
        const idStr = formatNumber(i, 3);
        const name = `Khoa Perf User ${idStr}`;
        const email = `khoa${idStr}@eshop.com`;
        const password = 'Test1234!';
        const role = 'user';
        const street = streetNames[(i - 1) % streetNames.length];
        const district = ((i - 1) % 12) + 1;
        const streetNum = ((i * 7) % 250) + 1;
        const shipping_address = `${streetNum} ${street}, Q${district}, TP.HCM`;
        const phone = `09${formatNumber(10000000 + i * 37, 8)}`;
        
        userStmt.run(name, email, password, role, shipping_address, phone);
        usersList.push({ email, password, shipping_address });
      }
      userStmt.finalize();
      console.log('[seed] Inserted 400 users (khoa001..khoa400)');
      
      const prodStmt = db.prepare(`
        INSERT INTO products (name, description, price, imageUrl, category_id)
        VALUES (?, ?, ?, ?, ?)
      `);
      
      for (let i = 1; i <= 500; i++) {
        const idStr = formatNumber(i, 3);
        const pType = productTypes[(i - 1) % productTypes.length];
        const name = `PERF ${pType} ${idStr}`;
        const descBase = baseDescriptions[(i - 1) % baseDescriptions.length];
        const description = `${descBase} Ma dinh danh san pham PERF-${idStr}.`;
        const price = (Math.floor(Math.random() * 490) + 10) * 100000; // 1,000,000 to 50,000,000
        const imageUrl = `https://placehold.co/300x300/png?text=PERF+${idStr}`;
        const category_id = ((i - 1) % 3) + 1;
        
        prodStmt.run(name, description, price, imageUrl, category_id);
      }
      prodStmt.finalize();
      console.log('[seed] Inserted 500 products (PERF ...)');
      
      db.run('COMMIT', (commitErr) => {
        if (commitErr) {
          console.error('Error committing transaction:', commitErr.message);
          return;
        }
        
        // Query products to build CSV
        db.all('SELECT id, name, price FROM products ORDER BY id ASC', (qErr, rows) => {
          if (qErr) {
            console.error('Error querying products for CSV:', qErr.message);
            return;
          }
          
          const csvRows = ['email,password,product_id,quantity,price,total_amount,shipping_address'];
          
          for (let i = 0; i < usersList.length; i++) {
            const u = usersList[i];
            const p = rows[i % rows.length];
            const quantity = (i % 3) + 1;
            const price = p.price;
            const total_amount = price * quantity;
            // Wrap address in double quotes for RFC 4180
            const csvRow = `${u.email},${u.password},${p.id},${quantity},${price},${total_amount},"${u.shipping_address}"`;
            csvRows.push(csvRow);
          }
          
          fs.writeFileSync(csvPath, csvRows.join('\n'), { encoding: 'utf8' });
          console.log(`[seed] Wrote ${path.relative(process.cwd(), csvPath)} (${usersList.length} rows + header)`);
          console.log('[seed] Done.');
          
          db.close();
        });
      });
    });
  });
});
