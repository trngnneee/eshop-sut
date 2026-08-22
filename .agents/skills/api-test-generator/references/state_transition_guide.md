# Stage B — State Transition Guide

Applies to any resource whose lifecycle is described in the spec as a
sequence of statuses (the assignment's canonical example is FR-10, the
order state machine: `pending → confirmed → shipping → delivered`, plus
cancellation rules).

## Procedure

1. **Reconstruct the state diagram from the spec.** List every state, every
   legal transition (state → state, and which action/endpoint triggers it),
   and every explicitly forbidden transition or cancellation rule (e.g.
   "an order can only be cancelled while `pending` or `confirmed`").
2. **Generate the legal-path matrix.** For each legal transition, one test
   case: precondition = resource currently in state X, action = the
   triggering call, expected = resource now in state Y (verify via a
   follow-up GET if the API doesn't return the new state directly).
3. **Generate the illegal-transition matrix.** This is the higher-value set
   and the one AI tends to under-generate from a single prompt — be
   deliberate:
   - Skipping a state (e.g. `pending → shipping` directly).
   - Reverse transition (e.g. `delivered → pending`).
   - Acting on a terminal state (e.g. cancelling an already-`delivered`
     order, confirming an already-`cancelled` order).
   - Self-transition where not idempotent (e.g. confirming a
     `confirmed` order twice — does it error or silently no-op? The spec
     should say; if it doesn't, that's worth flagging as ambiguous in the
     audit).
   - Concurrent/racing transitions: two requests attempting different valid
     transitions on the same resource at nearly the same time (useful for
     the "Extend" stage if hard to script directly in Postman — you can
     still describe the case and note the concurrency caveat).
4. **Cross-role transitions.** If different roles can trigger different
   transitions (e.g. only admin can mark `shipping → delivered`), add cases
   where a lower-privileged role attempts a transition it shouldn't be able
   to trigger — this doubles as a security (SEC) case; cross-reference it
   in both stages rather than picking one.

## Output

Each case: `"stage": "state_transition"`, `"category"` set to
`legal-transition` or `illegal-transition`, `"preconditions"` stating the
starting state explicitly, and `"expected.status"` reflecting whether the
API should accept (2xx + new state) or reject (4xx/409 + unchanged state)
the transition.
