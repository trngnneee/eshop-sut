// Test-only helper that talks directly to the SUT's SQLite database for deterministic
// ARRANGE-phase setup (e.g. simulating "the lockout window has just expired" without
// literally sleeping 3 minutes) and as a secondary oracle for lockout-state assertions.
// Reuses the backend's own already-installed `sqlite3` driver instead of adding a new
// native dependency to this test project.
import path from 'path';

// eslint-disable-next-line @typescript-eslint/no-var-requires
const sqlite3 = require(path.join(__dirname, '../../../backend/node_modules/sqlite3')).verbose();

const DB_PATH = path.join(__dirname, '../../../backend/database.sqlite');

function withDb<T>(fn: (db: any) => Promise<T>): Promise<T> {
  return new Promise((resolve, reject) => {
    const db = new sqlite3.Database(DB_PATH, (err: Error | null) => {
      if (err) return reject(err);
      fn(db)
        .then((result) => db.close((closeErr: Error | null) => (closeErr ? reject(closeErr) : resolve(result))))
        .catch((innerErr) => db.close(() => reject(innerErr)));
    });
  });
}

export interface UserRow {
  id: number;
  email: string;
  login_attempts: number;
  locked_until: string | null;
}

export function getUserState(email: string): Promise<UserRow | undefined> {
  return withDb(
    (db) =>
      new Promise((resolve, reject) => {
        db.get(
          'SELECT id, email, login_attempts, locked_until FROM users WHERE email = ?',
          [email],
          (err: Error | null, row: UserRow) => (err ? reject(err) : resolve(row)),
        );
      }),
  );
}

/** Force `locked_until` to an arbitrary ISO timestamp (or null) to simulate time passing. */
export function forceLockedUntil(email: string, isoTimestampOrNull: string | null): Promise<void> {
  return withDb(
    (db) =>
      new Promise((resolve, reject) => {
        db.run('UPDATE users SET locked_until = ? WHERE email = ?', [isoTimestampOrNull, email], (err: Error | null) =>
          err ? reject(err) : resolve(),
        );
      }),
  );
}

export function deleteUserByEmail(email: string): Promise<void> {
  return withDb(
    (db) =>
      new Promise((resolve, reject) => {
        db.run('DELETE FROM users WHERE email = ?', [email], (err: Error | null) => (err ? reject(err) : resolve()));
      }),
  );
}
