class ProductListingPage {
  constructor(page) {
    this.page = page;

    this.mainHeading = page.locator("h1").first();
    this.allHeadingsLevel1 = page.locator("h1");

    this.searchForm = page.locator("form").first();
    this.searchInput = this.searchForm.locator('input[type="text"]').first();
    this.searchButton = this.searchForm.locator('button[type="submit"]').first();

    this.productGrid = page.locator(".grid").first();
    this.productCards = page.locator(
      "div.border.rounded.shadow-sm.p-4.flex.flex-col.bg-white",
    );

    this.searchSummary = page.locator("div.mb-4.text-gray-600").first();
    this.errorPanel = page.locator("div.bg-red-100").first();
  }

  async goto() {
    await this.page.goto("/");
  }

  async search(keyword) {
    await this.searchInput.fill(keyword);
    await this.searchButton.click();
  }

  productCardByName(productName) {
    return this.productCards.filter({
      has: this.page.getByRole("heading", { level: 2, name: productName }),
    });
  }

  productName(productName) {
    return this.page.getByRole("heading", { level: 2, name: productName });
  }

  productImage(productName) {
    return this.productCardByName(productName).locator("img").first();
  }

  productPrice(productName) {
    return this.productCardByName(productName).locator("p.text-red-500").first();
  }

  productDetailLink(productName) {
    return this.productCardByName(productName).locator('a[href^="/product/"]').first();
  }

  addToCartButton(productName) {
    return this.productCardByName(productName).locator("button").last();
  }

  async productCardCount() {
    return this.productCards.count();
  }
}

module.exports = { ProductListingPage };
