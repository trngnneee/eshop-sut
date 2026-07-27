# Workload Model - EShop Performance Testing

## 1. Objective
To simulate realistic user behavior on the EShop application, allowing the team to measure response times, throughput, and error rates under representative loads, and to test application stability during peak traffic spikes.

## 2. EShop User Actions and Distribution
Users navigating EShop typically perform a sequence of search, view, and transactional actions. We model these using the following proportions:

- **Browse/Search Products (60%)**: Users land on the homepage, search for items, or paginate through product grids.
- **View Product Details (25%)**: Users click on a specific product page to view description, price, and reviews.
- **Add to Cart (10%)**: Users select a product option and add it to their session shopping cart.
- **Checkout Flow (5%)**: Users proceed to the checkout form, input shipping data, and complete the order.

## 3. Test Profiles

### A. Baseline Test Profile (Load Test)
- **Target virtual users (VUs)**: 50 concurrent VUs.
- **Ramp-up**: 1 minute.
- **Steady state duration**: 3 minutes.
- **Ramp-down**: 1 minute.
- **Purpose**: Measure baseline latencies (p50, p95, p99) and resource usage under normal operating conditions.
- **Baseline Scripts**: `[Link evidence here]`
- **Baseline Execution Screenshot**: `[Insert baseline test execution screenshot here]`

### B. Spike Test Profile
- **Target virtual users (VUs)**: Jump from 50 to 500 VUs.
- **Ramp-up duration**: 30 seconds.
- **Steady state at peak**: 1 minute.
- **Ramp-down**: 30 seconds.
- **Purpose**: Evaluate if EShop crashes, locks its database, or drops requests under sudden traffic bursts.
- **Spike Scripts**: `[Link evidence here]`
- **Spike Execution Screenshot**: `[Insert baseline test execution screenshot here]`

## 4. Performance Metrics to Collect
- **Response Time / Latency**: Average, Median (p50), 95th Percentile (p95), and 99th Percentile (p99) `[To be filled after execution]`
- **Throughput**: Requests per second (RPS) `[To be filled after execution]`
- **Error Rate**: Percentage of failed requests (HTTP 5xx, 4xx, connection timeouts) `[To be filled after execution]`
- **System Bottlenecks**: CPU/Memory utilization (if monitored) or application crashes `[To be filled after execution]`

## 5. Workload Rationale
This workload distribution reflects a standard e-commerce funnel where the majority of traffic is read-intensive (browsing/searching) and a smaller, high-value percentage is write-intensive (adding to cart, checkout). Simulating this distribution ensures that database locks or session conflicts are tested realistically without overwhelming the transactional database with invalid checkout requests.
