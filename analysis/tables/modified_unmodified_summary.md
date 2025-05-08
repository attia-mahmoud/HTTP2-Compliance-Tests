# Modified and Unmodified Test Results Summary\n\nThis file lists test cases where at least one proxy returned a 'modified' or 'unmodified' result.\n\n## Test 4: Client preface must include a SETTINGS frame

**Modified by:** Cloudflare

---

## Test 110: A reserved 1-bit field. The semantics of this bit are undefined, and the bit MUST remain unset (0x00) when sending and MUST be ignored when receiving. (server side)

**Unmodified by:** Caddy-2.9.1, Cloudflare, Envoy-1.32.2, HAproxy-2.9.10, Nghttpx-1.62.1, Node-20.16.0

---

## Test 75: With the CONNECT method, The ":authority" pseudo-header field contains the host and port to connect to

**Modified by:** H2O-26b116e95
**Unmodified by:** Nghttpx-1.62.1

---

## Test 49: A field value MUST NOT start with an ASCII whitespace character (ASCII SP or HTAB, 0x20 or 0x09).

**Unmodified by:** Envoy-1.32.2, HAproxy-2.9.10

---

## Test 50: A field value MUST NOT end with an ASCII whitespace character (ASCII SP or HTAB, 0x20 or 0x09).

**Unmodified by:** Envoy-1.32.2, HAproxy-2.9.10

---

## Test 66: Clients MUST NOT generate a request with a Host header field that differs from the ":authority" pseudo-header field.

**Modified by:** HAproxy-2.9.10, Nghttpx-1.62.1

---

## Test 67: ':authority' MUST NOT include the deprecated userinfo subcomponent for "http" or "https" schemed URIs.

**Unmodified by:** HAproxy-2.9.10, Nghttpx-1.62.1

---

## Test 10: A reserved 1-bit field. The semantics of this bit are undefined, and the bit MUST remain unset (0x00) when sending and MUST be ignored when receiving.

**Unmodified by:** Nghttpx-1.62.1

---

## Test 139: An endpoint MUST NOT generate an HTTP/2 message containing keep-alive header field (RFC9113 Section 8.2.2)

**Modified by:** Caddy-2.9.1

---

## Test 58: Pseudo-header fields defined for requests MUST NOT appear in responses.

**Modified by:** Cloudflare

---

## Test 151: If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the half-closed (remote) state.)

**Unmodified by:** Caddy-2.9.1, Cloudflare, Envoy-1.32.2, HAproxy-2.9.10, Nghttpx-1.62.1, Node-20.16.0

---

## Test 71: For HTTP/2 responses, a single ":status" pseudo-header field is defined that carries the HTTP status code field. This pseudo-header field MUST be included in all responses, including interim responses; otherwise, the response is malformed.

**Unmodified by:** Cloudflare

---

## Test 140: An endpoint MUST NOT generate an HTTP/2 message containing transfer-encoding header field (RFC9113 Section 8.2.2)

**Modified by:** Caddy-2.9.1

---

## Test 141: An endpoint MUST NOT generate an HTTP/2 message containing upgrade header field (RFC9113 Section 8.2.2)

**Modified by:** Caddy-2.9.1, Cloudflare

---

## Test 166: HTTP/2 does not support the 101 (Switching Protocols) informational status code (Section 15.2.2 of [HTTP]).

**Unmodified by:** Caddy-2.9.1

---

## Test 126: Trailers MUST NOT include pseudo-header fields (Section 8.3). (server side)

**Modified by:** Cloudflare, HAproxy-2.9.10

---

## Test 128: Field names MUST NOT contain control characters (0x00-0x1F)

**Modified by:** Node-20.16.0

---

## Test 129: Field names MUST NOT contain ASCII SP (0x20)

**Modified by:** Node-20.16.0

---

## Test 131: Field names MUST NOT contain high byte characters (0x80-0xFF)

**Modified by:** Node-20.16.0

---

## Test 132: With the exception of pseudo-header fields (Section 8.3), which have a name that starts with a single colon, field names MUST NOT include a colon (ASCII COLON, 0x3a).

**Modified by:** Node-20.16.0

---

## Test 133: A field value MUST NOT contain line feed (ASCII LF, 0x0a). (Tested at the start of the value)

**Modified by:** Node-20.16.0

---

## Test 134: A field value MUST NOT contain carriage return (ASCII CR, 0x0d). (Tested at the start of the value)

**Modified by:** Node-20.16.0

---

## Test 135: A field value MUST NOT start with an ASCII whitespace character (ASCII SP or HTAB, 0x20 or 0x09).

**Modified by:** Cloudflare, Node-20.16.0
**Unmodified by:** Caddy-2.9.1, Envoy-1.32.2, HAproxy-2.9.10

---

## Test 136: A field value MUST NOT end with an ASCII whitespace character (ASCII SP or HTAB, 0x20 or 0x09).

**Modified by:** Cloudflare, Node-20.16.0
**Unmodified by:** Caddy-2.9.1, Envoy-1.32.2, HAproxy-2.9.10

---

## Test 142: The TE header field MAY be present in an HTTP/2 request; when it is, it MUST NOT contain any value other than 'trailers'.

**Modified by:** Caddy-2.9.1
**Unmodified by:** HAproxy-2.9.10

---

## Test 137: An endpoint MUST NOT generate an HTTP/2 message containing connection header field (RFC9113 Section 8.2.2)

**Modified by:** Caddy-2.9.1

---

## Test 138: An endpoint MUST NOT generate an HTTP/2 message containing proxy-connection header field (RFC9113 Section 8.2.2)

**Modified by:** Caddy-2.9.1

---

