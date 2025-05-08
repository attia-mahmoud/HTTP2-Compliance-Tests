# Modified and Unmodified Test Results Summary

This file lists test cases where at least one proxy returned a 'modified' or 'unmodified' result.

## Test 2: Client must send connection preface after TLS establishment

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 3: the connection preface starts with the string: PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n

**Modified by:** Cloudflare, Mitmproxy-11.1.0

---

## Test 4: Client preface must include a SETTINGS frame

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 9: The frame type determines the format and semantics of the frame. Implementations MUST ignore and discard frames of unknown types.

**Unmodified by:** Caddy-2.9.1, Cloudflare, Envoy-1.21.2, Envoy-1.32.2, HAproxy-2.6.0, HAproxy-2.9.10, Mitmproxy-11.1.0, Nghttpx-1.47.0, Nghttpx-1.62.1, Node-14.19.3, Node-20.16.0

---

## Test 10: A reserved 1-bit field. The semantics of this bit are undefined, and the bit MUST remain unset (0x00) when sending and MUST be ignored when receiving.

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 108: Values greater than 16,384 MUST NOT be sent unless receiver has set larger SETTINGS_MAX_FRAME_SIZE. (server side)

**Modified by:** Node-14.19.3, Node-20.16.0
**Unmodified by:** Mitmproxy-11.1.0

---

## Test 109: The frame type determines the format and semantics of the frame. Implementations MUST ignore and discard frames of unknown types. (server side)

**Unmodified by:** Mitmproxy-11.1.0, Node-14.19.3

---

## Test 110: A reserved 1-bit field. The semantics of this bit are undefined, and the bit MUST remain unset (0x00) when sending and MUST be ignored when receiving. (server side)

**Modified by:** Node-14.19.3, Node-20.16.0
**Unmodified by:** Mitmproxy-11.1.0

---

## Test 6: An endpoint MUST NOT send any type of frame other than HEADERS, RST_STREAM, or PRIORITY in the reserved (local) state.

**Unmodified by:** HAproxy-2.6.0, Mitmproxy-11.1.0, Nghttpx-1.47.0, Nghttpx-1.62.1, Node-14.19.3

---

## Test 7: If an endpoint receives additional frames, other than WINDOW_UPDATE, PRIORITY, or RST_STREAM, for a stream that is in the half-closed (remote) state, it MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED.

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 106: Receiving any frame other than HEADERS or PRIORITY on a stream in this (idle) state MUST be treated as a connection error (Section 5.4.1) of type PROTOCOL_ERROR. (server side)

**Unmodified by:** Mitmproxy-11.1.0, Node-14.19.3

---

## Test 107: If an endpoint receives additional frames, other than WINDOW_UPDATE, PRIORITY, or RST_STREAM, for a stream that is in the half-closed (remote) state, it MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (server side)

**Modified by:** Node-14.19.3, Node-20.16.0
**Unmodified by:** Mitmproxy-11.1.0

---

## Test 144: An endpoint MUST NOT send frames other than PRIORITY on a closed stream.

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 11: Streams initiated by a client MUST use odd-numbered stream identifiers.

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 12: Streams initiated by a server MUST use even-numbered stream identifiers.

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 13: The identifier of a newly established stream MUST be numerically greater than all streams that the initiating endpoint has opened or reserved.

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 80: DATA frames MUST be associated with a stream.

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 81: If a DATA frame is received whose Stream Identifier field is 0x00, the recipient MUST respond with a connection error (Section 5.4.1) of type PROTOCOL_ERROR.

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 82: If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the idle state.)

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 83: If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the half-closed (remote) state.)

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 84: If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the closed state.)

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 148: DATA frames MUST be associated with a stream. (server side)

**Unmodified by:** Cloudflare, Mitmproxy-11.1.0

---

## Test 149: If a DATA frame is received whose Stream Identifier field is 0x00, the recipient MUST respond with a connection error (Section 5.4.1) of type PROTOCOL_ERROR. (server side)

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 150: If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the idle state.) (server side)

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 151: If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the half-closed (remote) state.)

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 152: If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the closed state.)

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 85: A HEADERS frame without the END_HEADERS flag set MUST be followed by a CONTINUATION frame for the same stream.

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 86: If a HEADERS frame is received whose Stream Identifier field is 0x00, the recipient MUST respond with a connection error (Section 5.4.1) of type PROTOCOL_ERROR.

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 153: A HEADERS frame without the END_HEADERS flag set MUST be followed by a CONTINUATION frame for the same stream.

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 154: If a HEADERS frame is received whose Stream Identifier field is 0x00, the recipient MUST respond with a connection error (Section 5.4.1) of type PROTOCOL_ERROR.

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 35: An endpoint MUST treat a change to SETTINGS_INITIAL_WINDOW_SIZE that causes any flow-control window to exceed the maximum size as a connection error (Section 5.4.1) of type FLOW_CONTROL_ERROR.

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 15: If a PRIORITY frame is received with a stream identifier of 0x00, the recipient MUST respond with a connection error of type PROTOCOL_ERROR

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 111: If a PRIORITY frame is received with a stream identifier of 0x00, the recipient MUST respond with a connection error of type PROTOCOL_ERROR. (server side)

**Modified by:** Node-14.19.3, Node-20.16.0
**Unmodified by:** Mitmproxy-11.1.0

---

## Test 16: After receiving a RST_STREAM on a stream, the receiver MUST NOT send additional frames for that stream, except for PRIORITY

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 19: A RST_STREAM frame with a length other than 4 octets MUST be treated as a connection error (Section 5.4.1) of type FRAME_SIZE_ERROR.

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 77: RST_STREAM frames MUST NOT be sent for a stream in the 'idle' state.

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 78: RST_STREAM frames MUST be associated with a stream.

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 112: If a RST_STREAM frame is received with a stream identifier of 0x00, the recipient MUST treat this as a connection error (Section 5.4.1) of type PROTOCOL_ERROR. (server side)

**Modified by:** Node-14.19.3, Node-20.16.0
**Unmodified by:** Mitmproxy-11.1.0

---

## Test 114: A RST_STREAM frame with a length other than 4 octets MUST be treated as a connection error (Section 5.4.1) of type FRAME_SIZE_ERROR. (server side)

**Modified by:** Cloudflare, Node-20.16.0
**Unmodified by:** Caddy-2.9.1, Envoy-1.21.2, Envoy-1.32.2, HAproxy-2.6.0, HAproxy-2.9.10, Mitmproxy-11.1.0, Nghttpx-1.47.0, Node-14.19.3

---

## Test 145: RST_STREAM frames MUST NOT be sent for a stream in the 'idle' state. (server side)

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 146: RST_STREAM frames MUST be associated with a stream. (server side)

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 18: When set, the ACK flag indicates that this frame acknowledges receipt and application of the peer's SETTINGS frame. When this bit is set, the frame payload of the SETTINGS frame MUST be empty.

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 20: The stream identifier for a SETTINGS frame MUST be zero (0x00).

**Unmodified by:** Mitmproxy-11.1.0, Node-14.19.3

---

## Test 113: When set, the ACK flag indicates that this frame acknowledges receipt and application of the peer's SETTINGS frame. When this bit is set, the frame payload of the SETTINGS frame MUST be empty. (server side)

**Modified by:** Node-14.19.3, Node-20.16.0
**Unmodified by:** Mitmproxy-11.1.0

---

## Test 115: The stream identifier for a SETTINGS frame MUST be zero (0x00).

**Modified by:** Cloudflare, Node-20.16.0
**Unmodified by:** Caddy-2.9.1, Envoy-1.21.2, Envoy-1.32.2, HAproxy-2.6.0, HAproxy-2.9.10, Mitmproxy-11.1.0, Nghttpx-1.47.0, Node-14.19.3

---

## Test 116: A SETTINGS frame with a length other than a multiple of 6 octets MUST be treated as a connection error (Section 5.4.1) of type FRAME_SIZE_ERROR.

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 22: The initial value of SETTINGS_ENABLE_PUSH is 1. Any value other than 0 or 1 MUST be treated as a connection error (Section 5.4.1) of type PROTOCOL_ERROR.

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 23: A server MUST NOT explicitly set this value (SETTINGS_ENABLE_PUSH) to 1. A server MAY choose to omit this setting (SETTINGS_ENABLE_PUSH) when it sends a SETTINGS frame, but if a server does include a value, it MUST be 0.

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 24: A server MUST NOT send a PUSH_PROMISE frame if it receives the SETTINGS_ENABLE_PUSH (0x02) parameter set to a value of 0.

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 25: For SETTINGS_INITIAL_WINDOW_SIZE, values above the maximum flow-control window size of 2^31-1 (2147483647) MUST be treated as a connection error (Section 5.4.1) of type FLOW_CONTROL_ERROR.

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 27: An endpoint that receives a SETTINGS frame with any unknown or unsupported identifier MUST ignore that setting.

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 117: For SETTINGS_INITIAL_WINDOW_SIZE, values above the maximum flow-control window size of 2^31-1 (2147483647) MUST be treated as a connection error (Section 5.4.1) of type FLOW_CONTROL_ERROR.

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 118: The value advertised by an endpoint MUST be between initial value (2^14 = 16,384) and maximum allowed frame size (2^24-1 = 16,777,215 octets), inclusive.

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 119: An endpoint that receives a SETTINGS frame with any unknown or unsupported identifier MUST ignore that setting.

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 88: Unsupported settings MUST be ignored.

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 155: Unsupported settings MUST be ignored.

**Modified by:** H2O-26b116e95
**Unmodified by:** HAproxy-2.6.0, Mitmproxy-11.1.0, Nghttpx-1.47.0, Nghttpx-1.62.1

---

## Test 28: If the Stream Identifier field of a PUSH_PROMISE frame specifies the value 0x00, a recipient MUST respond with a connection error (Section 5.4.1) of type PROTOCOL_ERROR.

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 29: The promised stream identifier MUST be a valid choice for the next stream sent by the sender (see 'new stream identifier' in Section 5.1.1). (Using Odd-numbered Stream ID (Invalid for Server))

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 89: The promised stream identifier MUST be a valid choice for the next stream sent by the sender (see 'new stream identifier' in Section 5.1.1). (Using Already Used Stream ID)

**Modified by:** Cloudflare, HAproxy-2.6.0, HAproxy-2.9.10, Mitmproxy-11.1.0, Node-14.19.3

---

## Test 90: The promised stream identifier MUST be a valid choice for the next stream sent by the sender (see 'new stream identifier' in Section 5.1.1). (Using Lower Stream ID)

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 91: A PUSH_PROMISE frame without the END_HEADERS flag set MUST be followed by a CONTINUATION frame for the same stream.

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 30: If a PING frame is received with a Stream Identifier field value other than 0x00, the recipient MUST respond with a connection error (Section 5.4.1) of type PROTOCOL_ERROR.

**Unmodified by:** Caddy-2.9.1, Cloudflare, Envoy-1.32.2, HAproxy-2.9.10, Mitmproxy-11.1.0, Nghttpx-1.62.1, Node-14.19.3, Node-20.16.0

---

## Test 120: If a PING frame is received with a Stream Identifier field value other than 0x00, the recipient MUST respond with a connection error (Section 5.4.1) of type PROTOCOL_ERROR.

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 33: A receiver MUST treat the receipt of a WINDOW_UPDATE frame with a flow-control window increment of 0 as a stream error (Section 5.4.2) of type PROTOCOL_ERROR.

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 121: A receiver MUST treat the receipt of a WINDOW_UPDATE frame with a flow-control window increment of 0 as a stream error (Section 5.4.2) of type PROTOCOL_ERROR.

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 34: A sender MUST NOT allow a flow-control window to exceed 2^31-1 octets. If a sender receives a WINDOW_UPDATE that causes a flow-control window to exceed this maximum, it MUST terminate either the stream or the connection, as appropriate.

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 93: The sender MUST NOT send a flow-controlled frame with a length that exceeds the space available in either of the flow-control windows advertised by the receiver.

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 122: A sender MUST NOT allow a flow-control window to exceed 2^31-1 octets. If a sender receives a WINDOW_UPDATE that causes a flow-control window to exceed this maximum, it MUST terminate either the stream or the connection, as appropriate.

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 156: The sender MUST NOT send a flow-controlled frame with a length that exceeds the space available in either of the flow-control windows advertised by the receiver.

**Unmodified by:** Caddy-2.9.1, Mitmproxy-11.1.0

---

## Test 36: If a CONTINUATION frame is received with a Stream Identifier field of 0x00, the recipient MUST respond with a connection error (Section 5.4.1) of type PROTOCOL_ERROR.

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 37: A CONTINUATION frame MUST be preceded by a HEADERS, PUSH_PROMISE or CONTINUATION frame without the END_HEADERS flag set. (Using HEADERS frame with END_HEADERS flag set)

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 79: Implementations MUST discard frames that have unknown or unsupported types.

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 94: CONTINUATION frames MUST be associated with a stream.

**Unmodified by:** Mitmproxy-11.1.0, Node-14.19.3

---

## Test 95: If the END_HEADERS flag is not set, this frame MUST be followed by another CONTINUATION frame. A receiver MUST treat the receipt of any other type of frame or a frame on a different stream as a connection error (Section 5.4.1) of type PROTOCOL_ERROR.

**Unmodified by:** Mitmproxy-11.1.0, Node-14.19.3

---

## Test 124: If a CONTINUATION frame is received with a Stream Identifier field of 0x00, the recipient MUST respond with a connection error (Section 5.4.1) of type PROTOCOL_ERROR.

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 125: A CONTINUATION frame MUST be preceded by a HEADERS, PUSH_PROMISE or CONTINUATION frame without the END_HEADERS flag set. (Using HEADERS frame with END_HEADERS flag set)

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 96: Other frames (from any stream) MUST NOT occur between the HEADERS frame and any CONTINUATION frames that might follow.

**Unmodified by:** Mitmproxy-11.1.0, Node-14.19.3

---

## Test 87: A SETTINGS frame MUST be sent by both endpoints at the start of a connection and MAY be sent at any other time by either endpoint over the lifetime of the connection. (Tested from the client side.)

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 97: An endpoint that receives a HEADERS frame without the END_STREAM flag set after receiving the HEADERS frame that opens a request or after receiving a final (non-informational) status code MUST treat the corresponding request or response as malformed (Section 8.1.1).

**Unmodified by:** Mitmproxy-11.1.0, Node-14.19.3

---

## Test 126: Trailers MUST NOT include pseudo-header fields (Section 8.3). (server side)

**Modified by:** Caddy-2.9.1
**Unmodified by:** Mitmproxy-11.1.0

---

## Test 92: PUSH_PROMISE MUST NOT be sent if the SETTINGS_ENABLE_PUSH setting of the peer endpoint is set to 0.

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 127: Field names MUST be converted to lowercase when constructing an HTTP/2 message.

**Modified by:** Caddy-2.9.1
**Unmodified by:** Mitmproxy-11.1.0

---

## Test 48: A field value MUST NOT contain carriage return (ASCII CR, 0x0d). (Tested at the start of the value)

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 49: A field value MUST NOT start with an ASCII whitespace character (ASCII SP or HTAB, 0x20 or 0x09).

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 102: Pseudo-header fields MUST NOT appear in a trailer section.

**Unmodified by:** Envoy-1.32.2, HAproxy-2.6.0, HAproxy-2.9.10, Mitmproxy-11.1.0, Nghttpx-1.47.0, Node-14.19.3

---

## Test 98: A field value MUST NOT contain line feed (ASCII LF, 0x0a). (Tested at the middle of the value)

**Unmodified by:** Mitmproxy-11.1.0, Node-14.19.3

---

## Test 99: A field value MUST NOT contain line feed (ASCII LF, 0x0a). (Tested at the end of the value)

**Unmodified by:** Mitmproxy-11.1.0, Node-14.19.3

---

## Test 104: Promised requests MUST be safe (see Section 9.2.1 of [HTTP]) and cacheable (see Section 9.2.3 of [HTTP]).

**Unmodified by:** Mitmproxy-11.1.0, Node-14.19.3

---

## Test 100: A field value MUST NOT contain carriage return (ASCII CR, 0x0d). (Tested at the middle of the value)

**Unmodified by:** Mitmproxy-11.1.0, Node-14.19.3

---

## Test 105: PUSH_PROMISE frames MUST NOT be sent by the client.

**Unmodified by:** Mitmproxy-11.1.0, Node-14.19.3

---

## Test 101: A field value MUST NOT contain carriage return (ASCII CR, 0x0d). (Tested at the end of the value)

**Unmodified by:** Envoy-1.32.2, HAproxy-2.6.0, HAproxy-2.9.10, Mitmproxy-11.1.0, Nghttpx-1.47.0, Node-14.19.3

---

## Test 128: Field names MUST NOT contain control characters (0x00-0x1F)

**Modified by:** Caddy-2.9.1
**Unmodified by:** Mitmproxy-11.1.0

---

## Test 129: Field names MUST NOT contain ASCII SP (0x20)

**Modified by:** Caddy-2.9.1
**Unmodified by:** Mitmproxy-11.1.0

---

## Test 130: Field names MUST NOT contain DEL character (0x7F)

**Modified by:** Caddy-2.9.1, Cloudflare
**Unmodified by:** Mitmproxy-11.1.0

---

## Test 131: Field names MUST NOT contain high byte characters (0x80-0xFF)

**Modified by:** Caddy-2.9.1
**Unmodified by:** HAproxy-2.6.0, HAproxy-2.9.10, Mitmproxy-11.1.0

---

## Test 132: With the exception of pseudo-header fields (Section 8.3), which have a name that starts with a single colon, field names MUST NOT include a colon (ASCII COLON, 0x3a).

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 133: A field value MUST NOT contain line feed (ASCII LF, 0x0a). (Tested at the start of the value)

**Modified by:** Cloudflare
**Unmodified by:** Mitmproxy-11.1.0

---

## Test 134: A field value MUST NOT contain carriage return (ASCII CR, 0x0d). (Tested at the start of the value)

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 135: A field value MUST NOT start with an ASCII whitespace character (ASCII SP or HTAB, 0x20 or 0x09).

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 136: A field value MUST NOT end with an ASCII whitespace character (ASCII SP or HTAB, 0x20 or 0x09).

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 51: An endpoint MUST NOT generate an HTTP/2 message containing connection header field (RFC9113 Section 8.2.2)

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 52: An endpoint MUST NOT generate an HTTP/2 message containing proxy-connection header field (RFC9113 Section 8.2.2)

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 53: An endpoint MUST NOT generate an HTTP/2 message containing keep-alive header field (RFC9113 Section 8.2.2)

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 54: An endpoint MUST NOT generate an HTTP/2 message containing transfer-encoding header field (RFC9113 Section 8.2.2)

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 123: An endpoint MUST treat a change to SETTINGS_INITIAL_WINDOW_SIZE that causes any flow-control window to exceed the maximum size as a connection error (Section 5.4.1) of type FLOW_CONTROL_ERROR.

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 55: An endpoint MUST NOT generate an HTTP/2 message containing upgrade header field (RFC9113 Section 8.2.2)

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 56: The TE header field MAY be present in an HTTP/2 request; when it is, it MUST NOT contain any value other than 'trailers'.

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 137: An endpoint MUST NOT generate an HTTP/2 message containing connection header field (RFC9113 Section 8.2.2)

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 138: An endpoint MUST NOT generate an HTTP/2 message containing proxy-connection header field (RFC9113 Section 8.2.2)

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 139: An endpoint MUST NOT generate an HTTP/2 message containing keep-alive header field (RFC9113 Section 8.2.2)

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 140: An endpoint MUST NOT generate an HTTP/2 message containing transfer-encoding header field (RFC9113 Section 8.2.2)

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 141: An endpoint MUST NOT generate an HTTP/2 message containing upgrade header field (RFC9113 Section 8.2.2)

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 142: The TE header field MAY be present in an HTTP/2 request; when it is, it MUST NOT contain any value other than 'trailers'.

**Modified by:** HAproxy-2.9.10, Nghttpx-1.62.1
**Unmodified by:** HAproxy-2.6.0, Mitmproxy-11.1.0, Nghttpx-1.47.0, Node-14.19.3

---

## Test 57: Pseudo-header fields are not HTTP header fields. Endpoints MUST NOT generate pseudo-header fields other than those defined in this document.

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 58: Pseudo-header fields defined for requests MUST NOT appear in responses.

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 60: All pseudo-header fields sent from a client MUST appear in a field block before all regular field lines. Any request or response that contains a pseudo-header field that appears in a field block after a regular field line MUST be treated as malformed (Section 8.1.1).

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 61: All pseudo-header fields sent from a server MUST appear in a field block before all regular field lines. Any request or response that contains a pseudo-header field that appears in a field block after a regular field line MUST be treated as malformed (Section 8.1.1).

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 62: The same pseudo-header field name MUST NOT appear more than once in a field block. A field block for an HTTP request or response that contains a repeated pseudo-header field name MUST be treated as malformed (Section 8.1.1). Tested with a request frame with the same value.

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 63: The same pseudo-header field name MUST NOT appear more than once in a field block. A field block for an HTTP request or response that contains a repeated pseudo-header field name MUST be treated as malformed (Section 8.1.1). Tested with a request frame with different values.

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 64: The same pseudo-header field name MUST NOT appear more than once in a field block. A field block for an HTTP request or response that contains a repeated pseudo-header field name MUST be treated as malformed (Section 8.1.1). Tested with a response frame with the same value.

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 65: The same pseudo-header field name MUST NOT appear more than once in a field block. A field block for an HTTP request or response that contains a repeated pseudo-header field name MUST be treated as malformed (Section 8.1.1). Tested with a response frame with different values.

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 143: Pseudo-header fields are not HTTP header fields. Endpoints MUST NOT generate pseudo-header fields other than those defined in this document.

**Unmodified by:** HAproxy-2.6.0, HAproxy-2.9.10, Mitmproxy-11.1.0, Nghttpx-1.47.0, Nghttpx-1.62.1, Node-14.19.3

---

## Test 66: Clients MUST NOT generate a request with a Host header field that differs from the ":authority" pseudo-header field.

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 67: ':authority' MUST NOT include the deprecated userinfo subcomponent for "http" or "https" schemed URIs.

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 68: The ":path" pseudo-header field MUST NOT be empty for "http" or "https" URIs; "http" or "https" URIs that do not contain a path component MUST include a value of '/'.

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 69: All HTTP/2 requests MUST include exactly one valid value for the ":method", ":scheme", and ":path" pseudo-header fields, unless they are CONNECT requests (Section 8.5). An HTTP request that omits mandatory pseudo-header fields is malformed (Section 8.1.1). (Tested with :method missing)

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 70: All HTTP/2 requests MUST include exactly one valid value for the ":method", ":scheme", and ":path" pseudo-header fields, unless they are CONNECT requests (Section 8.5). An HTTP request that omits mandatory pseudo-header fields is malformed (Section 8.1.1). (Tested with :scheme missing)

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 103: All HTTP/2 requests MUST include exactly one valid value for the ":method", ":scheme", and ":path" pseudo-header fields, unless they are CONNECT requests (Section 8.5). An HTTP request that omits mandatory pseudo-header fields is malformed (Section 8.1.1). (Tested with :path missing)

**Unmodified by:** Mitmproxy-11.1.0, Node-14.19.3

---

## Test 147: Implementations MUST discard frames that have unknown or unsupported types. (server side)

**Unmodified by:** Mitmproxy-11.1.0

---

## Test 32: With the CONNECT method, the " :scheme" and " :path" pseudo-header fields MUST be omitted. (Tested with only :scheme present)

**Unmodified by:** Mitmproxy-11.1.0

---

