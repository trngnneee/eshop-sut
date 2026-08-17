-- P02 lockout reset for Search-to-buy (23127271)
-- This does NOT create accounts. Before the first JMeter run, register tram01–tram50:
--   node generate-tram-users.js --register
-- See BEFORE-RUN.md.
-- Run against Repo/eshop-sut/backend/database.sqlite WHILE the SUT may stay up
-- (better-sqlite/sqlite3 file lock: stop Node if this fails with "database is locked").
--
-- Does NOT drop tables. Re-seed (node database.js / server restart that calls initDatabase)
-- DROPS users and would delete tram01–tram50 — then re-run:
--   node generate-tram-users.js --register

UPDATE users
SET login_attempts = 0,
    locked_until = NULL
WHERE email LIKE 'tram%@eshop.com';

SELECT email, login_attempts, locked_until
FROM users
WHERE email LIKE 'tram%@eshop.com'
ORDER BY email;
