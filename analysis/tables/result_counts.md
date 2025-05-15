# HTTP/2 Conformance Test Results

## Overview
This document presents the results of HTTP/2 conformance testing across various proxy servers. The tests evaluate how each proxy handles different HTTP/2 protocol scenarios.

## Test Categories
- **Error Handling Tests**: How proxies handle protocol errors (500 Error, GOAWAY, RESET)
- **Connection Tests**: Tests for connection handling (Dropped connections)
- **Response Tests**: Tests for response handling (Received, Modified, Unmodified)

## Result Types Explained
| Result Type | Description |
|:------------|:------------|
| Dropped     | Connection timed out or was dropped |
| 500 Error   | Server returned HTTP 500 error |
| GOAWAY      | Server sent HTTP/2 GOAWAY frame |
| RESET       | Server sent HTTP/2 RST_STREAM frame |
| Received    | Response received successfully |
| Modified    | Response was modified by proxy |
| Unmodified  | Response passed through unmodified |


## Full Test Suite

### Error Handling & Connection Statistics
| Proxy | Connection Issues | Error Responses | Protocol Errors | Response Stats |
|:------|:------------------|:----------------|:----------------|:--------------|
| Apache-2.4.63 | Dropped: 48 | 500 Error: 40 | GOAWAY: 67, RESET: 0 | Modified: 0, Unmodified: 1 |
| Caddy-2.9.1 | Dropped: 50 | 500 Error: 65 | GOAWAY: 29, RESET: 0 | Modified: 6, Unmodified: 6 |
| Cloudflare | Dropped: 73 | 500 Error: 63 | GOAWAY: 6, RESET: 5 | Modified: 7, Unmodified: 2 |
| Envoy-1.34.1 | Dropped: 52 | 500 Error: 31 | GOAWAY: 63, RESET: 4 | Modified: 0, Unmodified: 4 |
| H2O-26b116e95 | Dropped: 89 | 500 Error: 7 | GOAWAY: 59, RESET: 0 | Modified: 1, Unmodified: 0 |
| HAproxy-3.2.0 | Dropped: 40 | 500 Error: 24 | GOAWAY: 81, RESET: 1 | Modified: 5, Unmodified: 5 |
| Mitmproxy-11.1.0 | Dropped: 21 | 500 Error: 0 | GOAWAY: 0, RESET: 4 | Modified: 0, Unmodified: 131 |
| Nghttpx-1.62.1 | Dropped: 55 | 500 Error: 0 | GOAWAY: 61, RESET: 34 | Modified: 1, Unmodified: 5 |
| Node-20.16.0 | Dropped: 70 | 500 Error: 14 | GOAWAY: 61, RESET: 0 | Modified: 8, Unmodified: 3 |
| Traefik-3.3.5 | Dropped: 127 | 500 Error: 0 | GOAWAY: 29, RESET: 0 | Modified: 0, Unmodified: 0 |

### Detailed Test Results
| Proxy | Test Details |
|:------|:-------------|
| Apache-2.4.63 | **Unmodified Tests**: 6 |
| Caddy-2.9.1 | **Modified Tests**: 142-147<br>**Unmodified Tests**: 6, 81, 92, 136-137, 156 |
| Cloudflare | **Modified Tests**: 3, 125, 136-137, 146, 148, 153<br>**Unmodified Tests**: 81, 92 |
| Envoy-1.34.1 | **Unmodified Tests**: 6, 81, 136-137 |
| H2O-26b116e95 | **Modified Tests**: 78 |
| HAproxy-3.2.0 | **Modified Tests**: 51-52, 68, 136-137<br>**Unmodified Tests**: 6, 69, 78, 81, 147 |
| Mitmproxy-11.1.0 | **Unmodified Tests**: 2-4, 6-8, 10-15, 17-19, 25-32, 36-79, 81-85, 87, 89-92, 94-96, 103-116, 120-156 |
| Nghttpx-1.62.1 | **Modified Tests**: 68<br>**Unmodified Tests**: 6, 69, 78, 81, 92 |
| Node-20.16.0 | **Modified Tests**: 129-130, 132-137<br>**Unmodified Tests**: 6, 81, 92 |
| Traefik-3.3.5 | No test details available |


## Client-side Only Tests

### Error Handling & Connection Statistics
| Proxy | Connection Issues | Error Responses | Protocol Errors | Response Stats |
|:------|:------------------|:----------------|:----------------|:--------------|
| Azure-AG | Dropped: 76 | 500 Error: 0 | GOAWAY: 0, RESET: 0 | Received: 2 |
| Fastly | Dropped: 26 | 500 Error: 0 | GOAWAY: 43, RESET: 9 | Received: 0 |
| Lighttpd-1.4.76 | Dropped: 44 | 500 Error: 0 | GOAWAY: 30, RESET: 1 | Received: 3 |
| Nginx-1.28.0 | Dropped: 49 | 500 Error: 0 | GOAWAY: 27, RESET: 0 | Received: 2 |
| Varnish-7.7.0 | Dropped: 36 | 500 Error: 0 | GOAWAY: 31, RESET: 0 | Received: 11 |

### Detailed Test Results
| Proxy | Test Details |
|:------|:-------------|
| Azure-AG | **Received Tests**: 3-4 |
| Fastly | No test details available |
| Lighttpd-1.4.76 | **Received Tests**: 3, 8, 15 |
| Nginx-1.28.0 | **Received Tests**: 3-4 |
| Varnish-7.7.0 | **Received Tests**: 3, 6, 40, 57-62, 65, 69 |

