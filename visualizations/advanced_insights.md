# Advanced HTTP/2 Conformance Insights

## Test Type Analysis

| Proxy | Error Tests Conformance | Ignore Tests Conformance |
|-------|----------------------|----------------------|
| Nghttpx | 66.2% | 72.7% |
| HAproxy | 72.7% | 36.4% |
| Apache | 72.1% | 45.5% |
| Caddy | 63.0% | 27.3% |
| Node | 50.6% | 72.7% |
| Envoy | 54.5% | 54.5% |
| H2O | 31.2% | 90.9% |
| Cloudflare | 0.0% | 0.0% |
| Nginx | 20.8% | 90.9% |

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
| H2O | 4 (44.4%) | 5 (55.6%) | 9 |
| Cloudflare | 0 (0.0%) | 9 (100.0%) | 9 |
| Nginx | 4 (44.4%) | 5 (55.6%) | 9 |

### DATA Frame

| Proxy | Conformant | Non-Conformant | Total Tests |
|-------|------------|----------------|-------------|
| Nghttpx | 21 (70.0%) | 9 (30.0%) | 30 |
| HAproxy | 20 (66.7%) | 10 (33.3%) | 30 |
| Apache | 24 (80.0%) | 6 (20.0%) | 30 |
| Caddy | 19 (63.3%) | 11 (36.7%) | 30 |
| Node | 18 (60.0%) | 12 (40.0%) | 30 |
| Envoy | 18 (60.0%) | 12 (40.0%) | 30 |
| H2O | 10 (33.3%) | 20 (66.7%) | 30 |
| Cloudflare | 0 (0.0%) | 30 (100.0%) | 30 |
| Nginx | 6 (20.0%) | 24 (80.0%) | 30 |

### HEADERS Frame

| Proxy | Conformant | Non-Conformant | Total Tests |
|-------|------------|----------------|-------------|
| Nghttpx | 75 (57.7%) | 55 (42.3%) | 130 |
| HAproxy | 83 (63.8%) | 47 (36.2%) | 130 |
| Apache | 83 (63.8%) | 47 (36.2%) | 130 |
| Caddy | 68 (52.3%) | 62 (47.7%) | 130 |
| Node | 53 (40.8%) | 77 (59.2%) | 130 |
| Envoy | 70 (53.8%) | 60 (46.2%) | 130 |
| H2O | 34 (26.2%) | 96 (73.8%) | 130 |
| Cloudflare | 0 (0.0%) | 130 (100.0%) | 130 |
| Nginx | 24 (18.5%) | 106 (81.5%) | 130 |

### PING Frame

| Proxy | Conformant | Non-Conformant | Total Tests |
|-------|------------|----------------|-------------|
| Nghttpx | 2 (100.0%) | 0 (0.0%) | 2 |
| HAproxy | 2 (100.0%) | 0 (0.0%) | 2 |
| Apache | 2 (100.0%) | 0 (0.0%) | 2 |
| Caddy | 2 (100.0%) | 0 (0.0%) | 2 |
| Node | 2 (100.0%) | 0 (0.0%) | 2 |
| Envoy | 1 (50.0%) | 1 (50.0%) | 2 |
| H2O | 1 (50.0%) | 1 (50.0%) | 2 |
| Cloudflare | 0 (0.0%) | 2 (100.0%) | 2 |
| Nginx | 1 (50.0%) | 1 (50.0%) | 2 |

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
| Cloudflare | 0 (0.0%) | 2 (100.0%) | 2 |
| Nginx | 1 (50.0%) | 1 (50.0%) | 2 |

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
| Cloudflare | 0 (0.0%) | 14 (100.0%) | 14 |
| Nginx | 2 (14.3%) | 12 (85.7%) | 14 |

### RST_STREAM Frame

| Proxy | Conformant | Non-Conformant | Total Tests |
|-------|------------|----------------|-------------|
| Nghttpx | 8 (57.1%) | 6 (42.9%) | 14 |
| HAproxy | 10 (71.4%) | 4 (28.6%) | 14 |
| Apache | 9 (64.3%) | 5 (35.7%) | 14 |
| Caddy | 10 (71.4%) | 4 (28.6%) | 14 |
| Node | 8 (57.1%) | 6 (42.9%) | 14 |
| Envoy | 5 (35.7%) | 9 (64.3%) | 14 |
| H2O | 5 (35.7%) | 9 (64.3%) | 14 |
| Cloudflare | 0 (0.0%) | 14 (100.0%) | 14 |
| Nginx | 3 (21.4%) | 11 (78.6%) | 14 |

### SETTINGS Frame

| Proxy | Conformant | Non-Conformant | Total Tests |
|-------|------------|----------------|-------------|
| Nghttpx | 18 (100.0%) | 0 (0.0%) | 18 |
| HAproxy | 16 (88.9%) | 2 (11.1%) | 18 |
| Apache | 16 (88.9%) | 2 (11.1%) | 18 |
| Caddy | 16 (88.9%) | 2 (11.1%) | 18 |
| Node | 18 (100.0%) | 0 (0.0%) | 18 |
| Envoy | 10 (55.6%) | 8 (44.4%) | 18 |
| H2O | 12 (66.7%) | 6 (33.3%) | 18 |
| Cloudflare | 0 (0.0%) | 18 (100.0%) | 18 |
| Nginx | 12 (66.7%) | 6 (33.3%) | 18 |

### TRAILERS Frame

| Proxy | Conformant | Non-Conformant | Total Tests |
|-------|------------|----------------|-------------|
| Nghttpx | 0 (0.0%) | 4 (100.0%) | 4 |
| HAproxy | 0 (0.0%) | 4 (100.0%) | 4 |
| Apache | 2 (50.0%) | 2 (50.0%) | 4 |
| Caddy | 0 (0.0%) | 4 (100.0%) | 4 |
| Node | 0 (0.0%) | 4 (100.0%) | 4 |
| Envoy | 0 (0.0%) | 4 (100.0%) | 4 |
| H2O | 2 (50.0%) | 2 (50.0%) | 4 |
| Cloudflare | 0 (0.0%) | 4 (100.0%) | 4 |
| Nginx | 2 (50.0%) | 2 (50.0%) | 4 |

### UNKNOWN Frame

| Proxy | Conformant | Non-Conformant | Total Tests |
|-------|------------|----------------|-------------|
| Nghttpx | 2 (50.0%) | 2 (50.0%) | 4 |
| HAproxy | 2 (50.0%) | 2 (50.0%) | 4 |
| Apache | 2 (50.0%) | 2 (50.0%) | 4 |
| Caddy | 1 (25.0%) | 3 (75.0%) | 4 |
| Node | 2 (50.0%) | 2 (50.0%) | 4 |
| Envoy | 2 (50.0%) | 2 (50.0%) | 4 |
| H2O | 4 (100.0%) | 0 (0.0%) | 4 |
| Cloudflare | 0 (0.0%) | 4 (100.0%) | 4 |
| Nginx | 3 (75.0%) | 1 (25.0%) | 4 |

### WINDOW_UPDATE Frame

| Proxy | Conformant | Non-Conformant | Total Tests |
|-------|------------|----------------|-------------|
| Nghttpx | 4 (100.0%) | 0 (0.0%) | 4 |
| HAproxy | 4 (100.0%) | 0 (0.0%) | 4 |
| Apache | 4 (100.0%) | 0 (0.0%) | 4 |
| Caddy | 4 (100.0%) | 0 (0.0%) | 4 |
| Node | 3 (75.0%) | 1 (25.0%) | 4 |
| Envoy | 2 (50.0%) | 2 (50.0%) | 4 |
| H2O | 2 (50.0%) | 2 (50.0%) | 4 |
| Cloudflare | 0 (0.0%) | 4 (100.0%) | 4 |
| Nginx | 2 (50.0%) | 2 (50.0%) | 4 |

## Common Failure Patterns

### Most Common Types of Non-Conformance (Normalized)

| Pattern | Percentage of Non-Conformant Tests | Count |
|---------|-----------------------------------|-------|
| MUST NOT violations | 54.5% | 418 |
| MUST violations | 43.9% | 337 |
| Header-related issues | 40.9% | 314 |
| Frame-related issues | 40.2% | 308 |
| Stream-related issues | 27.8% | 213 |
| Pseudo-header issues | 22.9% | 176 |

Total non-conformant tests analyzed: 767