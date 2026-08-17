# BEFORE any JMeter run (23127271)

The CSV users **do not exist** in a fresh EShop seed. Seed only has `admin@eshop.com` and `test@eshop.com`.

**If you skip this, every `POST /api/login` returns 401** and Load / Stress / Spike / soak are invalid.

## Preflight (in order)

1. Start the SUT: `http://localhost:3000`
2. Register all **100** accounts **once per seed** (script skips emails that already login):

   ```bash
   cd SoftwareTesting-HW/HW5/23127271/test-plans
   node generate-tram-users.js --register
   ```

   Expect 100× HTTP 200 (or SKIP if already registered). Password: `Test1234!`
3. Spot-check: login as `tram01@eshop.com` / `Test1234!` → 200 + `token`
4. Then open / run the `.jmx` plans

Do **not** use `test@eshop.com` in JMeter (shared by the group).

After a **re-seed** or SUT restart that runs `initDatabase()` (it `DROP`s `users`), register again. Lockout reset (`reset-lockout.sql`) does **not** create accounts.
