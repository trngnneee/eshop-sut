'use strict';

/**
 * Artillery processor helpers for EShop workload scenarios.
 */

const SEARCH_KEYWORDS = ['iPhone', 'Samsung', 'MacBook', 'AirPods', 'Keychron', 'Laptop'];

function pickSearchKeyword(context, events, done) {
  context.vars.keyword =
    SEARCH_KEYWORDS[Math.floor(Math.random() * SEARCH_KEYWORDS.length)];
  return done();
}

function pickRandomProduct(requestParams, response, context, ee, next) {
  try {
    const body =
      typeof response.body === 'string' ? JSON.parse(response.body) : response.body;
    if (Array.isArray(body) && body.length > 0) {
      const product = body[Math.floor(Math.random() * body.length)];
      context.vars.productId = product.id;
      context.vars.productName = product.name;
      context.vars.productPrice =
        typeof product.price === 'string' ? Number(product.price) : product.price;
      context.vars.quantity = Math.floor(Math.random() * 3) + 1;
    } else {
      // Fallback to seeded catalog (ids 1–5)
      context.vars.productId = (Math.floor(Math.random() * 5) + 1);
      context.vars.productName = 'EShop Product';
      context.vars.productPrice = 1000000;
      context.vars.quantity = 1;
    }
  } catch (_err) {
    context.vars.productId = 1;
    context.vars.productName = 'iPhone 15 Pro Max';
    context.vars.productPrice = 30000000;
    context.vars.quantity = 1;
  }
  return next();
}

function setCheckoutPayload(context, events, done) {
  const price = Number(context.vars.productPrice) || 1000000;
  const qty = Number(context.vars.quantity) || 1;
  context.vars.totalAmount = price * qty;
  context.vars.shippingAddress =
    context.vars.shippingAddress ||
    `${Math.floor(Math.random() * 200) + 1} Nguyen Hue, Q1, TP.HCM`;
  return done();
}

module.exports = {
  pickSearchKeyword,
  pickRandomProduct,
  setCheckoutPayload,
};
