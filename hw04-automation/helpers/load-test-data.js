const fs = require('fs');
const path = require('path');

const FR03_JOURNEYS = new Set([
  'fullReset',
  'requestOnly',
  'requestThenInspect',
  'uiContract',
  'backToLogin',
]);

const FR08_JOURNEYS = new Set([
  'guestCartCheckout',
  'guestDirectCheckout',
  'emptyCartCheckout',
  'fullCheckout',
  'inspectCheckout',
  'tamperTotalCheckout',
  'apiCheckoutUnauthorized',
]);

const FR15_JOURNEYS = new Set([
  'uiCreate',
  'uiView',
  'uiEdit',
  'uiEditIsolation',
  'uiDelete',
  'apiCreate',
]);

const FR03_ASSERTIONS = new Set([
  'visible',
  'hidden',
  'containText',
  'attribute',
  'dialog',
  'dialogMatches',
  'url',
  'apiLogin',
  'otpLength',
]);

const FR08_ASSERTIONS = new Set([
  'visible',
  'hidden',
  'containText',
  'attribute',
  'dialog',
  'dialogMatches',
  'url',
  'count',
  'totalReadonly',
  'cartEmpty',
  'orderTotalEquals',
  'apiStatus',
]);

const FR15_ASSERTIONS = new Set([
  'visible',
  'hidden',
  'containText',
  'apiStatus',
  'apiProductExists',
  'apiProductAbsent',
  'apiProductFieldEquals',
  'apiSiblingUnchanged',
  'uiSiblingNameUnchanged',
]);

/**
 * Load and validate external case data (JSON only — never inline in specs).
 *
 * @param {string} relativePath path under test-data/
 * @param {{
 *   minCases?: number,
 *   feature?: 'FR-03' | 'FR-08' | 'FR-15',
 *   allowedJourneys?: Set<string>,
 *   allowedAssertions?: Set<string>,
 * }} [options]
 */
function loadFeatureCases(relativePath, options = {}) {
  const minCases = options.minCases ?? 12;
  const feature = options.feature || 'FR-03';
  const allowedJourneys =
    options.allowedJourneys ||
    (feature === 'FR-08'
      ? FR08_JOURNEYS
      : feature === 'FR-15'
        ? FR15_JOURNEYS
        : FR03_JOURNEYS);
  const allowedAssertions =
    options.allowedAssertions ||
    (feature === 'FR-08'
      ? FR08_ASSERTIONS
      : feature === 'FR-15'
        ? FR15_ASSERTIONS
        : FR03_ASSERTIONS);

  const absolutePath = path.resolve(__dirname, '..', 'test-data', relativePath);

  if (!fs.existsSync(absolutePath)) {
    throw new Error(`Test data file not found: ${absolutePath}`);
  }

  let parsed;
  try {
    parsed = JSON.parse(fs.readFileSync(absolutePath, 'utf8'));
  } catch (err) {
    throw new Error(`Malformed JSON in ${absolutePath}: ${err.message}`);
  }

  const cases = parsed?.cases;
  if (!Array.isArray(cases)) {
    throw new Error(`${absolutePath} must contain a top-level "cases" array`);
  }
  if (cases.length < minCases) {
    throw new Error(
      `${absolutePath} has ${cases.length} case(s); expected at least ${minCases}`,
    );
  }

  const ids = cases.map((c) => c?.id);
  const missingId = ids.findIndex((id) => !id || typeof id !== 'string');
  if (missingId !== -1) {
    throw new Error(`Case at index ${missingId} is missing a string "id"`);
  }

  const seen = new Set();
  for (const id of ids) {
    if (seen.has(id)) {
      throw new Error(`Duplicate case id "${id}" in ${absolutePath}`);
    }
    seen.add(id);
  }

  for (const c of cases) {
    for (const key of ['category', 'purpose', 'journey', 'expected']) {
      if (c[key] === undefined || c[key] === null || c[key] === '') {
        throw new Error(`Case ${c.id} is missing required field "${key}"`);
      }
    }

    if (!allowedJourneys.has(c.journey)) {
      throw new Error(
        `Case ${c.id} has unknown journey "${c.journey}". Allowed: ${[...allowedJourneys].join(', ')}`,
      );
    }

    if (!c.setup || typeof c.setup !== 'object') {
      throw new Error(`Case ${c.id} requires a setup object`);
    }

    if (feature === 'FR-08') {
      if (typeof c.setup.login !== 'boolean') {
        throw new Error(`Case ${c.id} requires setup.login boolean`);
      }
      if (typeof c.setup.seedCartCount !== 'number') {
        throw new Error(`Case ${c.id} requires setup.seedCartCount number`);
      }
    } else if (feature === 'FR-15') {
      const mode = c.setup.authMode;
      if (!['admin', 'user', 'none'].includes(mode)) {
        throw new Error(
          `Case ${c.id} requires setup.authMode of admin|user|none`,
        );
      }
    } else if (typeof c.setup.createUser !== 'boolean') {
      throw new Error(`Case ${c.id} requires setup.createUser boolean`);
    }

    const assertions = c.expected?.assertions;
    if (!Array.isArray(assertions) || assertions.length === 0) {
      throw new Error(`Case ${c.id} expected.assertions must be a non-empty array`);
    }

    for (const assertion of assertions) {
      if (!assertion?.type || !allowedAssertions.has(assertion.type)) {
        throw new Error(
          `Case ${c.id} has unknown assertion type "${assertion?.type}". Allowed: ${[...allowedAssertions].join(', ')}`,
        );
      }
    }
  }

  return { feature: parsed.feature, featureName: parsed.featureName, cases };
}

module.exports = {
  loadFeatureCases,
  FR03_JOURNEYS,
  FR08_JOURNEYS,
  FR15_JOURNEYS,
  FR03_ASSERTIONS,
  FR08_ASSERTIONS,
  FR15_ASSERTIONS,
  // backward-compatible aliases
  ALLOWED_JOURNEYS: FR03_JOURNEYS,
  ALLOWED_ASSERTIONS: FR03_ASSERTIONS,
};
