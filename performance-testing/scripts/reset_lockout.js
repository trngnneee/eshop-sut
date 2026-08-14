const sqlite3 = require('../../backend/node_modules/sqlite3').verbose();
const path = require('path');

const dbPath = path.resolve(__dirname, '../../backend/database.sqlite');

const db = new sqlite3.Database(dbPath, (err) => {
  if (err) {
    console.error('[reset-lockout] Error opening database:', err.message);
    process.exit(1);
  }
});

db.run('UPDATE users SET login_attempts = 0, locked_until = NULL', function(err) {
  if (err) {
    console.error('[reset-lockout] Failed to reset lockout:', err.message);
    db.close();
    process.exit(1);
  }
  
  const timestamp = new Date().toISOString();
  console.log(`[reset-lockout] Cleared lockout on ${this.changes} users at ${timestamp}`);
  
  db.get('SELECT COUNT(*) AS locked_count FROM users WHERE locked_until IS NOT NULL', (verifyErr, row) => {
    if (verifyErr) {
      console.error('[reset-lockout] Verification query error:', verifyErr.message);
    } else {
      console.log(`[reset-lockout] Verification: active locked users = ${row.locked_count}`);
    }
    db.close();
  });
});
