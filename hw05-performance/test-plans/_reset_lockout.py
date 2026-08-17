import sqlite3
from pathlib import Path

db_path = Path(r"c:\DiskD\HCMUS\Semester9\SoftwareTesting\Repo\eshop-sut\backend\database.sqlite")
sql_path = Path(r"c:\DiskD\HCMUS\Semester9\SoftwareTesting\SoftwareTesting-HW\HW5\23127271\test-plans\reset-lockout.sql")
db = sqlite3.connect(str(db_path))
db.executescript(sql_path.read_text(encoding="utf-8"))
row = db.execute(
    "SELECT COUNT(*), IFNULL(SUM(login_attempts),0), "
    "SUM(CASE WHEN locked_until IS NOT NULL THEN 1 ELSE 0 END) "
    "FROM users WHERE email LIKE 'tram%@eshop.com'"
).fetchone()
db.commit()
db.close()
print("tram_users", row[0], "attempts_sum", row[1], "locked", row[2])
