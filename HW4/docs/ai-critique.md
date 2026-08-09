# AI Critique (200–300 words, Mandatory)

The AI's most consistent failure mode this assignment was **assuming instead of verifying**. Its
first login script used `getByLabel`, which silently failed against this SUT's DOM (no `htmlFor`)
— it had generated a plausible-looking locator without actually inspecting the rendered page.
Later, in the Cart suite, the AI wrote `page.goto()` between every setup step without noticing
that `CartContext` holds state only in React memory; a full navigation quietly wiped the cart,
turning nearly every multi-step case into a false failure. Neither mistake was a knowledge gap —
Playwright's docs are clear on both points — it was a failure to *check the actual application*
before writing an assertion against it. The AI also, twice, wrote destructive test steps (mutating
a shared product's price, deleting the real seed admin account) without adding cleanup, because it
reasoned about each test case in isolation and never modeled that all three browsers share one
long-lived backend process across a run.

Why did it miss these? Partly prompt quality — early prompts asked for "a test for X" without
demanding the AI first read the relevant source file. Partly a structural blind spot: an LLM
completing one test case at a time doesn't naturally reason about *cross-test* shared state unless
explicitly told to. The bugs that survived longest were exactly the ones with effects delayed past
the current test — corrupted data only surfaced when a *later*, unrelated browser's run failed for
the wrong reason.

The principle I take from this: **an AI-generated test is a hypothesis, not evidence, until it has
actually been run against the real system twice** — once to see it pass for the right reason, once
more on a second browser to catch state it silently depends on. Trusting the first green run is
the mistake; the second run is where the real bugs (in the tests, not just the product) show up.
