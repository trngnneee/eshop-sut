// Platform definitions for the Task 3 cross-browser / cross-platform run.
// Each entry = one "platform" in the sense of the assignment: one rendering
// engine + one OS/device combination that the Task 1 checklist is re-executed on.

import { chromium, firefox, webkit, devices } from 'playwright';

export const HOST_OS = 'macOS 15.5 (24F74)';
export const HOST_DEVICE = 'MacBook Pro (Apple Silicon) — 2560×1664 Retina';

export const PLATFORMS = [
  {
    key: 'P1-chromium-macos',
    label: 'Chrome / Chromium — macOS',
    engine: 'Blink (Chromium)',
    browserType: chromium,
    // Real windowed browser, not headless shell, so the screenshots come from the
    // same rendering path a human user would see.
    launch: {
      headless: false,
      args: [
        '--window-position=0,0',
        '--window-size=1300,900',
        '--disable-features=TranslateUI',
        '--hide-crash-restore-bubble',
      ],
    },
    contextOptions: { viewport: { width: 1280, height: 800 } },
    os: HOST_OS,
    device: HOST_DEVICE,
  },
  {
    key: 'P2-firefox-macos',
    label: 'Firefox — macOS',
    engine: 'Gecko (Firefox)',
    browserType: firefox,
    launch: { headless: false },
    contextOptions: { viewport: { width: 1280, height: 800 } },
    os: HOST_OS,
    device: HOST_DEVICE,
  },
  {
    key: 'P3-webkit-macos',
    label: 'Safari / WebKit — macOS',
    engine: 'WebKit (Safari)',
    browserType: webkit,
    launch: { headless: false },
    contextOptions: { viewport: { width: 1280, height: 800 } },
    os: HOST_OS,
    device: HOST_DEVICE,
  }
];

export function resolvePlatforms(keys) {
  if (!keys || keys.length === 0) return PLATFORMS.filter((p) => !p.optional);
  if (keys.length === 1 && keys[0] === 'all') return PLATFORMS;
  return keys.map((k) => {
    const found = PLATFORMS.find((p) => p.key === k || p.key.includes(k));
    if (!found) throw new Error(`Unknown platform: ${k}`);
    return found;
  });
}
