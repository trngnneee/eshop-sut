# FR-05 Test Cases - Product Listing and Search

Feature: FR-05 - Product listing and search  
Scope: Web homepage product grid and search behavior  
Source requirement: README.md, FR-05

## Requirement Summary

- The homepage displays all products in a grid.
- Each product displays image, descriptive alt text, product name, and formatted price.
- Search filters products by product name.
- The search keyword must be displayed safely and must not render HTML.
- A loading state is shown while product data is being fetched.
- An empty state is shown when no products match the search.
- The homepage has exactly one `<h1>`.

## Test Case Table

| TC ID | Type | Title | Preconditions | Steps | Test Data (ref) | Expected Result | Priority | Status |
|---|---|---|---|---|---|---|---|---|
| TC-FR05-01 | Positive | Display all products on homepage | Backend and frontend are running; seed products exist | 1. Open homepage<br>2. Wait for product request to finish | data/fr05.json: all_products | Product grid is visible and contains the seeded products | High | Not Run |
| TC-FR05-02 | Positive | Product card shows required fields | Homepage has loaded products | 1. Open homepage<br>2. Inspect each product card | data/fr05.json: all_products | Each product card shows image, product name, formatted price, detail button, and add-to-cart button | High | Not Run |
| TC-FR05-03 | Positive | Product price is formatted with thousands separator and currency | Homepage has loaded products | 1. Open homepage<br>2. Check visible price text | data/fr05.json: price_format | Prices are shown with thousands separators and currency unit | Medium | Not Run |
| TC-FR05-04 | Positive | Search by exact product name | Homepage is open | 1. Enter exact product name<br>2. Submit search | data/fr05.json: exact_match | Only the matching product is shown; search summary displays the keyword | High | Not Run |
| TC-FR05-05 | Positive | Search by partial product name | Homepage is open | 1. Enter partial product name<br>2. Submit search | data/fr05.json: partial_match | All products whose names contain the keyword are shown | High | Not Run |
| TC-FR05-06 | Edge | Search with no matching result | Homepage is open | 1. Enter a keyword that matches no product<br>2. Submit search | data/fr05.json: no_result | No product card is shown and an appropriate empty-state message is visible | High | Not Run |
| TC-FR05-07 | Edge | Search with empty keyword | Homepage is open | 1. Clear search input<br>2. Submit search | data/fr05.json: empty_keyword | Full product list is shown again | Medium | Not Run |
| TC-FR05-08 | Edge | Search keyword with leading and trailing spaces | Homepage is open | 1. Enter keyword with spaces before and after<br>2. Submit search | data/fr05.json: padded_keyword | System handles the keyword without crashing and shows a deterministic result | Medium | Not Run |
| TC-FR05-09 | Negative | Search keyword containing HTML is displayed safely | Homepage is open | 1. Enter HTML payload<br>2. Submit search<br>3. Inspect rendered search summary | data/fr05.json: html_payload | Payload is displayed as plain text; no injected HTML element is rendered | Critical | Not Run |
| TC-FR05-10 | Negative | Search keyword containing script does not execute | Homepage is open | 1. Enter script payload<br>2. Submit search<br>3. Check page state and browser dialog events | data/fr05.json: script_payload | Script is not executed and page remains usable | Critical | Not Run |
| TC-FR05-11 | Negative | SQL injection style payload does not expose unrelated products | Homepage is open | 1. Enter SQL injection-style payload<br>2. Submit search<br>3. Compare returned product names | data/fr05.json: sql_payload | API does not error and does not return products outside the intended search behavior | Critical | Not Run |
| TC-FR05-12 | Accessibility | Product images have descriptive alt text | Homepage has loaded products | 1. Open homepage<br>2. Inspect all product images | data/fr05.json: all_products | Every product image has non-empty descriptive alt text | Medium | Not Run |
| TC-FR05-13 | Semantic HTML | Homepage has exactly one h1 element | Homepage has loaded products | 1. Open homepage<br>2. Count h1 elements in the document | data/fr05.json: h1_rule | Exactly one h1 exists on the page | Medium | Not Run |
| TC-FR05-14 | Loading | Loading state is visible while products are fetched | Product API response can be delayed or intercepted | 1. Delay product API response<br>2. Open homepage<br>3. Observe UI before response completes | data/fr05.json: delayed_api | Loading indicator is visible while waiting for data | Medium | Not Run |

## Coverage Checklist

- [x] At least 12 test cases total for this feature
- [x] At least one Positive case
- [x] At least one Negative case
- [x] At least one Edge case
- [x] Expected results are objectively checkable
- [x] Each case maps to planned data in `data/fr05.json`

## Known Bug Candidates From Static Review

- Search keyword is rendered using `dangerouslySetInnerHTML`, which can violate the safe-display requirement.
- Product image `alt` attribute is empty.
- Loading state is not implemented in the homepage component.
- Empty state is not implemented when the filtered result list is empty.
- The homepage can render more than one `<h1>` when products are present.
- Product search API builds SQL using string interpolation, which creates SQL injection risk.
