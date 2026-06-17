---
paths:
  - "lib/**/*.dart"
  - "test/**/*.dart"
---

# Flutter Mobile App Grading Standards

These are the professor's mandatory evaluation criteria for this project.
Every code change to `.dart` files must satisfy all applicable criteria below.

---

## 1. Project Structure — Clear & Modular (10%)

Required directory layout:
```
lib/
  main.dart
  core/
    constants/
    themes/
    routes/
  features/
    auth/
      data/
      domain/
      presentation/
        screens/
        widgets/
    product/
      data/
      domain/
      presentation/
        screens/
        widgets/
    cart/
      ...
```

**Rules:**
- Never put business logic, API calls, or significant UI in `main.dart`
- Each feature lives in its own folder under `features/`
- Screens, widgets, models, and services must be in separate files
- Folder names must reflect their function — no generic names like `utils2/`, `screen3/`

---

## 2. Readable Code (10%)

**Rules:**
- Variable, class, and function names must be descriptive (`productList`, not `x` or `data1`)
- Format code consistently with `dart format`
- No method longer than ~60 lines — split into helpers
- Comments only where the WHY is non-obvious (not what the code does)

---

## 3. Widget Decomposition — Split UI into Small Widgets (10%)

**Rules:**
- `build()` method must not exceed ~50 lines
- Every logical section of a screen must be its own widget (e.g. `ProductImage`, `PriceSection`, `AddToCartButton`)
- Reusable widgets go in `widgets/` — never copy-paste UI across screens
- No "god widget" that renders an entire screen in one class

---

## 4. Logic Separated from UI (10%)

**Rules:**
- `onPressed` / event handlers must NOT contain inline API calls, validation logic, or navigation chains
- Business logic lives in service / repository / BLoC / Cubit — not in widgets
- Widgets only call pre-built methods; they do not compute results themselves
- API calls must go through a data layer (repository or datasource), not directly in `setState`

---

## 5. State Management — Correct & Consistent (10%)

**Rules:**
- Use `setState` only for purely local, ephemeral UI state (e.g. checkbox toggle within one widget)
- App-wide or feature-level state must use BLoC/Cubit (this project uses BLoC pattern)
- No global mutable variables
- Every async operation must expose Loading / Success / Error / Empty states in the UI
- UI must update automatically when state changes — no manual refresh hacks

---

## 6. Navigation — Clean & Correct (8%)

**Rules:**
- All routes defined in a central router (`app_router.dart` or equivalent)
- No hard-coded route strings scattered across screens — use typed route classes or named constants
- Arguments passed between screens via typed parameters (not raw `Object?`)
- Back button works correctly on every screen
- No `Navigator.push` inside business logic layers

---

## 7. Data Modeling — Use Classes, Not Maps (8%)

**Rules:**
- Every entity (Product, User, CartItem, Order) must have a dedicated model class
- Access via `product.name`, NOT `product['name']`
- Models must include `fromJson` / `toJson` if they are serialized from/to API
- No `dynamic` or `Map<String, dynamic>` passed between layers — map at the boundary, pass typed models inward

---

## 8. Error Handling (8%)

**Rules:**
- All `async` calls that can throw must be wrapped in `try/catch` or use `Result<T>` pattern
- Never let the app crash on null data or network failure
- Display user-friendly error messages in the UI (not raw stack traces)
- Validate all form inputs before submission
- Handle the "no internet" / server error case with a visible error state

---

## 9. Responsive UI — No Overflow (8%)

**Rules:**
- Never use fixed widths/heights that will overflow on small screens
- Use `Expanded`, `Flexible`, `FractionallySizedBox`, or `MediaQuery` for sizing
- Wrap scrollable content in `SingleChildScrollView` or `ListView`
- Always wrap top-level screens in `SafeArea`
- Test layout at 360×640 (small) and 428×926 (large) screen sizes
- Zero tolerance for `RenderFlex overflowed` errors at runtime

---

## 10. Code Reuse & Constants (6%)

**Rules:**
- Colors, text strings, padding values, and route names must be defined as constants in `core/constants/`
- No copy-paste of the same UI block across screens — extract to a shared widget
- No magic numbers in layout (`SizedBox(height: 16)` must come from `AppSizes.spacingMd`)
- **All user-facing strings must be i18n-ready:** every `Text`, `SnackBar`, dialog,
  or error/empty-state message must read from `core/constants/app_strings.dart`
  (`AppStrings.xyz`) — never an inline string literal. Dynamic text (e.g.
  `'Added $name to cart'`) must be a static method on `AppStrings`, not built
  inline in the widget. This keeps future multi-language support a one-file change.
  Exceptions: debug/log-only strings and non-UI identifiers (route names, asset
  paths, API endpoints).

Suggested files:
```dart
// core/constants/app_colors.dart
// core/constants/app_strings.dart
// core/constants/app_sizes.dart
// core/routes/app_routes.dart
```

---

## 11. Basic Performance (6%)

**Rules:**
- Use `ListView.builder()` / `GridView.builder()` for any list with dynamic length
- Never call API or async operations inside `build()`
- Use `const` constructors wherever possible
- Don't rebuild the whole screen when only a small widget changes — scope state correctly
- Images loaded from network should be sized and cached (`cached_network_image`)

---

## 12. Extensibility (implicit)

**Rules:**
- Adding a new screen must not require modifying unrelated files
- Adding a new API endpoint must only touch the data layer
- No tight coupling between screens (screen A should not import screen B's internal widgets)

---

## 13. Dart/Flutter Conventions

| Item | Convention |
|------|-----------|
| Classes | `PascalCase` → `ProductCard`, `CartPage` |
| Variables & functions | `camelCase` → `productName`, `getProducts()` |
| Files | `snake_case` → `product_detail_page.dart` |
| Constants | `camelCase` inside class → `AppStrings.addToCart` |

- Run `dart analyze` — zero errors, zero warnings before any commit
- Run `dart format .` to auto-format before commit

---

## Hard Deductions (flag immediately when found)

| Issue | Severity |
|-------|----------|
| All code in `main.dart` | Critical |
| `build()` > 150 lines | High |
| API call directly inside `build()` | High |
| No model classes — raw `Map` everywhere | High |
| Copy-pasted UI blocks across screens | Medium |
| No error handling for async calls | Medium |
| App crashes on null or empty data | High |
| `RenderFlex overflowed` in the running app | Medium |
| Hard-coded colors/strings/sizes outside constants | Low |
| `dart analyze` reports errors at submission | Medium |
