# Advanced HTTP/2 Conformance Insights

## Test Type Analysis

| Proxy | Error Tests Conformance | Ignore Tests Conformance |
|-------|----------------------|----------------------|
| Nghttpx | 66.2% | 90.9% |
| HAproxy | 72.7% | 36.4% |
| Apache | 72.1% | 45.5% |
| Caddy | 63.0% | 27.3% |
| Node | 50.6% | 90.9% |
| Envoy | 54.5% | 45.5% |
| H2O | 44.8% | 72.7% |
| Cloudflare | 39.4% | 81.8% |
| Mitmproxy | 3.2% | 36.4% |

## Frame Type Analysis


### CONTINUATION Frame

| Proxy | Conformant | Non-Conformant | Total Tests |
|-------|------------|----------------|-------------|
| Nghttpx | 9 (100.0%) | 0 (0.0%) | 9 |
| HAproxy | 9 (100.0%) | 0 (0.0%) | 9 |
| Apache | 9 (100.0%) | 0 (0.0%) | 9 |
| Caddy | 8 (88.9%) | 1 (11.1%) | 9 |
| Node | 6 (66.7%) | 3 (33.3%) | 9 |
| Envoy | 7 (77.8%) | 2 (22.2%) | 9 |
| H2O | 7 (77.8%) | 2 (22.2%) | 9 |
| Cloudflare | 6 (66.7%) | 3 (33.3%) | 9 |
| Mitmproxy | 0 (0.0%) | 9 (100.0%) | 9 |

### DATA Frame

| Proxy | Conformant | Non-Conformant | Total Tests |
|-------|------------|----------------|-------------|
| Nghttpx | 21 (70.0%) | 9 (30.0%) | 30 |
| HAproxy | 20 (66.7%) | 10 (33.3%) | 30 |
| Apache | 24 (80.0%) | 6 (20.0%) | 30 |
| Caddy | 19 (63.3%) | 11 (36.7%) | 30 |
| Node | 18 (60.0%) | 12 (40.0%) | 30 |
| Envoy | 18 (60.0%) | 12 (40.0%) | 30 |
| H2O | 15 (50.0%) | 15 (50.0%) | 30 |
| Cloudflare | 16 (53.3%) | 14 (46.7%) | 30 |
| Mitmproxy | 0 (0.0%) | 30 (100.0%) | 30 |

### HEADERS Frame

| Proxy | Conformant | Non-Conformant | Total Tests |
|-------|------------|----------------|-------------|
| Nghttpx | 52 (51.0%) | 50 (49.0%) | 102 |
| HAproxy | 60 (58.8%) | 42 (41.2%) | 102 |
| Apache | 58 (56.9%) | 44 (43.1%) | 102 |
| Caddy | 43 (42.2%) | 59 (57.8%) | 102 |
| Node | 35 (34.3%) | 67 (65.7%) | 102 |
| Envoy | 45 (44.1%) | 57 (55.9%) | 102 |
| H2O | 41 (40.2%) | 61 (59.8%) | 102 |
| Cloudflare | 36 (35.0%) | 67 (65.0%) | 103 |
| Mitmproxy | 1 (1.0%) | 102 (99.0%) | 103 |

### PING Frame

| Proxy | Conformant | Non-Conformant | Total Tests |
|-------|------------|----------------|-------------|
| Nghttpx | 2 (100.0%) | 0 (0.0%) | 2 |
| HAproxy | 2 (100.0%) | 0 (0.0%) | 2 |
| Apache | 2 (100.0%) | 0 (0.0%) | 2 |
| Caddy | 2 (100.0%) | 0 (0.0%) | 2 |
| Node | 2 (100.0%) | 0 (0.0%) | 2 |
| Envoy | 1 (50.0%) | 1 (50.0%) | 2 |
| H2O | 2 (100.0%) | 0 (0.0%) | 2 |
| Cloudflare | 1 (50.0%) | 1 (50.0%) | 2 |
| Mitmproxy | 0 (0.0%) | 2 (100.0%) | 2 |

### PRIORITY Frame

| Proxy | Conformant | Non-Conformant | Total Tests |
|-------|------------|----------------|-------------|
| Nghttpx | 1 (50.0%) | 1 (50.0%) | 2 |
| HAproxy | 2 (100.0%) | 0 (0.0%) | 2 |
| Apache | 2 (100.0%) | 0 (0.0%) | 2 |
| Caddy | 2 (100.0%) | 0 (0.0%) | 2 |
| Node | 2 (100.0%) | 0 (0.0%) | 2 |
| Envoy | 1 (50.0%) | 1 (50.0%) | 2 |
| H2O | 1 (50.0%) | 1 (50.0%) | 2 |
| Cloudflare | 1 (50.0%) | 1 (50.0%) | 2 |
| Mitmproxy | 0 (0.0%) | 2 (100.0%) | 2 |

### PUSH_PROMISE Frame

| Proxy | Conformant | Non-Conformant | Total Tests |
|-------|------------|----------------|-------------|
| Nghttpx | 14 (100.0%) | 0 (0.0%) | 14 |
| HAproxy | 14 (100.0%) | 0 (0.0%) | 14 |
| Apache | 14 (100.0%) | 0 (0.0%) | 14 |
| Caddy | 14 (100.0%) | 0 (0.0%) | 14 |
| Node | 8 (57.1%) | 6 (42.9%) | 14 |
| Envoy | 12 (85.7%) | 2 (14.3%) | 14 |
| H2O | 2 (14.3%) | 12 (85.7%) | 14 |
| Cloudflare | 9 (64.3%) | 5 (35.7%) | 14 |
| Mitmproxy | 0 (0.0%) | 14 (100.0%) | 14 |

### RST_STREAM Frame

| Proxy | Conformant | Non-Conformant | Total Tests |
|-------|------------|----------------|-------------|
| Nghttpx | 8 (57.1%) | 6 (42.9%) | 14 |
| HAproxy | 10 (71.4%) | 4 (28.6%) | 14 |
| Apache | 9 (64.3%) | 5 (35.7%) | 14 |
| Caddy | 10 (71.4%) | 4 (28.6%) | 14 |
| Node | 8 (57.1%) | 6 (42.9%) | 14 |
| Envoy | 5 (35.7%) | 9 (64.3%) | 14 |
| H2O | 7 (50.0%) | 7 (50.0%) | 14 |
| Cloudflare | 6 (42.9%) | 8 (57.1%) | 14 |
| Mitmproxy | 4 (28.6%) | 10 (71.4%) | 14 |

### SETTINGS Frame

| Proxy | Conformant | Non-Conformant | Total Tests |
|-------|------------|----------------|-------------|
| Nghttpx | 18 (100.0%) | 0 (0.0%) | 18 |
| HAproxy | 16 (88.9%) | 2 (11.1%) | 18 |
| Apache | 16 (88.9%) | 2 (11.1%) | 18 |
| Caddy | 16 (88.9%) | 2 (11.1%) | 18 |
| Node | 18 (100.0%) | 0 (0.0%) | 18 |
| Envoy | 10 (55.6%) | 8 (44.4%) | 18 |
| H2O | 13 (72.2%) | 5 (27.8%) | 18 |
| Cloudflare | 8 (44.4%) | 10 (55.6%) | 18 |
| Mitmproxy | 0 (0.0%) | 18 (100.0%) | 18 |

### TRAILERS Frame

| Proxy | Conformant | Non-Conformant | Total Tests |
|-------|------------|----------------|-------------|
| Nghttpx | 0 (0.0%) | 4 (100.0%) | 4 |
| HAproxy | 0 (0.0%) | 4 (100.0%) | 4 |
| Apache | 2 (50.0%) | 2 (50.0%) | 4 |
| Caddy | 0 (0.0%) | 4 (100.0%) | 4 |
| Node | 0 (0.0%) | 4 (100.0%) | 4 |
| Envoy | 0 (0.0%) | 4 (100.0%) | 4 |
| H2O | 3 (75.0%) | 1 (25.0%) | 4 |
| Cloudflare | 2 (50.0%) | 2 (50.0%) | 4 |
| Mitmproxy | 0 (0.0%) | 4 (100.0%) | 4 |

### UNKNOWN Frame

| Proxy | Conformant | Non-Conformant | Total Tests |
|-------|------------|----------------|-------------|
| Nghttpx | 4 (100.0%) | 0 (0.0%) | 4 |
| HAproxy | 2 (50.0%) | 2 (50.0%) | 4 |
| Apache | 2 (50.0%) | 2 (50.0%) | 4 |
| Caddy | 1 (25.0%) | 3 (75.0%) | 4 |
| Node | 4 (100.0%) | 0 (0.0%) | 4 |
| Envoy | 2 (50.0%) | 2 (50.0%) | 4 |
| H2O | 4 (100.0%) | 0 (0.0%) | 4 |
| Cloudflare | 4 (100.0%) | 0 (0.0%) | 4 |
| Mitmproxy | 4 (100.0%) | 0 (0.0%) | 4 |

### WINDOW_UPDATE Frame

| Proxy | Conformant | Non-Conformant | Total Tests |
|-------|------------|----------------|-------------|
| Nghttpx | 4 (100.0%) | 0 (0.0%) | 4 |
| HAproxy | 4 (100.0%) | 0 (0.0%) | 4 |
| Apache | 4 (100.0%) | 0 (0.0%) | 4 |
| Caddy | 4 (100.0%) | 0 (0.0%) | 4 |
| Node | 3 (75.0%) | 1 (25.0%) | 4 |
| Envoy | 2 (50.0%) | 2 (50.0%) | 4 |
| H2O | 4 (100.0%) | 0 (0.0%) | 4 |
| Cloudflare | 1 (25.0%) | 3 (75.0%) | 4 |
| Mitmproxy | 0 (0.0%) | 4 (100.0%) | 4 |

## Common Failure Patterns

### Most Common Types of Non-Conformance (Normalized)

| Pattern | Percentage of Non-Conformant Tests | Count |
|---------|-----------------------------------|-------|
| MUST NOT violations | 54.9% | 390 |
| MUST violations | 43.1% | 306 |
| Header-related issues | 41.3% | 293 |
| Frame-related issues | 37.6% | 267 |
| Stream-related issues | 26.1% | 185 |
| Pseudo-header issues | 23.9% | 170 |

Total non-conformant tests analyzed: 710
