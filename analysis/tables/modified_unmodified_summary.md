# Modified and Unmodified Test Results Summary

This file lists test cases where at least one proxy returned a 'modified' or 'unmodified' result.

## Test 3: the connection preface starts with the string: PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n

**Modified by:** Cloudflare

---

## Test 81: If a DATA frame is received whose Stream Identifier field is 0x00, the recipient MUST respond with a connection error (Section 5.4.1) of type PROTOCOL_ERROR.

**Unmodified by:** Caddy-2.9.1, Cloudflare, Envoy-1.32.2, HAproxy-2.9.10, Nghttpx-1.62.1, Node-20.16.0

---

## Test 78: RST_STREAM frames MUST be associated with a stream.

**Modified by:** H2O-26b116e95
**Unmodified by:** Nghttpx-1.62.1

---

## Test 51: An endpoint MUST NOT generate an HTTP/2 message containing connection header field (RFC9113 Section 8.2.2)

**Unmodified by:** Envoy-1.32.2, HAproxy-2.9.10

---

## Test 52: An endpoint MUST NOT generate an HTTP/2 message containing proxy-connection header field (RFC9113 Section 8.2.2)

**Unmodified by:** Envoy-1.32.2, HAproxy-2.9.10

---

## Test 68: The ":path" pseudo-header field MUST NOT be empty for "http" or "https" URIs; "http" or "https" URIs that do not contain a path component MUST include a value of '/'.

**Modified by:** HAproxy-2.9.10, Nghttpx-1.62.1

---

## Test 69: All HTTP/2 requests MUST include exactly one valid value for the ":method", ":scheme", and ":path" pseudo-header fields, unless they are CONNECT requests (Section 8.5). An HTTP request that omits mandatory pseudo-header fields is malformed (Section 8.1.1). (Tested with :method missing)

**Unmodified by:** HAproxy-2.9.10, Nghttpx-1.62.1

---

## Test 6: An endpoint MUST NOT send any type of frame other than HEADERS, RST_STREAM, or PRIORITY in the reserved (local) state.

**Unmodified by:** Nghttpx-1.62.1

---

## Test 144: An endpoint MUST NOT send frames other than PRIORITY on a closed stream.

**Modified by:** Caddy-2.9.1

---

## Test 148: DATA frames MUST be associated with a stream. (server side)

**Modified by:** Cloudflare

---

## Test 92: PUSH_PROMISE MUST NOT be sent if the SETTINGS_ENABLE_PUSH setting of the peer endpoint is set to 0.

**Unmodified by:** Caddy-2.9.1, Cloudflare, Envoy-1.32.2, HAproxy-2.9.10, Nghttpx-1.62.1, Node-20.16.0

---

## Test 153: A HEADERS frame without the END_HEADERS flag set MUST be followed by a CONTINUATION frame for the same stream.

**Unmodified by:** Cloudflare

---

## Test 145: RST_STREAM frames MUST NOT be sent for a stream in the 'idle' state. (server side)

**Modified by:** Caddy-2.9.1

---

## Test 146: RST_STREAM frames MUST be associated with a stream. (server side)

**Modified by:** Caddy-2.9.1, Cloudflare

---

## Test 156: The sender MUST NOT send a flow-controlled frame with a length that exceeds the space available in either of the flow-control windows advertised by the receiver.

**Unmodified by:** Caddy-2.9.1

---

## Test 125: A CONTINUATION frame MUST be preceded by a HEADERS, PUSH_PROMISE or CONTINUATION frame without the END_HEADERS flag set. (Using HEADERS frame with END_HEADERS flag set)

**Modified by:** Cloudflare, HAproxy-2.9.10

---

## Test 129: Field names MUST NOT contain ASCII SP (0x20)

**Modified by:** Node-20.16.0

---

## Test 130: Field names MUST NOT contain DEL character (0x7F)

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

**Modified by:** Node-20.16.0

---

## Test 136: A field value MUST NOT end with an ASCII whitespace character (ASCII SP or HTAB, 0x20 or 0x09).

**Modified by:** Cloudflare, Node-20.16.0
**Unmodified by:** Caddy-2.9.1, Envoy-1.32.2, HAproxy-2.9.10

---

## Test 137: An endpoint MUST NOT generate an HTTP/2 message containing connection header field (RFC9113 Section 8.2.2)

**Modified by:** Cloudflare, Node-20.16.0
**Unmodified by:** Caddy-2.9.1, Envoy-1.32.2, HAproxy-2.9.10

---

## Test 147: Implementations MUST discard frames that have unknown or unsupported types. (server side)

**Modified by:** Caddy-2.9.1
**Unmodified by:** HAproxy-2.9.10

---

## Test 142: The TE header field MAY be present in an HTTP/2 request; when it is, it MUST NOT contain any value other than 'trailers'.

**Modified by:** Caddy-2.9.1

---

## Test 143: Pseudo-header fields are not HTTP header fields. Endpoints MUST NOT generate pseudo-header fields other than those defined in this document.

**Modified by:** Caddy-2.9.1

---

