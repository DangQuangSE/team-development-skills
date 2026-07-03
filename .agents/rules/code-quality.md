# Code Quality Rules (HARD ENFORCEMENT)

## Type Safety
- All new code must include type hints/annotations.
- No `any`, `object`, or untyped parameters.
- Use strict type checking where the language supports it.

## Error Handling
- Every external call (file I/O, network, DB) must have try/except or equivalent.
- Do NOT silence exceptions. Log or re-raise with context.
- User-facing errors must be human-readable.

## Testing
- Every new function must have at least one test.
- Tests must be in the same PR/commit as the code they test.
- All tests must pass before marking a step complete.

## Security
- Validate all external input. Never trust user input directly.
- Use parameterized queries, not string interpolation, for all database operations.
- No eval/exec of dynamic strings in production code.

## Performance
- No O(n²) or worse algorithms where O(n) or O(log n) exists.
- N+1 query patterns are forbidden. Use batch loading.
- Cache expensive operations. Document cache invalidation strategy.
