# HTTP/2 Section-wise Conformance Results


## Section 3: Starting HTTP/2

| Proxy | Conformant | Non-Conformant | Total Tests |
|-------|------------|----------------|-------------|
| Nghttpx | 3 (75.0%) | 1 (25.0%) | 4 |
| HAproxy | 1 (25.0%) | 3 (75.0%) | 4 |
| Apache | 3 (75.0%) | 1 (25.0%) | 4 |
| Caddy | 3 (75.0%) | 1 (25.0%) | 4 |
| Node | 3 (75.0%) | 1 (25.0%) | 4 |
| Envoy | 3 (75.0%) | 1 (25.0%) | 4 |
| H2O | 1 (25.0%) | 3 (75.0%) | 4 |
| Cloudflare | 0 (0.0%) | 4 (100.0%) | 4 |
| Mitmproxy | 1 (25.0%) | 3 (75.0%) | 4 |
| Azure-AG | 2 (50.0%) | 2 (50.0%) | 4 |
| Nginx | 2 (50.0%) | 2 (50.0%) | 4 |
| Lighttpd | 2 (50.0%) | 2 (50.0%) | 4 |

### Non-Conformant Tests

| Proxy | Test ID | Expected | Actual | Description |
|-------|---------|-----------|--------|-------------|
| Nghttpx | 3 | error | dropped | the connection preface starts with the string: PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n |
| HAproxy | 3 | error | dropped | the connection preface starts with the string: PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n |
| HAproxy | 4 | error | dropped | Client preface must include a SETTINGS frame |
| HAproxy | 87 | error | dropped | A SETTINGS frame MUST be sent by both endpoints at the start of a connection and MAY be sent at any other time by either endpoint over the lifetime of the connection. (Tested from the client side.) |
| Apache | 3 | error | dropped | the connection preface starts with the string: PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n |
| Caddy | 3 | error | dropped | the connection preface starts with the string: PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n |
| Node | 3 | error | dropped | the connection preface starts with the string: PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n |
| Envoy | 3 | error | dropped | the connection preface starts with the string: PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n |
| H2O | 3 | error | dropped | the connection preface starts with the string: PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n |
| H2O | 4 | error | dropped | Client preface must include a SETTINGS frame |
| H2O | 87 | error | dropped | A SETTINGS frame MUST be sent by both endpoints at the start of a connection and MAY be sent at any other time by either endpoint over the lifetime of the connection. (Tested from the client side.) |
| Cloudflare | 2 | error | dropped | Client must send connection preface after TLS establishment |
| Cloudflare | 3 | error | dropped | the connection preface starts with the string: PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n |
| Cloudflare | 4 | error | received | Client preface must include a SETTINGS frame |
| Cloudflare | 87 | error | received | A SETTINGS frame MUST be sent by both endpoints at the start of a connection and MAY be sent at any other time by either endpoint over the lifetime of the connection. (Tested from the client side.) |
| Mitmproxy | 3 | error | received | the connection preface starts with the string: PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n |
| Mitmproxy | 4 | error | received | Client preface must include a SETTINGS frame |
| Mitmproxy | 87 | error | received | A SETTINGS frame MUST be sent by both endpoints at the start of a connection and MAY be sent at any other time by either endpoint over the lifetime of the connection. (Tested from the client side.) |
| Azure-AG | 4 | error | received | Client preface must include a SETTINGS frame |
| Azure-AG | 87 | error | received | A SETTINGS frame MUST be sent by both endpoints at the start of a connection and MAY be sent at any other time by either endpoint over the lifetime of the connection. (Tested from the client side.) |
| Nginx | 4 | error | received | Client preface must include a SETTINGS frame |
| Nginx | 87 | error | received | A SETTINGS frame MUST be sent by both endpoints at the start of a connection and MAY be sent at any other time by either endpoint over the lifetime of the connection. (Tested from the client side.) |
| Lighttpd | 4 | error | received | Client preface must include a SETTINGS frame |
| Lighttpd | 87 | error | received | A SETTINGS frame MUST be sent by both endpoints at the start of a connection and MAY be sent at any other time by either endpoint over the lifetime of the connection. (Tested from the client side.) |

## Section 4: HTTP Frames

| Proxy | Conformant | Non-Conformant | Total Tests |
|-------|------------|----------------|-------------|
| Nghttpx | 7 (87.5%) | 1 (12.5%) | 8 |
| HAproxy | 4 (50.0%) | 4 (50.0%) | 8 |
| Apache | 4 (50.0%) | 4 (50.0%) | 8 |
| Caddy | 3 (37.5%) | 5 (62.5%) | 8 |
| Node | 7 (87.5%) | 1 (12.5%) | 8 |
| Envoy | 4 (50.0%) | 4 (50.0%) | 8 |
| H2O | 7 (87.5%) | 1 (12.5%) | 8 |
| Cloudflare | 6 (75.0%) | 2 (25.0%) | 8 |
| Mitmproxy | 4 (50.0%) | 4 (50.0%) | 8 |
| Azure-AG | 3 (75.0%) | 1 (25.0%) | 4 |
| Nginx | 3 (75.0%) | 1 (25.0%) | 4 |
| Lighttpd | 4 (100.0%) | 0 (0.0%) | 4 |

### Non-Conformant Tests

| Proxy | Test ID | Expected | Actual | Description |
|-------|---------|-----------|--------|-------------|
| Nghttpx | 110 | ignore | received | A reserved 1-bit field. The semantics of this bit are undefined, and the bit MUST remain unset (0x00) when sending and MUST be ignored when receiving. (server side) |
| HAproxy | 10 | ignore | 500 | A reserved 1-bit field. The semantics of this bit are undefined, and the bit MUST remain unset (0x00) when sending and MUST be ignored when receiving. |
| HAproxy | 109 | ignore | 500 | The frame type determines the format and semantics of the frame. Implementations MUST ignore and discard frames of unknown types. (server side) |
| HAproxy | 110 | ignore | received | A reserved 1-bit field. The semantics of this bit are undefined, and the bit MUST remain unset (0x00) when sending and MUST be ignored when receiving. (server side) |
| HAproxy | 147 | ignore | 500 | Implementations MUST discard frames that have unknown or unsupported types. |
| Apache | 10 | ignore | 500 | A reserved 1-bit field. The semantics of this bit are undefined, and the bit MUST remain unset (0x00) when sending and MUST be ignored when receiving. |
| Apache | 109 | ignore | 500 | The frame type determines the format and semantics of the frame. Implementations MUST ignore and discard frames of unknown types. (server side) |
| Apache | 110 | ignore | 500 | A reserved 1-bit field. The semantics of this bit are undefined, and the bit MUST remain unset (0x00) when sending and MUST be ignored when receiving. (server side) |
| Apache | 147 | ignore | 500 | Implementations MUST discard frames that have unknown or unsupported types. |
| Caddy | 10 | ignore | 500 | A reserved 1-bit field. The semantics of this bit are undefined, and the bit MUST remain unset (0x00) when sending and MUST be ignored when receiving. |
| Caddy | 79 | ignore | other | Implementations MUST discard frames that have unknown or unsupported types. |
| Caddy | 109 | ignore | 500 | The frame type determines the format and semantics of the frame. Implementations MUST ignore and discard frames of unknown types. (server side) |
| Caddy | 110 | ignore | received | A reserved 1-bit field. The semantics of this bit are undefined, and the bit MUST remain unset (0x00) when sending and MUST be ignored when receiving. (server side) |
| Caddy | 147 | ignore | 500 | Implementations MUST discard frames that have unknown or unsupported types. |
| Node | 110 | ignore | received | A reserved 1-bit field. The semantics of this bit are undefined, and the bit MUST remain unset (0x00) when sending and MUST be ignored when receiving. (server side) |
| Envoy | 10 | ignore | 500 | A reserved 1-bit field. The semantics of this bit are undefined, and the bit MUST remain unset (0x00) when sending and MUST be ignored when receiving. |
| Envoy | 109 | ignore | 500 | The frame type determines the format and semantics of the frame. Implementations MUST ignore and discard frames of unknown types. (server side) |
| Envoy | 110 | ignore | received | A reserved 1-bit field. The semantics of this bit are undefined, and the bit MUST remain unset (0x00) when sending and MUST be ignored when receiving. (server side) |
| Envoy | 147 | ignore | 500 | Implementations MUST discard frames that have unknown or unsupported types. |
| H2O | 108 | error | dropped | Values greater than 16,384 MUST NOT be sent unless receiver has set larger SETTINGS_MAX_FRAME_SIZE. (server side) |
| Cloudflare | 8 | error | received | Values greater than 16,384 MUST NOT be sent unless receiver has set larger SETTINGS_MAX_FRAME_SIZE |
| Cloudflare | 110 | ignore | received | A reserved 1-bit field. The semantics of this bit are undefined, and the bit MUST remain unset (0x00) when sending and MUST be ignored when receiving. (server side) |
| Mitmproxy | 8 | error | received | Values greater than 16,384 MUST NOT be sent unless receiver has set larger SETTINGS_MAX_FRAME_SIZE |
| Mitmproxy | 10 | ignore | received | A reserved 1-bit field. The semantics of this bit are undefined, and the bit MUST remain unset (0x00) when sending and MUST be ignored when receiving. |
| Mitmproxy | 108 | error | received | Values greater than 16,384 MUST NOT be sent unless receiver has set larger SETTINGS_MAX_FRAME_SIZE. (server side) |
| Mitmproxy | 110 | ignore | received | A reserved 1-bit field. The semantics of this bit are undefined, and the bit MUST remain unset (0x00) when sending and MUST be ignored when receiving. (server side) |
| Azure-AG | 8 | error | received | Values greater than 16,384 MUST NOT be sent unless receiver has set larger SETTINGS_MAX_FRAME_SIZE |
| Nginx | 8 | error | received | Values greater than 16,384 MUST NOT be sent unless receiver has set larger SETTINGS_MAX_FRAME_SIZE |

## Section 5: Streams and Multiplexing

| Proxy | Conformant | Non-Conformant | Total Tests |
|-------|------------|----------------|-------------|
| Nghttpx | 27 (77.1%) | 8 (22.9%) | 35 |
| HAproxy | 28 (80.0%) | 7 (20.0%) | 35 |
| Apache | 29 (82.9%) | 6 (17.1%) | 35 |
| Caddy | 27 (77.1%) | 8 (22.9%) | 35 |
| Node | 27 (77.1%) | 8 (22.9%) | 35 |
| Envoy | 18 (51.4%) | 17 (48.6%) | 35 |
| H2O | 18 (51.4%) | 17 (48.6%) | 35 |
| Cloudflare | 14 (40.0%) | 21 (60.0%) | 35 |
| Mitmproxy | 3 (8.6%) | 32 (91.4%) | 35 |
| Azure-AG | 8 (47.1%) | 9 (52.9%) | 17 |
| Nginx | 9 (52.9%) | 8 (47.1%) | 17 |
| Lighttpd | 13 (76.5%) | 4 (23.5%) | 17 |

### Non-Conformant Tests

| Proxy | Test ID | Expected | Actual | Description |
|-------|---------|-----------|--------|-------------|
| Nghttpx | 13 | error | dropped | The identifier of a newly established stream MUST be numerically greater than all streams that the initiating endpoint has opened or reserved. |
| Nghttpx | 14 | error | dropped | An endpoint MUST NOT send a RST_STREAM in response to a RST_STREAM frame |
| Nghttpx | 16 | error | dropped | After receiving a RST_STREAM on a stream, the receiver MUST NOT send additional frames for that stream, except for PRIORITY |
| Nghttpx | 76 | error | dropped | An endpoint MUST NOT send frames other than PRIORITY on a closed stream. |
| Nghttpx | 84 | error | dropped | If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the closed state.) |
| Nghttpx | 144 | error | dropped | An endpoint MUST NOT send frames other than PRIORITY on a closed stream. |
| Nghttpx | 151 | error | received | If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the half-closed (remote) state.) |
| Nghttpx | 152 | error | dropped | If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the closed state.) |
| HAproxy | 7 | error | dropped | If an endpoint receives additional frames, other than WINDOW_UPDATE, PRIORITY, or RST_STREAM, for a stream that is in the half-closed (remote) state, it MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. |
| HAproxy | 14 | error | dropped | An endpoint MUST NOT send a RST_STREAM in response to a RST_STREAM frame |
| HAproxy | 16 | error | dropped | After receiving a RST_STREAM on a stream, the receiver MUST NOT send additional frames for that stream, except for PRIORITY |
| HAproxy | 83 | error | dropped | If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the half-closed (remote) state.) |
| HAproxy | 84 | error | dropped | If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the closed state.) |
| HAproxy | 144 | error | dropped | An endpoint MUST NOT send frames other than PRIORITY on a closed stream. |
| HAproxy | 151 | error | received | If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the half-closed (remote) state.) |
| Apache | 14 | error | dropped | An endpoint MUST NOT send a RST_STREAM in response to a RST_STREAM frame |
| Apache | 16 | error | dropped | After receiving a RST_STREAM on a stream, the receiver MUST NOT send additional frames for that stream, except for PRIORITY |
| Apache | 76 | error | dropped | An endpoint MUST NOT send frames other than PRIORITY on a closed stream. |
| Apache | 84 | error | dropped | If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the closed state.) |
| Apache | 144 | error | dropped | An endpoint MUST NOT send frames other than PRIORITY on a closed stream. |
| Apache | 151 | error | received | If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the half-closed (remote) state.) |
| Caddy | 7 | error | dropped | If an endpoint receives additional frames, other than WINDOW_UPDATE, PRIORITY, or RST_STREAM, for a stream that is in the half-closed (remote) state, it MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. |
| Caddy | 14 | error | dropped | An endpoint MUST NOT send a RST_STREAM in response to a RST_STREAM frame |
| Caddy | 16 | error | dropped | After receiving a RST_STREAM on a stream, the receiver MUST NOT send additional frames for that stream, except for PRIORITY |
| Caddy | 83 | error | dropped | If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the half-closed (remote) state.) |
| Caddy | 84 | error | dropped | If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the closed state.) |
| Caddy | 144 | error | dropped | An endpoint MUST NOT send frames other than PRIORITY on a closed stream. |
| Caddy | 149 | error | dropped | If a DATA frame is received whose Stream Identifier field is 0x00, the recipient MUST respond with a connection error (Section 5.4.1) of type PROTOCOL_ERROR. |
| Caddy | 151 | error | received | If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the half-closed (remote) state.) |
| Node | 13 | error | dropped | The identifier of a newly established stream MUST be numerically greater than all streams that the initiating endpoint has opened or reserved. |
| Node | 14 | error | dropped | An endpoint MUST NOT send a RST_STREAM in response to a RST_STREAM frame |
| Node | 16 | error | dropped | After receiving a RST_STREAM on a stream, the receiver MUST NOT send additional frames for that stream, except for PRIORITY |
| Node | 76 | error | dropped | An endpoint MUST NOT send frames other than PRIORITY on a closed stream. |
| Node | 84 | error | dropped | If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the closed state.) |
| Node | 144 | error | dropped | An endpoint MUST NOT send frames other than PRIORITY on a closed stream. |
| Node | 151 | error | received | If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the half-closed (remote) state.) |
| Node | 152 | error | dropped | If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the closed state.) |
| Envoy | 11 | error | dropped | Streams initiated by a client MUST use odd-numbered stream identifiers. |
| Envoy | 13 | error | dropped | The identifier of a newly established stream MUST be numerically greater than all streams that the initiating endpoint has opened or reserved. |
| Envoy | 14 | error | dropped | An endpoint MUST NOT send a RST_STREAM in response to a RST_STREAM frame |
| Envoy | 15 | error | dropped | If a PRIORITY frame is received with a stream identifier of 0x00, the recipient MUST respond with a connection error of type PROTOCOL_ERROR |
| Envoy | 16 | error | dropped | After receiving a RST_STREAM on a stream, the receiver MUST NOT send additional frames for that stream, except for PRIORITY |
| Envoy | 17 | error | dropped | If a RST_STREAM frame is received with a stream identifier of 0x00, the recipient MUST treat this as a connection error (Section 5.4.1) of type PROTOCOL_ERROR. |
| Envoy | 72 | error | dropped | A client cannot push. Thus, servers MUST treat the receipt of a PUSH_PROMISE frame as a connection error (Section 5.4.1) of type PROTOCOL_ERROR. |
| Envoy | 76 | error | dropped | An endpoint MUST NOT send frames other than PRIORITY on a closed stream. |
| Envoy | 77 | error | dropped | RST_STREAM frames MUST NOT be sent for a stream in the 'idle' state. |
| Envoy | 78 | error | dropped | RST_STREAM frames MUST be associated with a stream. |
| Envoy | 84 | error | dropped | If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the closed state.) |
| Envoy | 86 | error | dropped | If a HEADERS frame is received whose Stream Identifier field is 0x00, the recipient MUST respond with a connection error (Section 5.4.1) of type PROTOCOL_ERROR. |
| Envoy | 105 | error | dropped | PUSH_PROMISE frames MUST NOT be sent by the client. |
| Envoy | 144 | error | dropped | An endpoint MUST NOT send frames other than PRIORITY on a closed stream. |
| Envoy | 150 | error | dropped | If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the idle state.) |
| Envoy | 151 | error | received | If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the half-closed (remote) state.) |
| Envoy | 152 | error | dropped | If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the closed state.) |
| H2O | 5 | error | dropped | If this stream (initially in the idle state) is initiated by the server, as described in Section 5.1.1, then receiving a HEADERS frame MUST also be treated as a connection error (Section 5.4.1) of type PROTOCOL_ERROR. |
| H2O | 6 | error | dropped | An endpoint MUST NOT send any type of frame other than HEADERS, RST_STREAM, or PRIORITY in the reserved (local) state. |
| H2O | 7 | error | dropped | If an endpoint receives additional frames, other than WINDOW_UPDATE, PRIORITY, or RST_STREAM, for a stream that is in the half-closed (remote) state, it MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. |
| H2O | 12 | error | dropped | Streams initiated by a server MUST use even-numbered stream identifiers. |
| H2O | 14 | error | dropped | An endpoint MUST NOT send a RST_STREAM in response to a RST_STREAM frame |
| H2O | 16 | error | dropped | After receiving a RST_STREAM on a stream, the receiver MUST NOT send additional frames for that stream, except for PRIORITY |
| H2O | 29 | error | dropped | The promised stream identifier MUST be a valid choice for the next stream sent by the sender (see 'new stream identifier' in Section 5.1.1). (Using Odd-numbered Stream ID (Invalid for Server)) |
| H2O | 83 | error | dropped | If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the half-closed (remote) state.) |
| H2O | 84 | error | dropped | If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the closed state.) |
| H2O | 89 | error | dropped | The promised stream identifier MUST be a valid choice for the next stream sent by the sender (see 'new stream identifier' in Section 5.1.1). (Using Already Used Stream ID) |
| H2O | 90 | error | dropped | The promised stream identifier MUST be a valid choice for the next stream sent by the sender (see 'new stream identifier' in Section 5.1.1). (Using Lower Stream ID) |
| H2O | 106 | error | dropped | Receiving any frame other than HEADERS or PRIORITY on a stream in this (idle) state MUST be treated as a connection error (Section 5.4.1) of type PROTOCOL_ERROR. (server side) |
| H2O | 107 | error | dropped | If an endpoint receives additional frames, other than WINDOW_UPDATE, PRIORITY, or RST_STREAM, for a stream that is in the half-closed (remote) state, it MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (server side) |
| H2O | 144 | error | dropped | An endpoint MUST NOT send frames other than PRIORITY on a closed stream. |
| H2O | 149 | error | dropped | If a DATA frame is received whose Stream Identifier field is 0x00, the recipient MUST respond with a connection error (Section 5.4.1) of type PROTOCOL_ERROR. |
| H2O | 151 | error | dropped | If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the half-closed (remote) state.) |
| H2O | 152 | error | dropped | If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the closed state.) |
| Cloudflare | 1 | error | dropped | Receiving any frame other than HEADERS or PRIORITY on a stream in this (idle) state MUST be treated as a connection error (Section 5.4.1) of type PROTOCOL_ERROR. |
| Cloudflare | 7 | error | dropped | If an endpoint receives additional frames, other than WINDOW_UPDATE, PRIORITY, or RST_STREAM, for a stream that is in the half-closed (remote) state, it MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. |
| Cloudflare | 11 | error | dropped | Streams initiated by a client MUST use odd-numbered stream identifiers. |
| Cloudflare | 13 | error | dropped | The identifier of a newly established stream MUST be numerically greater than all streams that the initiating endpoint has opened or reserved. |
| Cloudflare | 14 | error | dropped | An endpoint MUST NOT send a RST_STREAM in response to a RST_STREAM frame |
| Cloudflare | 15 | error | dropped | If a PRIORITY frame is received with a stream identifier of 0x00, the recipient MUST respond with a connection error of type PROTOCOL_ERROR |
| Cloudflare | 16 | error | dropped | After receiving a RST_STREAM on a stream, the receiver MUST NOT send additional frames for that stream, except for PRIORITY |
| Cloudflare | 17 | error | dropped | If a RST_STREAM frame is received with a stream identifier of 0x00, the recipient MUST treat this as a connection error (Section 5.4.1) of type PROTOCOL_ERROR. |
| Cloudflare | 72 | error | dropped | A client cannot push. Thus, servers MUST treat the receipt of a PUSH_PROMISE frame as a connection error (Section 5.4.1) of type PROTOCOL_ERROR. |
| Cloudflare | 77 | error | dropped | RST_STREAM frames MUST NOT be sent for a stream in the 'idle' state. |
| Cloudflare | 78 | error | dropped | RST_STREAM frames MUST be associated with a stream. |
| Cloudflare | 80 | error | dropped | DATA frames MUST be associated with a stream. |
| Cloudflare | 81 | error | dropped | If a DATA frame is received whose Stream Identifier field is 0x00, the recipient MUST respond with a connection error (Section 5.4.1) of type PROTOCOL_ERROR. |
| Cloudflare | 82 | error | dropped | If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the idle state.) |
| Cloudflare | 83 | error | dropped | If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the half-closed (remote) state.) |
| Cloudflare | 84 | error | dropped | If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the closed state.) |
| Cloudflare | 86 | error | dropped | If a HEADERS frame is received whose Stream Identifier field is 0x00, the recipient MUST respond with a connection error (Section 5.4.1) of type PROTOCOL_ERROR. |
| Cloudflare | 105 | error | dropped | PUSH_PROMISE frames MUST NOT be sent by the client. |
| Cloudflare | 107 | error | dropped | If an endpoint receives additional frames, other than WINDOW_UPDATE, PRIORITY, or RST_STREAM, for a stream that is in the half-closed (remote) state, it MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (server side) |
| Cloudflare | 144 | error | dropped | An endpoint MUST NOT send frames other than PRIORITY on a closed stream. |
| Cloudflare | 151 | error | received | If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the half-closed (remote) state.) |
| Mitmproxy | 1 | error | received | Receiving any frame other than HEADERS or PRIORITY on a stream in this (idle) state MUST be treated as a connection error (Section 5.4.1) of type PROTOCOL_ERROR. |
| Mitmproxy | 5 | error | received | If this stream (initially in the idle state) is initiated by the server, as described in Section 5.1.1, then receiving a HEADERS frame MUST also be treated as a connection error (Section 5.4.1) of type PROTOCOL_ERROR. |
| Mitmproxy | 6 | error | received | An endpoint MUST NOT send any type of frame other than HEADERS, RST_STREAM, or PRIORITY in the reserved (local) state. |
| Mitmproxy | 7 | error | received | If an endpoint receives additional frames, other than WINDOW_UPDATE, PRIORITY, or RST_STREAM, for a stream that is in the half-closed (remote) state, it MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. |
| Mitmproxy | 11 | error | received | Streams initiated by a client MUST use odd-numbered stream identifiers. |
| Mitmproxy | 12 | error | received | Streams initiated by a server MUST use even-numbered stream identifiers. |
| Mitmproxy | 13 | error | received | The identifier of a newly established stream MUST be numerically greater than all streams that the initiating endpoint has opened or reserved. |
| Mitmproxy | 14 | error | dropped | An endpoint MUST NOT send a RST_STREAM in response to a RST_STREAM frame |
| Mitmproxy | 15 | error | received | If a PRIORITY frame is received with a stream identifier of 0x00, the recipient MUST respond with a connection error of type PROTOCOL_ERROR |
| Mitmproxy | 16 | error | dropped | After receiving a RST_STREAM on a stream, the receiver MUST NOT send additional frames for that stream, except for PRIORITY |
| Mitmproxy | 29 | error | received | The promised stream identifier MUST be a valid choice for the next stream sent by the sender (see 'new stream identifier' in Section 5.1.1). (Using Odd-numbered Stream ID (Invalid for Server)) |
| Mitmproxy | 72 | error | received | A client cannot push. Thus, servers MUST treat the receipt of a PUSH_PROMISE frame as a connection error (Section 5.4.1) of type PROTOCOL_ERROR. |
| Mitmproxy | 76 | error | dropped | An endpoint MUST NOT send frames other than PRIORITY on a closed stream. |
| Mitmproxy | 77 | error | dropped | RST_STREAM frames MUST NOT be sent for a stream in the 'idle' state. |
| Mitmproxy | 78 | error | dropped | RST_STREAM frames MUST be associated with a stream. |
| Mitmproxy | 80 | error | received | DATA frames MUST be associated with a stream. |
| Mitmproxy | 81 | error | received | If a DATA frame is received whose Stream Identifier field is 0x00, the recipient MUST respond with a connection error (Section 5.4.1) of type PROTOCOL_ERROR. |
| Mitmproxy | 82 | error | received | If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the idle state.) |
| Mitmproxy | 83 | error | received | If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the half-closed (remote) state.) |
| Mitmproxy | 84 | error | dropped | If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the closed state.) |
| Mitmproxy | 86 | error | received | If a HEADERS frame is received whose Stream Identifier field is 0x00, the recipient MUST respond with a connection error (Section 5.4.1) of type PROTOCOL_ERROR. |
| Mitmproxy | 89 | error | received | The promised stream identifier MUST be a valid choice for the next stream sent by the sender (see 'new stream identifier' in Section 5.1.1). (Using Already Used Stream ID) |
| Mitmproxy | 90 | error | received | The promised stream identifier MUST be a valid choice for the next stream sent by the sender (see 'new stream identifier' in Section 5.1.1). (Using Lower Stream ID) |
| Mitmproxy | 105 | error | received | PUSH_PROMISE frames MUST NOT be sent by the client. |
| Mitmproxy | 106 | error | received | Receiving any frame other than HEADERS or PRIORITY on a stream in this (idle) state MUST be treated as a connection error (Section 5.4.1) of type PROTOCOL_ERROR. (server side) |
| Mitmproxy | 107 | error | received | If an endpoint receives additional frames, other than WINDOW_UPDATE, PRIORITY, or RST_STREAM, for a stream that is in the half-closed (remote) state, it MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (server side) |
| Mitmproxy | 144 | error | dropped | An endpoint MUST NOT send frames other than PRIORITY on a closed stream. |
| Mitmproxy | 148 | error | received | DATA frames MUST be associated with a stream. |
| Mitmproxy | 149 | error | received | If a DATA frame is received whose Stream Identifier field is 0x00, the recipient MUST respond with a connection error (Section 5.4.1) of type PROTOCOL_ERROR. |
| Mitmproxy | 150 | error | received | If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the idle state.) |
| Mitmproxy | 151 | error | received | If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the half-closed (remote) state.) |
| Mitmproxy | 152 | error | dropped | If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the closed state.) |
| Azure-AG | 1 | error | dropped | Receiving any frame other than HEADERS or PRIORITY on a stream in this (idle) state MUST be treated as a connection error (Section 5.4.1) of type PROTOCOL_ERROR. |
| Azure-AG | 7 | error | dropped | If an endpoint receives additional frames, other than WINDOW_UPDATE, PRIORITY, or RST_STREAM, for a stream that is in the half-closed (remote) state, it MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. |
| Azure-AG | 77 | error | dropped | RST_STREAM frames MUST NOT be sent for a stream in the 'idle' state. |
| Azure-AG | 78 | error | dropped | RST_STREAM frames MUST be associated with a stream. |
| Azure-AG | 80 | error | dropped | DATA frames MUST be associated with a stream. |
| Azure-AG | 81 | error | dropped | If a DATA frame is received whose Stream Identifier field is 0x00, the recipient MUST respond with a connection error (Section 5.4.1) of type PROTOCOL_ERROR. |
| Azure-AG | 82 | error | dropped | If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the idle state.) |
| Azure-AG | 83 | error | dropped | If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the half-closed (remote) state.) |
| Azure-AG | 84 | error | dropped | If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the closed state.) |
| Nginx | 1 | error | dropped | Receiving any frame other than HEADERS or PRIORITY on a stream in this (idle) state MUST be treated as a connection error (Section 5.4.1) of type PROTOCOL_ERROR. |
| Nginx | 7 | error | dropped | If an endpoint receives additional frames, other than WINDOW_UPDATE, PRIORITY, or RST_STREAM, for a stream that is in the half-closed (remote) state, it MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. |
| Nginx | 77 | error | dropped | RST_STREAM frames MUST NOT be sent for a stream in the 'idle' state. |
| Nginx | 78 | error | dropped | RST_STREAM frames MUST be associated with a stream. |
| Nginx | 80 | error | dropped | DATA frames MUST be associated with a stream. |
| Nginx | 82 | error | dropped | If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the idle state.) |
| Nginx | 83 | error | dropped | If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the half-closed (remote) state.) |
| Nginx | 84 | error | dropped | If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the closed state.) |
| Lighttpd | 7 | error | received | If an endpoint receives additional frames, other than WINDOW_UPDATE, PRIORITY, or RST_STREAM, for a stream that is in the half-closed (remote) state, it MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. |
| Lighttpd | 76 | error | dropped | An endpoint MUST NOT send frames other than PRIORITY on a closed stream. |
| Lighttpd | 83 | error | received | If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the half-closed (remote) state.) |
| Lighttpd | 84 | error | dropped | If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the closed state.) |

## Section 6: Frame Definitions

| Proxy | Conformant | Non-Conformant | Total Tests |
|-------|------------|----------------|-------------|
| Nghttpx | 46 (93.9%) | 3 (6.1%) | 49 |
| HAproxy | 45 (91.8%) | 4 (8.2%) | 49 |
| Apache | 45 (91.8%) | 4 (8.2%) | 49 |
| Caddy | 44 (89.8%) | 5 (10.2%) | 49 |
| Node | 37 (75.5%) | 12 (24.5%) | 49 |
| Envoy | 33 (67.3%) | 16 (32.7%) | 49 |
| H2O | 31 (63.3%) | 18 (36.7%) | 49 |
| Cloudflare | 27 (55.1%) | 22 (44.9%) | 49 |
| Mitmproxy | 1 (2.0%) | 48 (98.0%) | 49 |
| Azure-AG | 16 (80.0%) | 4 (20.0%) | 20 |
| Nginx | 19 (95.0%) | 1 (5.0%) | 20 |
| Lighttpd | 19 (95.0%) | 1 (5.0%) | 20 |

### Non-Conformant Tests

| Proxy | Test ID | Expected | Actual | Description |
|-------|---------|-----------|--------|-------------|
| Nghttpx | 93 | error | dropped | The sender MUST NOT send a flow-controlled frame with a length that exceeds the space available in either of the flow-control windows advertised by the receiver. |
| Nghttpx | 111 | error | dropped | If a PRIORITY frame is received with a stream identifier of 0x00, the recipient MUST respond with a connection error of type PROTOCOL_ERROR. (server side) |
| Nghttpx | 156 | error | dropped | The sender MUST NOT send a flow-controlled frame with a length that exceeds the space available in either of the flow-control windows advertised by the receiver. |
| HAproxy | 93 | error | dropped | The sender MUST NOT send a flow-controlled frame with a length that exceeds the space available in either of the flow-control windows advertised by the receiver. |
| HAproxy | 119 | ignore | 500 | An endpoint that receives a SETTINGS frame with any unknown or unsupported identifier MUST ignore that setting. |
| HAproxy | 155 | ignore | 500 | Unsupported settings MUST be ignored. |
| HAproxy | 156 | error | dropped | The sender MUST NOT send a flow-controlled frame with a length that exceeds the space available in either of the flow-control windows advertised by the receiver. |
| Apache | 93 | error | dropped | The sender MUST NOT send a flow-controlled frame with a length that exceeds the space available in either of the flow-control windows advertised by the receiver. |
| Apache | 119 | ignore | 500 | An endpoint that receives a SETTINGS frame with any unknown or unsupported identifier MUST ignore that setting. |
| Apache | 155 | ignore | 500 | Unsupported settings MUST be ignored. |
| Apache | 156 | error | dropped | The sender MUST NOT send a flow-controlled frame with a length that exceeds the space available in either of the flow-control windows advertised by the receiver. |
| Caddy | 93 | error | dropped | The sender MUST NOT send a flow-controlled frame with a length that exceeds the space available in either of the flow-control windows advertised by the receiver. |
| Caddy | 119 | ignore | 500 | An endpoint that receives a SETTINGS frame with any unknown or unsupported identifier MUST ignore that setting. |
| Caddy | 125 | error | dropped | A CONTINUATION frame MUST be preceded by a HEADERS, PUSH_PROMISE or CONTINUATION frame without the END_HEADERS flag set. (Using HEADERS frame with END_HEADERS flag set) |
| Caddy | 155 | ignore | 500 | Unsupported settings MUST be ignored. |
| Caddy | 156 | error | dropped | The sender MUST NOT send a flow-controlled frame with a length that exceeds the space available in either of the flow-control windows advertised by the receiver. |
| Node | 24 | error | dropped | A server MUST NOT send a PUSH_PROMISE frame if it receives the SETTINGS_ENABLE_PUSH (0x02) parameter set to a value of 0. |
| Node | 28 | error | dropped | If the Stream Identifier field of a PUSH_PROMISE frame specifies the value 0x00, a recipient MUST respond with a connection error (Section 5.4.1) of type PROTOCOL_ERROR. |
| Node | 39 | error | dropped | The header fields in PUSH_PROMISE and any subsequent CONTINUATION frames MUST be a valid and complete set of request header fields. |
| Node | 85 | error | dropped | A HEADERS frame without the END_HEADERS flag set MUST be followed by a CONTINUATION frame for the same stream. |
| Node | 92 | error | dropped | PUSH_PROMISE MUST NOT be sent if the SETTINGS_ENABLE_PUSH setting of the peer endpoint is set to 0. |
| Node | 93 | error | dropped | The sender MUST NOT send a flow-controlled frame with a length that exceeds the space available in either of the flow-control windows advertised by the receiver. |
| Node | 122 | error | dropped | A sender MUST NOT allow a flow-control window to exceed 2^31-1 octets. If a sender receives a WINDOW_UPDATE that causes a flow-control window to exceed this maximum, it MUST terminate either the stream or the connection, as appropriate. |
| Node | 125 | error | dropped | A CONTINUATION frame MUST be preceded by a HEADERS, PUSH_PROMISE or CONTINUATION frame without the END_HEADERS flag set. (Using HEADERS frame with END_HEADERS flag set) |
| Node | 156 | error | dropped | The sender MUST NOT send a flow-controlled frame with a length that exceeds the space available in either of the flow-control windows advertised by the receiver. |
| Node | 157 | error | dropped | CONTINUATION frames MUST be associated with a stream. |
| Node | 158 | error | dropped | If the END_HEADERS flag is not set, this frame MUST be followed by another CONTINUATION frame. A receiver MUST treat the receipt of any other type of frame or a frame on a different stream as a connection error (Section 5.4.1) of type PROTOCOL_ERROR. |
| Node | 159 | error | dropped | Other frames (from any stream) MUST NOT occur between the HEADERS frame and any CONTINUATION frames that might follow. |
| Envoy | 20 | error | dropped | The stream identifier for a SETTINGS frame MUST be zero (0x00). |
| Envoy | 22 | error | dropped | The initial value of SETTINGS_ENABLE_PUSH is 1. Any value other than 0 or 1 MUST be treated as a connection error (Section 5.4.1) of type PROTOCOL_ERROR. |
| Envoy | 25 | error | dropped | For SETTINGS_INITIAL_WINDOW_SIZE, values above the maximum flow-control window size of 2^31-1 (2147483647) MUST be treated as a connection error (Section 5.4.1) of type FLOW_CONTROL_ERROR. |
| Envoy | 26 | error | dropped | The value advertised by an endpoint MUST be between initial value (2^14 = 16,384) and maximum allowed frame size (2^24-1 = 16,777,215 octets), inclusive. |
| Envoy | 30 | error | dropped | If a PING frame is received with a Stream Identifier field value other than 0x00, the recipient MUST respond with a connection error (Section 5.4.1) of type PROTOCOL_ERROR. |
| Envoy | 33 | error | dropped | A receiver MUST treat the receipt of a WINDOW_UPDATE frame with a flow-control window increment of 0 as a stream error (Section 5.4.2) of type PROTOCOL_ERROR. |
| Envoy | 34 | error | dropped | A sender MUST NOT allow a flow-control window to exceed 2^31-1 octets. If a sender receives a WINDOW_UPDATE that causes a flow-control window to exceed this maximum, it MUST terminate either the stream or the connection, as appropriate. |
| Envoy | 35 | error | dropped | An endpoint MUST treat a change to SETTINGS_INITIAL_WINDOW_SIZE that causes any flow-control window to exceed the maximum size as a connection error (Section 5.4.1) of type FLOW_CONTROL_ERROR. |
| Envoy | 93 | error | dropped | The sender MUST NOT send a flow-controlled frame with a length that exceeds the space available in either of the flow-control windows advertised by the receiver. |
| Envoy | 119 | ignore | 500 | An endpoint that receives a SETTINGS frame with any unknown or unsupported identifier MUST ignore that setting. |
| Envoy | 123 | error | dropped | An endpoint MUST treat a change to SETTINGS_INITIAL_WINDOW_SIZE that causes any flow-control window to exceed the maximum size as a connection error (Section 5.4.1) of type FLOW_CONTROL_ERROR. |
| Envoy | 125 | error | dropped | A CONTINUATION frame MUST be preceded by a HEADERS, PUSH_PROMISE or CONTINUATION frame without the END_HEADERS flag set. (Using HEADERS frame with END_HEADERS flag set) |
| Envoy | 155 | ignore | 500 | Unsupported settings MUST be ignored. |
| Envoy | 156 | error | dropped | The sender MUST NOT send a flow-controlled frame with a length that exceeds the space available in either of the flow-control windows advertised by the receiver. |
| Envoy | 158 | error | dropped | If the END_HEADERS flag is not set, this frame MUST be followed by another CONTINUATION frame. A receiver MUST treat the receipt of any other type of frame or a frame on a different stream as a connection error (Section 5.4.1) of type PROTOCOL_ERROR. |
| Envoy | 159 | error | dropped | Other frames (from any stream) MUST NOT occur between the HEADERS frame and any CONTINUATION frames that might follow. |
| H2O | 23 | error | dropped | A server MUST NOT explicitly set this value (SETTINGS_ENABLE_PUSH) to 1. A server MAY choose to omit this setting (SETTINGS_ENABLE_PUSH) when it sends a SETTINGS frame, but if a server does include a value, it MUST be 0. |
| H2O | 24 | error | dropped | A server MUST NOT send a PUSH_PROMISE frame if it receives the SETTINGS_ENABLE_PUSH (0x02) parameter set to a value of 0. |
| H2O | 28 | error | dropped | If the Stream Identifier field of a PUSH_PROMISE frame specifies the value 0x00, a recipient MUST respond with a connection error (Section 5.4.1) of type PROTOCOL_ERROR. |
| H2O | 38 | error | dropped | A CONTINUATION frame MUST be preceded by a HEADERS, PUSH_PROMISE or CONTINUATION frame without the END_HEADERS flag set. (Using PUSH_PROMISE frame with END_HEADERS flag set) |
| H2O | 39 | error | dropped | The header fields in PUSH_PROMISE and any subsequent CONTINUATION frames MUST be a valid and complete set of request header fields. |
| H2O | 91 | error | dropped | A PUSH_PROMISE frame without the END_HEADERS flag set MUST be followed by a CONTINUATION frame for the same stream. |
| H2O | 92 | error | dropped | PUSH_PROMISE MUST NOT be sent if the SETTINGS_ENABLE_PUSH setting of the peer endpoint is set to 0. |
| H2O | 93 | error | dropped | The sender MUST NOT send a flow-controlled frame with a length that exceeds the space available in either of the flow-control windows advertised by the receiver. |
| H2O | 111 | error | dropped | If a PRIORITY frame is received with a stream identifier of 0x00, the recipient MUST respond with a connection error of type PROTOCOL_ERROR. (server side) |
| H2O | 112 | error | dropped | If a RST_STREAM frame is received with a stream identifier of 0x00, the recipient MUST treat this as a connection error (Section 5.4.1) of type PROTOCOL_ERROR. (server side) |
| H2O | 113 | error | dropped | When set, the ACK flag indicates that this frame acknowledges receipt and application of the peer's SETTINGS frame. When this bit is set, the frame payload of the SETTINGS frame MUST be empty. (server side) |
| H2O | 114 | error | dropped | A RST_STREAM frame with a length other than 4 octets MUST be treated as a connection error (Section 5.4.1) of type FRAME_SIZE_ERROR. (server side) |
| H2O | 115 | error | dropped | The stream identifier for a SETTINGS frame MUST be zero (0x00). |
| H2O | 119 | ignore | 500 | An endpoint that receives a SETTINGS frame with any unknown or unsupported identifier MUST ignore that setting. |
| H2O | 124 | error | dropped | If a CONTINUATION frame is received with a Stream Identifier field of 0x00, the recipient MUST respond with a connection error (Section 5.4.1) of type PROTOCOL_ERROR. |
| H2O | 153 | error | dropped | A HEADERS frame without the END_HEADERS flag set MUST be followed by a CONTINUATION frame for the same stream. |
| H2O | 155 | ignore | 500 | Unsupported settings MUST be ignored. |
| H2O | 156 | error | dropped | The sender MUST NOT send a flow-controlled frame with a length that exceeds the space available in either of the flow-control windows advertised by the receiver. |
| Cloudflare | 18 | error | dropped | When set, the ACK flag indicates that this frame acknowledges receipt and application of the peer's SETTINGS frame. When this bit is set, the frame payload of the SETTINGS frame MUST be empty. |
| Cloudflare | 19 | error | dropped | A RST_STREAM frame with a length other than 4 octets MUST be treated as a connection error (Section 5.4.1) of type FRAME_SIZE_ERROR. |
| Cloudflare | 20 | error | dropped | The stream identifier for a SETTINGS frame MUST be zero (0x00). |
| Cloudflare | 21 | error | dropped | A SETTINGS frame with a length other than a multiple of 6 octets MUST be treated as a connection error (Section 5.4.1) of type FRAME_SIZE_ERROR. |
| Cloudflare | 22 | error | dropped | The initial value of SETTINGS_ENABLE_PUSH is 1. Any value other than 0 or 1 MUST be treated as a connection error (Section 5.4.1) of type PROTOCOL_ERROR. |
| Cloudflare | 23 | error | dropped | A server MUST NOT explicitly set this value (SETTINGS_ENABLE_PUSH) to 1. A server MAY choose to omit this setting (SETTINGS_ENABLE_PUSH) when it sends a SETTINGS frame, but if a server does include a value, it MUST be 0. |
| Cloudflare | 25 | error | dropped | For SETTINGS_INITIAL_WINDOW_SIZE, values above the maximum flow-control window size of 2^31-1 (2147483647) MUST be treated as a connection error (Section 5.4.1) of type FLOW_CONTROL_ERROR. |
| Cloudflare | 26 | error | dropped | The value advertised by an endpoint MUST be between initial value (2^14 = 16,384) and maximum allowed frame size (2^24-1 = 16,777,215 octets), inclusive. |
| Cloudflare | 30 | error | dropped | If a PING frame is received with a Stream Identifier field value other than 0x00, the recipient MUST respond with a connection error (Section 5.4.1) of type PROTOCOL_ERROR. |
| Cloudflare | 33 | error | dropped | A receiver MUST treat the receipt of a WINDOW_UPDATE frame with a flow-control window increment of 0 as a stream error (Section 5.4.2) of type PROTOCOL_ERROR. |
| Cloudflare | 34 | error | dropped | A sender MUST NOT allow a flow-control window to exceed 2^31-1 octets. If a sender receives a WINDOW_UPDATE that causes a flow-control window to exceed this maximum, it MUST terminate either the stream or the connection, as appropriate. |
| Cloudflare | 35 | error | dropped | An endpoint MUST treat a change to SETTINGS_INITIAL_WINDOW_SIZE that causes any flow-control window to exceed the maximum size as a connection error (Section 5.4.1) of type FLOW_CONTROL_ERROR. |
| Cloudflare | 37 | error | dropped | A CONTINUATION frame MUST be preceded by a HEADERS, PUSH_PROMISE or CONTINUATION frame without the END_HEADERS flag set. (Using HEADERS frame with END_HEADERS flag set) |
| Cloudflare | 39 | error | dropped | The header fields in PUSH_PROMISE and any subsequent CONTINUATION frames MUST be a valid and complete set of request header fields. |
| Cloudflare | 91 | error | dropped | A PUSH_PROMISE frame without the END_HEADERS flag set MUST be followed by a CONTINUATION frame for the same stream. |
| Cloudflare | 92 | error | dropped | PUSH_PROMISE MUST NOT be sent if the SETTINGS_ENABLE_PUSH setting of the peer endpoint is set to 0. |
| Cloudflare | 93 | error | dropped | The sender MUST NOT send a flow-controlled frame with a length that exceeds the space available in either of the flow-control windows advertised by the receiver. |
| Cloudflare | 94 | error | dropped | CONTINUATION frames MUST be associated with a stream. |
| Cloudflare | 117 | error | dropped | For SETTINGS_INITIAL_WINDOW_SIZE, values above the maximum flow-control window size of 2^31-1 (2147483647) MUST be treated as a connection error (Section 5.4.1) of type FLOW_CONTROL_ERROR. |
| Cloudflare | 119 | ignore | 500 | An endpoint that receives a SETTINGS frame with any unknown or unsupported identifier MUST ignore that setting. |
| Cloudflare | 122 | error | dropped | A sender MUST NOT allow a flow-control window to exceed 2^31-1 octets. If a sender receives a WINDOW_UPDATE that causes a flow-control window to exceed this maximum, it MUST terminate either the stream or the connection, as appropriate. |
| Cloudflare | 124 | error | dropped | If a CONTINUATION frame is received with a Stream Identifier field of 0x00, the recipient MUST respond with a connection error (Section 5.4.1) of type PROTOCOL_ERROR. |
| Mitmproxy | 18 | error | dropped | When set, the ACK flag indicates that this frame acknowledges receipt and application of the peer's SETTINGS frame. When this bit is set, the frame payload of the SETTINGS frame MUST be empty. |
| Mitmproxy | 19 | error | dropped | A RST_STREAM frame with a length other than 4 octets MUST be treated as a connection error (Section 5.4.1) of type FRAME_SIZE_ERROR. |
| Mitmproxy | 20 | error | received | The stream identifier for a SETTINGS frame MUST be zero (0x00). |
| Mitmproxy | 21 | error | received | A SETTINGS frame with a length other than a multiple of 6 octets MUST be treated as a connection error (Section 5.4.1) of type FRAME_SIZE_ERROR. |
| Mitmproxy | 22 | error | received | The initial value of SETTINGS_ENABLE_PUSH is 1. Any value other than 0 or 1 MUST be treated as a connection error (Section 5.4.1) of type PROTOCOL_ERROR. |
| Mitmproxy | 23 | error | received | A server MUST NOT explicitly set this value (SETTINGS_ENABLE_PUSH) to 1. A server MAY choose to omit this setting (SETTINGS_ENABLE_PUSH) when it sends a SETTINGS frame, but if a server does include a value, it MUST be 0. |
| Mitmproxy | 24 | error | received | A server MUST NOT send a PUSH_PROMISE frame if it receives the SETTINGS_ENABLE_PUSH (0x02) parameter set to a value of 0. |
| Mitmproxy | 25 | error | received | For SETTINGS_INITIAL_WINDOW_SIZE, values above the maximum flow-control window size of 2^31-1 (2147483647) MUST be treated as a connection error (Section 5.4.1) of type FLOW_CONTROL_ERROR. |
| Mitmproxy | 26 | error | received | The value advertised by an endpoint MUST be between initial value (2^14 = 16,384) and maximum allowed frame size (2^24-1 = 16,777,215 octets), inclusive. |
| Mitmproxy | 27 | ignore | received | An endpoint that receives a SETTINGS frame with any unknown or unsupported identifier MUST ignore that setting. |
| Mitmproxy | 28 | error | received | If the Stream Identifier field of a PUSH_PROMISE frame specifies the value 0x00, a recipient MUST respond with a connection error (Section 5.4.1) of type PROTOCOL_ERROR. |
| Mitmproxy | 30 | error | received | If a PING frame is received with a Stream Identifier field value other than 0x00, the recipient MUST respond with a connection error (Section 5.4.1) of type PROTOCOL_ERROR. |
| Mitmproxy | 33 | error | dropped | A receiver MUST treat the receipt of a WINDOW_UPDATE frame with a flow-control window increment of 0 as a stream error (Section 5.4.2) of type PROTOCOL_ERROR. |
| Mitmproxy | 34 | error | dropped | A sender MUST NOT allow a flow-control window to exceed 2^31-1 octets. If a sender receives a WINDOW_UPDATE that causes a flow-control window to exceed this maximum, it MUST terminate either the stream or the connection, as appropriate. |
| Mitmproxy | 35 | error | received | An endpoint MUST treat a change to SETTINGS_INITIAL_WINDOW_SIZE that causes any flow-control window to exceed the maximum size as a connection error (Section 5.4.1) of type FLOW_CONTROL_ERROR. |
| Mitmproxy | 36 | error | received | If a CONTINUATION frame is received with a Stream Identifier field of 0x00, the recipient MUST respond with a connection error (Section 5.4.1) of type PROTOCOL_ERROR. |
| Mitmproxy | 37 | error | received | A CONTINUATION frame MUST be preceded by a HEADERS, PUSH_PROMISE or CONTINUATION frame without the END_HEADERS flag set. (Using HEADERS frame with END_HEADERS flag set) |
| Mitmproxy | 38 | error | received | A CONTINUATION frame MUST be preceded by a HEADERS, PUSH_PROMISE or CONTINUATION frame without the END_HEADERS flag set. (Using PUSH_PROMISE frame with END_HEADERS flag set) |
| Mitmproxy | 39 | error | received | The header fields in PUSH_PROMISE and any subsequent CONTINUATION frames MUST be a valid and complete set of request header fields. |
| Mitmproxy | 85 | error | received | A HEADERS frame without the END_HEADERS flag set MUST be followed by a CONTINUATION frame for the same stream. |
| Mitmproxy | 88 | ignore | received | Unsupported settings MUST be ignored. |
| Mitmproxy | 91 | error | received | A PUSH_PROMISE frame without the END_HEADERS flag set MUST be followed by a CONTINUATION frame for the same stream. |
| Mitmproxy | 92 | error | received | PUSH_PROMISE MUST NOT be sent if the SETTINGS_ENABLE_PUSH setting of the peer endpoint is set to 0. |
| Mitmproxy | 93 | error | dropped | The sender MUST NOT send a flow-controlled frame with a length that exceeds the space available in either of the flow-control windows advertised by the receiver. |
| Mitmproxy | 94 | error | received | CONTINUATION frames MUST be associated with a stream. |
| Mitmproxy | 95 | error | received | If the END_HEADERS flag is not set, this frame MUST be followed by another CONTINUATION frame. A receiver MUST treat the receipt of any other type of frame or a frame on a different stream as a connection error (Section 5.4.1) of type PROTOCOL_ERROR. |
| Mitmproxy | 96 | error | received | Other frames (from any stream) MUST NOT occur between the HEADERS frame and any CONTINUATION frames that might follow. |
| Mitmproxy | 111 | error | received | If a PRIORITY frame is received with a stream identifier of 0x00, the recipient MUST respond with a connection error of type PROTOCOL_ERROR. (server side) |
| Mitmproxy | 113 | error | dropped | When set, the ACK flag indicates that this frame acknowledges receipt and application of the peer's SETTINGS frame. When this bit is set, the frame payload of the SETTINGS frame MUST be empty. (server side) |
| Mitmproxy | 114 | error | dropped | A RST_STREAM frame with a length other than 4 octets MUST be treated as a connection error (Section 5.4.1) of type FRAME_SIZE_ERROR. (server side) |
| Mitmproxy | 115 | error | received | The stream identifier for a SETTINGS frame MUST be zero (0x00). |
| Mitmproxy | 116 | error | received | A SETTINGS frame with a length other than a multiple of 6 octets MUST be treated as a connection error (Section 5.4.1) of type FRAME_SIZE_ERROR. |
| Mitmproxy | 117 | error | dropped | For SETTINGS_INITIAL_WINDOW_SIZE, values above the maximum flow-control window size of 2^31-1 (2147483647) MUST be treated as a connection error (Section 5.4.1) of type FLOW_CONTROL_ERROR. |
| Mitmproxy | 118 | error | received | The value advertised by an endpoint MUST be between initial value (2^14 = 16,384) and maximum allowed frame size (2^24-1 = 16,777,215 octets), inclusive. |
| Mitmproxy | 119 | ignore | received | An endpoint that receives a SETTINGS frame with any unknown or unsupported identifier MUST ignore that setting. |
| Mitmproxy | 120 | error | received | If a PING frame is received with a Stream Identifier field value other than 0x00, the recipient MUST respond with a connection error (Section 5.4.1) of type PROTOCOL_ERROR. |
| Mitmproxy | 121 | error | dropped | A receiver MUST treat the receipt of a WINDOW_UPDATE frame with a flow-control window increment of 0 as a stream error (Section 5.4.2) of type PROTOCOL_ERROR. |
| Mitmproxy | 122 | error | dropped | A sender MUST NOT allow a flow-control window to exceed 2^31-1 octets. If a sender receives a WINDOW_UPDATE that causes a flow-control window to exceed this maximum, it MUST terminate either the stream or the connection, as appropriate. |
| Mitmproxy | 123 | error | dropped | An endpoint MUST treat a change to SETTINGS_INITIAL_WINDOW_SIZE that causes any flow-control window to exceed the maximum size as a connection error (Section 5.4.1) of type FLOW_CONTROL_ERROR. |
| Mitmproxy | 124 | error | received | If a CONTINUATION frame is received with a Stream Identifier field of 0x00, the recipient MUST respond with a connection error (Section 5.4.1) of type PROTOCOL_ERROR. |
| Mitmproxy | 125 | error | received | A CONTINUATION frame MUST be preceded by a HEADERS, PUSH_PROMISE or CONTINUATION frame without the END_HEADERS flag set. (Using HEADERS frame with END_HEADERS flag set) |
| Mitmproxy | 153 | error | received | A HEADERS frame without the END_HEADERS flag set MUST be followed by a CONTINUATION frame for the same stream. |
| Mitmproxy | 154 | error | received | If a HEADERS frame is received whose Stream Identifier field is 0x00, the recipient MUST respond with a connection error (Section 5.4.1) of type PROTOCOL_ERROR. |
| Mitmproxy | 155 | ignore | received | Unsupported settings MUST be ignored. |
| Mitmproxy | 156 | error | dropped | The sender MUST NOT send a flow-controlled frame with a length that exceeds the space available in either of the flow-control windows advertised by the receiver. |
| Mitmproxy | 157 | error | received | CONTINUATION frames MUST be associated with a stream. |
| Mitmproxy | 158 | error | received | If the END_HEADERS flag is not set, this frame MUST be followed by another CONTINUATION frame. A receiver MUST treat the receipt of any other type of frame or a frame on a different stream as a connection error (Section 5.4.1) of type PROTOCOL_ERROR. |
| Mitmproxy | 159 | error | received | Other frames (from any stream) MUST NOT occur between the HEADERS frame and any CONTINUATION frames that might follow. |
| Azure-AG | 20 | error | dropped | The stream identifier for a SETTINGS frame MUST be zero (0x00). |
| Azure-AG | 30 | error | dropped | If a PING frame is received with a Stream Identifier field value other than 0x00, the recipient MUST respond with a connection error (Section 5.4.1) of type PROTOCOL_ERROR. |
| Azure-AG | 33 | error | dropped | A receiver MUST treat the receipt of a WINDOW_UPDATE frame with a flow-control window increment of 0 as a stream error (Section 5.4.2) of type PROTOCOL_ERROR. |
| Azure-AG | 93 | error | dropped | The sender MUST NOT send a flow-controlled frame with a length that exceeds the space available in either of the flow-control windows advertised by the receiver. |
| Nginx | 93 | error | dropped | The sender MUST NOT send a flow-controlled frame with a length that exceeds the space available in either of the flow-control windows advertised by the receiver. |
| Lighttpd | 93 | error | dropped | The sender MUST NOT send a flow-controlled frame with a length that exceeds the space available in either of the flow-control windows advertised by the receiver. |

## Section 8: HTTP Semantics in HTTP/2

| Proxy | Conformant | Non-Conformant | Total Tests |
|-------|------------|----------------|-------------|
| Nghttpx | 29 (42.0%) | 40 (58.0%) | 69 |
| HAproxy | 38 (55.1%) | 31 (44.9%) | 69 |
| Apache | 35 (50.7%) | 34 (49.3%) | 69 |
| Caddy | 23 (33.3%) | 46 (66.7%) | 69 |
| Node | 14 (20.3%) | 55 (79.7%) | 69 |
| Envoy | 31 (44.9%) | 38 (55.1%) | 69 |
| H2O | 20 (29.0%) | 49 (71.0%) | 69 |
| Cloudflare | 23 (32.9%) | 47 (67.1%) | 70 |
| Mitmproxy | 0 (0.0%) | 70 (100.0%) | 70 |
| Azure-AG | 4 (10.5%) | 34 (89.5%) | 38 |
| Nginx | 4 (10.5%) | 34 (89.5%) | 38 |
| Lighttpd | 1 (2.6%) | 37 (97.4%) | 38 |

### Non-Conformant Tests

| Proxy | Test ID | Expected | Actual | Description |
|-------|---------|-----------|--------|-------------|
| Nghttpx | 31 | error | dropped | With the CONNECT method, the " :scheme" and " :path" pseudo-header fields MUST be omitted. (Tested with only :path present) |
| Nghttpx | 32 | error | dropped | With the CONNECT method, the " :scheme" and " :path" pseudo-header fields MUST be omitted. (Tested with only :scheme present) |
| Nghttpx | 40 | error | dropped | Trailers MUST NOT include pseudo-header fields (Section 8.3). |
| Nghttpx | 41 | error | dropped | Field names MUST be converted to lowercase when constructing an HTTP/2 message. |
| Nghttpx | 42 | error | dropped | Field names MUST NOT contain control characters (0x00-0x1F) |
| Nghttpx | 43 | error | dropped | Field names MUST NOT contain ASCII SP (0x20) |
| Nghttpx | 44 | error | dropped | Field names MUST NOT contain DEL character (0x7F) |
| Nghttpx | 45 | error | dropped | Field names MUST NOT contain high byte characters (0x80-0xFF) |
| Nghttpx | 46 | error | dropped | With the exception of pseudo-header fields (Section 8.3), which have a name that starts with a single colon, field names MUST NOT include a colon (ASCII COLON, 0x3a). |
| Nghttpx | 47 | error | dropped | A field value MUST NOT contain line feed (ASCII LF, 0x0a). (Tested at the start of the value) |
| Nghttpx | 48 | error | dropped | A field value MUST NOT contain carriage return (ASCII CR, 0x0d). (Tested at the start of the value) |
| Nghttpx | 49 | error | dropped | A field value MUST NOT start with an ASCII whitespace character (ASCII SP or HTAB, 0x20 or 0x09). |
| Nghttpx | 50 | error | dropped | A field value MUST NOT end with an ASCII whitespace character (ASCII SP or HTAB, 0x20 or 0x09). |
| Nghttpx | 51 | error | dropped | An endpoint MUST NOT generate an HTTP/2 message containing connection header field (RFC9113 Section 8.2.2) |
| Nghttpx | 52 | error | dropped | An endpoint MUST NOT generate an HTTP/2 message containing proxy-connection header field (RFC9113 Section 8.2.2) |
| Nghttpx | 53 | error | dropped | An endpoint MUST NOT generate an HTTP/2 message containing keep-alive header field (RFC9113 Section 8.2.2) |
| Nghttpx | 54 | error | dropped | An endpoint MUST NOT generate an HTTP/2 message containing transfer-encoding header field (RFC9113 Section 8.2.2) |
| Nghttpx | 55 | error | dropped | An endpoint MUST NOT generate an HTTP/2 message containing upgrade header field (RFC9113 Section 8.2.2) |
| Nghttpx | 56 | error | dropped | The TE header field MAY be present in an HTTP/2 request; when it is, it MUST NOT contain any value other than 'trailers'. |
| Nghttpx | 57 | error | dropped | Pseudo-header fields are not HTTP header fields. Endpoints MUST NOT generate pseudo-header fields other than those defined in this document. |
| Nghttpx | 59 | error | dropped | Pseudo-header fields defined for responses MUST NOT appear in requests. |
| Nghttpx | 60 | error | dropped | All pseudo-header fields sent from a client MUST appear in a field block before all regular field lines. Any request or response that contains a pseudo-header field that appears in a field block after a regular field line MUST be treated as malformed (Section 8.1.1). |
| Nghttpx | 62 | error | dropped | The same pseudo-header field name MUST NOT appear more than once in a field block. A field block for an HTTP request or response that contains a repeated pseudo-header field name MUST be treated as malformed (Section 8.1.1). Tested with a request frame with the same value. |
| Nghttpx | 63 | error | dropped | The same pseudo-header field name MUST NOT appear more than once in a field block. A field block for an HTTP request or response that contains a repeated pseudo-header field name MUST be treated as malformed (Section 8.1.1). Tested with a request frame with different values. |
| Nghttpx | 66 | error | dropped | Clients MUST NOT generate a request with a Host header field that differs from the ":authority" pseudo-header field. |
| Nghttpx | 67 | error | dropped | ':authority' MUST NOT include the deprecated userinfo subcomponent for "http" or "https" schemed URIs. |
| Nghttpx | 68 | error | dropped | The ":path" pseudo-header field MUST NOT be empty for "http" or "https" URIs; "http" or "https" URIs that do not contain a path component MUST include a value of '/'. |
| Nghttpx | 69 | error | dropped | All HTTP/2 requests MUST include exactly one valid value for the ":method", ":scheme", and ":path" pseudo-header fields, unless they are CONNECT requests (Section 8.5). An HTTP request that omits mandatory pseudo-header fields is malformed (Section 8.1.1). (Tested with :method missing) |
| Nghttpx | 70 | error | dropped | All HTTP/2 requests MUST include exactly one valid value for the ":method", ":scheme", and ":path" pseudo-header fields, unless they are CONNECT requests (Section 8.5). An HTTP request that omits mandatory pseudo-header fields is malformed (Section 8.1.1). (Tested with :scheme missing) |
| Nghttpx | 74 | error | dropped | With the CONNECT method, the ":scheme" and ":path" pseudo-header fields MUST be omitted. (Tested with both present) |
| Nghttpx | 97 | error | dropped | An endpoint that receives a HEADERS frame without the END_STREAM flag set after receiving the HEADERS frame that opens a request or after receiving a final (non-informational) status code MUST treat the corresponding request or response as malformed (Section 8.1.1). |
| Nghttpx | 98 | error | dropped | A field value MUST NOT contain line feed (ASCII LF, 0x0a). (Tested at the middle of the value) |
| Nghttpx | 99 | error | dropped | A field value MUST NOT contain line feed (ASCII LF, 0x0a). (Tested at the end of the value) |
| Nghttpx | 100 | error | dropped | A field value MUST NOT contain carriage return (ASCII CR, 0x0d). (Tested at the middle of the value) |
| Nghttpx | 101 | error | dropped | A field value MUST NOT contain carriage return (ASCII CR, 0x0d). (Tested at the end of the value) |
| Nghttpx | 102 | error | dropped | Pseudo-header fields MUST NOT appear in a trailer section. |
| Nghttpx | 103 | error | dropped | All HTTP/2 requests MUST include exactly one valid value for the ":method", ":scheme", and ":path" pseudo-header fields, unless they are CONNECT requests (Section 8.5). An HTTP request that omits mandatory pseudo-header fields is malformed (Section 8.1.1). (Tested with :path missing) |
| Nghttpx | 126 | error | dropped | Trailers MUST NOT include pseudo-header fields (Section 8.3). |
| Nghttpx | 160 | error | dropped | An endpoint that receives a HEADERS frame without the END_STREAM flag set after receiving the HEADERS frame that opens a request or after receiving a final (non-informational) status code MUST treat the corresponding request or response as malformed (Section 8.1.1). |
| Nghttpx | 165 | error | dropped | Pseudo-header fields MUST NOT appear in a trailer section. |
| HAproxy | 31 | error | dropped | With the CONNECT method, the " :scheme" and " :path" pseudo-header fields MUST be omitted. (Tested with only :path present) |
| HAproxy | 32 | error | dropped | With the CONNECT method, the " :scheme" and " :path" pseudo-header fields MUST be omitted. (Tested with only :scheme present) |
| HAproxy | 40 | error | dropped | Trailers MUST NOT include pseudo-header fields (Section 8.3). |
| HAproxy | 41 | error | dropped | Field names MUST be converted to lowercase when constructing an HTTP/2 message. |
| HAproxy | 43 | error | dropped | Field names MUST NOT contain ASCII SP (0x20) |
| HAproxy | 44 | error | dropped | Field names MUST NOT contain DEL character (0x7F) |
| HAproxy | 45 | error | dropped | Field names MUST NOT contain high byte characters (0x80-0xFF) |
| HAproxy | 46 | error | dropped | With the exception of pseudo-header fields (Section 8.3), which have a name that starts with a single colon, field names MUST NOT include a colon (ASCII COLON, 0x3a). |
| HAproxy | 51 | error | dropped | An endpoint MUST NOT generate an HTTP/2 message containing connection header field (RFC9113 Section 8.2.2) |
| HAproxy | 52 | error | dropped | An endpoint MUST NOT generate an HTTP/2 message containing proxy-connection header field (RFC9113 Section 8.2.2) |
| HAproxy | 53 | error | dropped | An endpoint MUST NOT generate an HTTP/2 message containing keep-alive header field (RFC9113 Section 8.2.2) |
| HAproxy | 54 | error | dropped | An endpoint MUST NOT generate an HTTP/2 message containing transfer-encoding header field (RFC9113 Section 8.2.2) |
| HAproxy | 55 | error | dropped | An endpoint MUST NOT generate an HTTP/2 message containing upgrade header field (RFC9113 Section 8.2.2) |
| HAproxy | 56 | error | dropped | The TE header field MAY be present in an HTTP/2 request; when it is, it MUST NOT contain any value other than 'trailers'. |
| HAproxy | 57 | error | dropped | Pseudo-header fields are not HTTP header fields. Endpoints MUST NOT generate pseudo-header fields other than those defined in this document. |
| HAproxy | 59 | error | dropped | Pseudo-header fields defined for responses MUST NOT appear in requests. |
| HAproxy | 60 | error | dropped | All pseudo-header fields sent from a client MUST appear in a field block before all regular field lines. Any request or response that contains a pseudo-header field that appears in a field block after a regular field line MUST be treated as malformed (Section 8.1.1). |
| HAproxy | 62 | error | dropped | The same pseudo-header field name MUST NOT appear more than once in a field block. A field block for an HTTP request or response that contains a repeated pseudo-header field name MUST be treated as malformed (Section 8.1.1). Tested with a request frame with the same value. |
| HAproxy | 63 | error | dropped | The same pseudo-header field name MUST NOT appear more than once in a field block. A field block for an HTTP request or response that contains a repeated pseudo-header field name MUST be treated as malformed (Section 8.1.1). Tested with a request frame with different values. |
| HAproxy | 68 | error | dropped | The ":path" pseudo-header field MUST NOT be empty for "http" or "https" URIs; "http" or "https" URIs that do not contain a path component MUST include a value of '/'. |
| HAproxy | 69 | error | dropped | All HTTP/2 requests MUST include exactly one valid value for the ":method", ":scheme", and ":path" pseudo-header fields, unless they are CONNECT requests (Section 8.5). An HTTP request that omits mandatory pseudo-header fields is malformed (Section 8.1.1). (Tested with :method missing) |
| HAproxy | 70 | error | dropped | All HTTP/2 requests MUST include exactly one valid value for the ":method", ":scheme", and ":path" pseudo-header fields, unless they are CONNECT requests (Section 8.5). An HTTP request that omits mandatory pseudo-header fields is malformed (Section 8.1.1). (Tested with :scheme missing) |
| HAproxy | 74 | error | dropped | With the CONNECT method, the ":scheme" and ":path" pseudo-header fields MUST be omitted. (Tested with both present) |
| HAproxy | 75 | ignore | 500 | With the CONNECT method, The ":authority" pseudo-header field contains the host and port to connect to |
| HAproxy | 102 | error | dropped | Pseudo-header fields MUST NOT appear in a trailer section. |
| HAproxy | 103 | error | dropped | All HTTP/2 requests MUST include exactly one valid value for the ":method", ":scheme", and ":path" pseudo-header fields, unless they are CONNECT requests (Section 8.5). An HTTP request that omits mandatory pseudo-header fields is malformed (Section 8.1.1). (Tested with :path missing) |
| HAproxy | 126 | error | received | Trailers MUST NOT include pseudo-header fields (Section 8.3). |
| HAproxy | 135 | error | received | A field value MUST NOT start with an ASCII whitespace character (ASCII SP or HTAB, 0x20 or 0x09). |
| HAproxy | 136 | error | received | A field value MUST NOT end with an ASCII whitespace character (ASCII SP or HTAB, 0x20 or 0x09). |
| HAproxy | 142 | error | received | The TE header field MAY be present in an HTTP/2 request; when it is, it MUST NOT contain any value other than 'trailers'. |
| HAproxy | 165 | error | received | Pseudo-header fields MUST NOT appear in a trailer section. |
| Apache | 31 | error | dropped | With the CONNECT method, the " :scheme" and " :path" pseudo-header fields MUST be omitted. (Tested with only :path present) |
| Apache | 32 | error | dropped | With the CONNECT method, the " :scheme" and " :path" pseudo-header fields MUST be omitted. (Tested with only :scheme present) |
| Apache | 40 | error | dropped | Trailers MUST NOT include pseudo-header fields (Section 8.3). |
| Apache | 41 | error | dropped | Field names MUST be converted to lowercase when constructing an HTTP/2 message. |
| Apache | 42 | error | dropped | Field names MUST NOT contain control characters (0x00-0x1F) |
| Apache | 43 | error | dropped | Field names MUST NOT contain ASCII SP (0x20) |
| Apache | 44 | error | dropped | Field names MUST NOT contain DEL character (0x7F) |
| Apache | 45 | error | dropped | Field names MUST NOT contain high byte characters (0x80-0xFF) |
| Apache | 46 | error | dropped | With the exception of pseudo-header fields (Section 8.3), which have a name that starts with a single colon, field names MUST NOT include a colon (ASCII COLON, 0x3a). |
| Apache | 47 | error | dropped | A field value MUST NOT contain line feed (ASCII LF, 0x0a). (Tested at the start of the value) |
| Apache | 48 | error | dropped | A field value MUST NOT contain carriage return (ASCII CR, 0x0d). (Tested at the start of the value) |
| Apache | 51 | error | dropped | An endpoint MUST NOT generate an HTTP/2 message containing connection header field (RFC9113 Section 8.2.2) |
| Apache | 52 | error | dropped | An endpoint MUST NOT generate an HTTP/2 message containing proxy-connection header field (RFC9113 Section 8.2.2) |
| Apache | 53 | error | dropped | An endpoint MUST NOT generate an HTTP/2 message containing keep-alive header field (RFC9113 Section 8.2.2) |
| Apache | 54 | error | dropped | An endpoint MUST NOT generate an HTTP/2 message containing transfer-encoding header field (RFC9113 Section 8.2.2) |
| Apache | 55 | error | dropped | An endpoint MUST NOT generate an HTTP/2 message containing upgrade header field (RFC9113 Section 8.2.2) |
| Apache | 56 | error | dropped | The TE header field MAY be present in an HTTP/2 request; when it is, it MUST NOT contain any value other than 'trailers'. |
| Apache | 57 | error | dropped | Pseudo-header fields are not HTTP header fields. Endpoints MUST NOT generate pseudo-header fields other than those defined in this document. |
| Apache | 59 | error | dropped | Pseudo-header fields defined for responses MUST NOT appear in requests. |
| Apache | 60 | error | dropped | All pseudo-header fields sent from a client MUST appear in a field block before all regular field lines. Any request or response that contains a pseudo-header field that appears in a field block after a regular field line MUST be treated as malformed (Section 8.1.1). |
| Apache | 62 | error | dropped | The same pseudo-header field name MUST NOT appear more than once in a field block. A field block for an HTTP request or response that contains a repeated pseudo-header field name MUST be treated as malformed (Section 8.1.1). Tested with a request frame with the same value. |
| Apache | 63 | error | dropped | The same pseudo-header field name MUST NOT appear more than once in a field block. A field block for an HTTP request or response that contains a repeated pseudo-header field name MUST be treated as malformed (Section 8.1.1). Tested with a request frame with different values. |
| Apache | 67 | error | dropped | ':authority' MUST NOT include the deprecated userinfo subcomponent for "http" or "https" schemed URIs. |
| Apache | 68 | error | dropped | The ":path" pseudo-header field MUST NOT be empty for "http" or "https" URIs; "http" or "https" URIs that do not contain a path component MUST include a value of '/'. |
| Apache | 69 | error | dropped | All HTTP/2 requests MUST include exactly one valid value for the ":method", ":scheme", and ":path" pseudo-header fields, unless they are CONNECT requests (Section 8.5). An HTTP request that omits mandatory pseudo-header fields is malformed (Section 8.1.1). (Tested with :method missing) |
| Apache | 70 | error | dropped | All HTTP/2 requests MUST include exactly one valid value for the ":method", ":scheme", and ":path" pseudo-header fields, unless they are CONNECT requests (Section 8.5). An HTTP request that omits mandatory pseudo-header fields is malformed (Section 8.1.1). (Tested with :scheme missing) |
| Apache | 74 | error | dropped | With the CONNECT method, the ":scheme" and ":path" pseudo-header fields MUST be omitted. (Tested with both present) |
| Apache | 97 | error | dropped | An endpoint that receives a HEADERS frame without the END_STREAM flag set after receiving the HEADERS frame that opens a request or after receiving a final (non-informational) status code MUST treat the corresponding request or response as malformed (Section 8.1.1). |
| Apache | 98 | error | dropped | A field value MUST NOT contain line feed (ASCII LF, 0x0a). (Tested at the middle of the value) |
| Apache | 99 | error | dropped | A field value MUST NOT contain line feed (ASCII LF, 0x0a). (Tested at the end of the value) |
| Apache | 100 | error | dropped | A field value MUST NOT contain carriage return (ASCII CR, 0x0d). (Tested at the middle of the value) |
| Apache | 101 | error | dropped | A field value MUST NOT contain carriage return (ASCII CR, 0x0d). (Tested at the end of the value) |
| Apache | 102 | error | dropped | Pseudo-header fields MUST NOT appear in a trailer section. |
| Apache | 103 | error | dropped | All HTTP/2 requests MUST include exactly one valid value for the ":method", ":scheme", and ":path" pseudo-header fields, unless they are CONNECT requests (Section 8.5). An HTTP request that omits mandatory pseudo-header fields is malformed (Section 8.1.1). (Tested with :path missing) |
| Caddy | 31 | error | dropped | With the CONNECT method, the " :scheme" and " :path" pseudo-header fields MUST be omitted. (Tested with only :path present) |
| Caddy | 32 | error | dropped | With the CONNECT method, the " :scheme" and " :path" pseudo-header fields MUST be omitted. (Tested with only :scheme present) |
| Caddy | 40 | error | dropped | Trailers MUST NOT include pseudo-header fields (Section 8.3). |
| Caddy | 41 | error | dropped | Field names MUST be converted to lowercase when constructing an HTTP/2 message. |
| Caddy | 42 | error | dropped | Field names MUST NOT contain control characters (0x00-0x1F) |
| Caddy | 43 | error | dropped | Field names MUST NOT contain ASCII SP (0x20) |
| Caddy | 44 | error | dropped | Field names MUST NOT contain DEL character (0x7F) |
| Caddy | 45 | error | dropped | Field names MUST NOT contain high byte characters (0x80-0xFF) |
| Caddy | 46 | error | dropped | With the exception of pseudo-header fields (Section 8.3), which have a name that starts with a single colon, field names MUST NOT include a colon (ASCII COLON, 0x3a). |
| Caddy | 47 | error | dropped | A field value MUST NOT contain line feed (ASCII LF, 0x0a). (Tested at the start of the value) |
| Caddy | 48 | error | dropped | A field value MUST NOT contain carriage return (ASCII CR, 0x0d). (Tested at the start of the value) |
| Caddy | 51 | error | dropped | An endpoint MUST NOT generate an HTTP/2 message containing connection header field (RFC9113 Section 8.2.2) |
| Caddy | 52 | error | dropped | An endpoint MUST NOT generate an HTTP/2 message containing proxy-connection header field (RFC9113 Section 8.2.2) |
| Caddy | 53 | error | dropped | An endpoint MUST NOT generate an HTTP/2 message containing keep-alive header field (RFC9113 Section 8.2.2) |
| Caddy | 54 | error | dropped | An endpoint MUST NOT generate an HTTP/2 message containing transfer-encoding header field (RFC9113 Section 8.2.2) |
| Caddy | 55 | error | dropped | An endpoint MUST NOT generate an HTTP/2 message containing upgrade header field (RFC9113 Section 8.2.2) |
| Caddy | 56 | error | dropped | The TE header field MAY be present in an HTTP/2 request; when it is, it MUST NOT contain any value other than 'trailers'. |
| Caddy | 57 | error | dropped | Pseudo-header fields are not HTTP header fields. Endpoints MUST NOT generate pseudo-header fields other than those defined in this document. |
| Caddy | 59 | error | dropped | Pseudo-header fields defined for responses MUST NOT appear in requests. |
| Caddy | 60 | error | dropped | All pseudo-header fields sent from a client MUST appear in a field block before all regular field lines. Any request or response that contains a pseudo-header field that appears in a field block after a regular field line MUST be treated as malformed (Section 8.1.1). |
| Caddy | 62 | error | dropped | The same pseudo-header field name MUST NOT appear more than once in a field block. A field block for an HTTP request or response that contains a repeated pseudo-header field name MUST be treated as malformed (Section 8.1.1). Tested with a request frame with the same value. |
| Caddy | 63 | error | dropped | The same pseudo-header field name MUST NOT appear more than once in a field block. A field block for an HTTP request or response that contains a repeated pseudo-header field name MUST be treated as malformed (Section 8.1.1). Tested with a request frame with different values. |
| Caddy | 67 | error | dropped | ':authority' MUST NOT include the deprecated userinfo subcomponent for "http" or "https" schemed URIs. |
| Caddy | 68 | error | dropped | The ":path" pseudo-header field MUST NOT be empty for "http" or "https" URIs; "http" or "https" URIs that do not contain a path component MUST include a value of '/'. |
| Caddy | 69 | error | dropped | All HTTP/2 requests MUST include exactly one valid value for the ":method", ":scheme", and ":path" pseudo-header fields, unless they are CONNECT requests (Section 8.5). An HTTP request that omits mandatory pseudo-header fields is malformed (Section 8.1.1). (Tested with :method missing) |
| Caddy | 70 | error | dropped | All HTTP/2 requests MUST include exactly one valid value for the ":method", ":scheme", and ":path" pseudo-header fields, unless they are CONNECT requests (Section 8.5). An HTTP request that omits mandatory pseudo-header fields is malformed (Section 8.1.1). (Tested with :scheme missing) |
| Caddy | 74 | error | dropped | With the CONNECT method, the ":scheme" and ":path" pseudo-header fields MUST be omitted. (Tested with both present) |
| Caddy | 75 | ignore | 500 | With the CONNECT method, The ":authority" pseudo-header field contains the host and port to connect to |
| Caddy | 97 | error | dropped | An endpoint that receives a HEADERS frame without the END_STREAM flag set after receiving the HEADERS frame that opens a request or after receiving a final (non-informational) status code MUST treat the corresponding request or response as malformed (Section 8.1.1). |
| Caddy | 98 | error | dropped | A field value MUST NOT contain line feed (ASCII LF, 0x0a). (Tested at the middle of the value) |
| Caddy | 99 | error | dropped | A field value MUST NOT contain line feed (ASCII LF, 0x0a). (Tested at the end of the value) |
| Caddy | 100 | error | dropped | A field value MUST NOT contain carriage return (ASCII CR, 0x0d). (Tested at the middle of the value) |
| Caddy | 101 | error | dropped | A field value MUST NOT contain carriage return (ASCII CR, 0x0d). (Tested at the end of the value) |
| Caddy | 102 | error | dropped | Pseudo-header fields MUST NOT appear in a trailer section. |
| Caddy | 103 | error | dropped | All HTTP/2 requests MUST include exactly one valid value for the ":method", ":scheme", and ":path" pseudo-header fields, unless they are CONNECT requests (Section 8.5). An HTTP request that omits mandatory pseudo-header fields is malformed (Section 8.1.1). (Tested with :path missing) |
| Caddy | 126 | error | dropped | Trailers MUST NOT include pseudo-header fields (Section 8.3). |
| Caddy | 135 | error | received | A field value MUST NOT start with an ASCII whitespace character (ASCII SP or HTAB, 0x20 or 0x09). |
| Caddy | 136 | error | received | A field value MUST NOT end with an ASCII whitespace character (ASCII SP or HTAB, 0x20 or 0x09). |
| Caddy | 137 | error | received | An endpoint MUST NOT generate an HTTP/2 message containing connection header field (RFC9113 Section 8.2.2) |
| Caddy | 138 | error | received | An endpoint MUST NOT generate an HTTP/2 message containing proxy-connection header field (RFC9113 Section 8.2.2) |
| Caddy | 139 | error | received | An endpoint MUST NOT generate an HTTP/2 message containing keep-alive header field (RFC9113 Section 8.2.2) |
| Caddy | 140 | error | received | An endpoint MUST NOT generate an HTTP/2 message containing transfer-encoding header field (RFC9113 Section 8.2.2) |
| Caddy | 141 | error | received | An endpoint MUST NOT generate an HTTP/2 message containing upgrade header field (RFC9113 Section 8.2.2) |
| Caddy | 142 | error | received | The TE header field MAY be present in an HTTP/2 request; when it is, it MUST NOT contain any value other than 'trailers'. |
| Caddy | 160 | error | dropped | An endpoint that receives a HEADERS frame without the END_STREAM flag set after receiving the HEADERS frame that opens a request or after receiving a final (non-informational) status code MUST treat the corresponding request or response as malformed (Section 8.1.1). |
| Caddy | 165 | error | dropped | Pseudo-header fields MUST NOT appear in a trailer section. |
| Node | 31 | error | dropped | With the CONNECT method, the " :scheme" and " :path" pseudo-header fields MUST be omitted. (Tested with only :path present) |
| Node | 32 | error | dropped | With the CONNECT method, the " :scheme" and " :path" pseudo-header fields MUST be omitted. (Tested with only :scheme present) |
| Node | 40 | error | dropped | Trailers MUST NOT include pseudo-header fields (Section 8.3). |
| Node | 41 | error | dropped | Field names MUST be converted to lowercase when constructing an HTTP/2 message. |
| Node | 42 | error | dropped | Field names MUST NOT contain control characters (0x00-0x1F) |
| Node | 43 | error | dropped | Field names MUST NOT contain ASCII SP (0x20) |
| Node | 44 | error | dropped | Field names MUST NOT contain DEL character (0x7F) |
| Node | 45 | error | dropped | Field names MUST NOT contain high byte characters (0x80-0xFF) |
| Node | 46 | error | dropped | With the exception of pseudo-header fields (Section 8.3), which have a name that starts with a single colon, field names MUST NOT include a colon (ASCII COLON, 0x3a). |
| Node | 47 | error | dropped | A field value MUST NOT contain line feed (ASCII LF, 0x0a). (Tested at the start of the value) |
| Node | 48 | error | dropped | A field value MUST NOT contain carriage return (ASCII CR, 0x0d). (Tested at the start of the value) |
| Node | 49 | error | dropped | A field value MUST NOT start with an ASCII whitespace character (ASCII SP or HTAB, 0x20 or 0x09). |
| Node | 50 | error | dropped | A field value MUST NOT end with an ASCII whitespace character (ASCII SP or HTAB, 0x20 or 0x09). |
| Node | 51 | error | dropped | An endpoint MUST NOT generate an HTTP/2 message containing connection header field (RFC9113 Section 8.2.2) |
| Node | 52 | error | dropped | An endpoint MUST NOT generate an HTTP/2 message containing proxy-connection header field (RFC9113 Section 8.2.2) |
| Node | 53 | error | dropped | An endpoint MUST NOT generate an HTTP/2 message containing keep-alive header field (RFC9113 Section 8.2.2) |
| Node | 54 | error | dropped | An endpoint MUST NOT generate an HTTP/2 message containing transfer-encoding header field (RFC9113 Section 8.2.2) |
| Node | 55 | error | dropped | An endpoint MUST NOT generate an HTTP/2 message containing upgrade header field (RFC9113 Section 8.2.2) |
| Node | 56 | error | dropped | The TE header field MAY be present in an HTTP/2 request; when it is, it MUST NOT contain any value other than 'trailers'. |
| Node | 57 | error | dropped | Pseudo-header fields are not HTTP header fields. Endpoints MUST NOT generate pseudo-header fields other than those defined in this document. |
| Node | 59 | error | dropped | Pseudo-header fields defined for responses MUST NOT appear in requests. |
| Node | 60 | error | dropped | All pseudo-header fields sent from a client MUST appear in a field block before all regular field lines. Any request or response that contains a pseudo-header field that appears in a field block after a regular field line MUST be treated as malformed (Section 8.1.1). |
| Node | 62 | error | dropped | The same pseudo-header field name MUST NOT appear more than once in a field block. A field block for an HTTP request or response that contains a repeated pseudo-header field name MUST be treated as malformed (Section 8.1.1). Tested with a request frame with the same value. |
| Node | 63 | error | dropped | The same pseudo-header field name MUST NOT appear more than once in a field block. A field block for an HTTP request or response that contains a repeated pseudo-header field name MUST be treated as malformed (Section 8.1.1). Tested with a request frame with different values. |
| Node | 66 | error | dropped | Clients MUST NOT generate a request with a Host header field that differs from the ":authority" pseudo-header field. |
| Node | 67 | error | dropped | ':authority' MUST NOT include the deprecated userinfo subcomponent for "http" or "https" schemed URIs. |
| Node | 68 | error | dropped | The ":path" pseudo-header field MUST NOT be empty for "http" or "https" URIs; "http" or "https" URIs that do not contain a path component MUST include a value of '/'. |
| Node | 69 | error | dropped | All HTTP/2 requests MUST include exactly one valid value for the ":method", ":scheme", and ":path" pseudo-header fields, unless they are CONNECT requests (Section 8.5). An HTTP request that omits mandatory pseudo-header fields is malformed (Section 8.1.1). (Tested with :method missing) |
| Node | 70 | error | dropped | All HTTP/2 requests MUST include exactly one valid value for the ":method", ":scheme", and ":path" pseudo-header fields, unless they are CONNECT requests (Section 8.5). An HTTP request that omits mandatory pseudo-header fields is malformed (Section 8.1.1). (Tested with :scheme missing) |
| Node | 73 | error | dropped | In the PUSH_PROMISE frame, the server MUST include a method in the ":method" pseudo-header field that is safe and cacheable. |
| Node | 74 | error | dropped | With the CONNECT method, the ":scheme" and ":path" pseudo-header fields MUST be omitted. (Tested with both present) |
| Node | 97 | error | dropped | An endpoint that receives a HEADERS frame without the END_STREAM flag set after receiving the HEADERS frame that opens a request or after receiving a final (non-informational) status code MUST treat the corresponding request or response as malformed (Section 8.1.1). |
| Node | 98 | error | dropped | A field value MUST NOT contain line feed (ASCII LF, 0x0a). (Tested at the middle of the value) |
| Node | 99 | error | dropped | A field value MUST NOT contain line feed (ASCII LF, 0x0a). (Tested at the end of the value) |
| Node | 100 | error | dropped | A field value MUST NOT contain carriage return (ASCII CR, 0x0d). (Tested at the middle of the value) |
| Node | 101 | error | dropped | A field value MUST NOT contain carriage return (ASCII CR, 0x0d). (Tested at the end of the value) |
| Node | 102 | error | dropped | Pseudo-header fields MUST NOT appear in a trailer section. |
| Node | 103 | error | dropped | All HTTP/2 requests MUST include exactly one valid value for the ":method", ":scheme", and ":path" pseudo-header fields, unless they are CONNECT requests (Section 8.5). An HTTP request that omits mandatory pseudo-header fields is malformed (Section 8.1.1). (Tested with :path missing) |
| Node | 104 | error | dropped | Promised requests MUST be safe (see Section 9.2.1 of [HTTP]) and cacheable (see Section 9.2.3 of [HTTP]). |
| Node | 126 | error | dropped | Trailers MUST NOT include pseudo-header fields (Section 8.3). |
| Node | 128 | error | received | Field names MUST NOT contain control characters (0x00-0x1F) |
| Node | 129 | error | received | Field names MUST NOT contain ASCII SP (0x20) |
| Node | 130 | error | dropped | Field names MUST NOT contain DEL character (0x7F) |
| Node | 131 | error | received | Field names MUST NOT contain high byte characters (0x80-0xFF) |
| Node | 132 | error | received | With the exception of pseudo-header fields (Section 8.3), which have a name that starts with a single colon, field names MUST NOT include a colon (ASCII COLON, 0x3a). |
| Node | 133 | error | received | A field value MUST NOT contain line feed (ASCII LF, 0x0a). (Tested at the start of the value) |
| Node | 134 | error | received | A field value MUST NOT contain carriage return (ASCII CR, 0x0d). (Tested at the start of the value) |
| Node | 135 | error | received | A field value MUST NOT start with an ASCII whitespace character (ASCII SP or HTAB, 0x20 or 0x09). |
| Node | 136 | error | received | A field value MUST NOT end with an ASCII whitespace character (ASCII SP or HTAB, 0x20 or 0x09). |
| Node | 160 | error | dropped | An endpoint that receives a HEADERS frame without the END_STREAM flag set after receiving the HEADERS frame that opens a request or after receiving a final (non-informational) status code MUST treat the corresponding request or response as malformed (Section 8.1.1). |
| Node | 161 | error | dropped | A field value MUST NOT contain line feed (ASCII LF, 0x0a). (Tested at the middle of the value) |
| Node | 162 | error | dropped | A field value MUST NOT contain line feed (ASCII LF, 0x0a). (Tested at the end of the value) |
| Node | 163 | error | dropped | A field value MUST NOT contain carriage return (ASCII CR, 0x0d). (Tested at the middle of the value) |
| Node | 164 | error | dropped | A field value MUST NOT contain carriage return (ASCII CR, 0x0d). (Tested at the end of the value) |
| Node | 165 | error | dropped | Pseudo-header fields MUST NOT appear in a trailer section. |
| Envoy | 31 | error | dropped | With the CONNECT method, the " :scheme" and " :path" pseudo-header fields MUST be omitted. (Tested with only :path present) |
| Envoy | 32 | error | dropped | With the CONNECT method, the " :scheme" and " :path" pseudo-header fields MUST be omitted. (Tested with only :scheme present) |
| Envoy | 40 | error | dropped | Trailers MUST NOT include pseudo-header fields (Section 8.3). |
| Envoy | 41 | error | dropped | Field names MUST be converted to lowercase when constructing an HTTP/2 message. |
| Envoy | 42 | error | dropped | Field names MUST NOT contain control characters (0x00-0x1F) |
| Envoy | 43 | error | dropped | Field names MUST NOT contain ASCII SP (0x20) |
| Envoy | 44 | error | dropped | Field names MUST NOT contain DEL character (0x7F) |
| Envoy | 45 | error | dropped | Field names MUST NOT contain high byte characters (0x80-0xFF) |
| Envoy | 46 | error | dropped | With the exception of pseudo-header fields (Section 8.3), which have a name that starts with a single colon, field names MUST NOT include a colon (ASCII COLON, 0x3a). |
| Envoy | 47 | error | dropped | A field value MUST NOT contain line feed (ASCII LF, 0x0a). (Tested at the start of the value) |
| Envoy | 48 | error | dropped | A field value MUST NOT contain carriage return (ASCII CR, 0x0d). (Tested at the start of the value) |
| Envoy | 51 | error | dropped | An endpoint MUST NOT generate an HTTP/2 message containing connection header field (RFC9113 Section 8.2.2) |
| Envoy | 52 | error | dropped | An endpoint MUST NOT generate an HTTP/2 message containing proxy-connection header field (RFC9113 Section 8.2.2) |
| Envoy | 53 | error | dropped | An endpoint MUST NOT generate an HTTP/2 message containing keep-alive header field (RFC9113 Section 8.2.2) |
| Envoy | 54 | error | dropped | An endpoint MUST NOT generate an HTTP/2 message containing transfer-encoding header field (RFC9113 Section 8.2.2) |
| Envoy | 55 | error | dropped | An endpoint MUST NOT generate an HTTP/2 message containing upgrade header field (RFC9113 Section 8.2.2) |
| Envoy | 56 | error | dropped | The TE header field MAY be present in an HTTP/2 request; when it is, it MUST NOT contain any value other than 'trailers'. |
| Envoy | 57 | error | dropped | Pseudo-header fields are not HTTP header fields. Endpoints MUST NOT generate pseudo-header fields other than those defined in this document. |
| Envoy | 59 | error | dropped | Pseudo-header fields defined for responses MUST NOT appear in requests. |
| Envoy | 60 | error | dropped | All pseudo-header fields sent from a client MUST appear in a field block before all regular field lines. Any request or response that contains a pseudo-header field that appears in a field block after a regular field line MUST be treated as malformed (Section 8.1.1). |
| Envoy | 62 | error | dropped | The same pseudo-header field name MUST NOT appear more than once in a field block. A field block for an HTTP request or response that contains a repeated pseudo-header field name MUST be treated as malformed (Section 8.1.1). Tested with a request frame with the same value. |
| Envoy | 63 | error | dropped | The same pseudo-header field name MUST NOT appear more than once in a field block. A field block for an HTTP request or response that contains a repeated pseudo-header field name MUST be treated as malformed (Section 8.1.1). Tested with a request frame with different values. |
| Envoy | 68 | error | dropped | The ":path" pseudo-header field MUST NOT be empty for "http" or "https" URIs; "http" or "https" URIs that do not contain a path component MUST include a value of '/'. |
| Envoy | 69 | error | dropped | All HTTP/2 requests MUST include exactly one valid value for the ":method", ":scheme", and ":path" pseudo-header fields, unless they are CONNECT requests (Section 8.5). An HTTP request that omits mandatory pseudo-header fields is malformed (Section 8.1.1). (Tested with :method missing) |
| Envoy | 70 | error | dropped | All HTTP/2 requests MUST include exactly one valid value for the ":method", ":scheme", and ":path" pseudo-header fields, unless they are CONNECT requests (Section 8.5). An HTTP request that omits mandatory pseudo-header fields is malformed (Section 8.1.1). (Tested with :scheme missing) |
| Envoy | 74 | error | dropped | With the CONNECT method, the ":scheme" and ":path" pseudo-header fields MUST be omitted. (Tested with both present) |
| Envoy | 97 | error | dropped | An endpoint that receives a HEADERS frame without the END_STREAM flag set after receiving the HEADERS frame that opens a request or after receiving a final (non-informational) status code MUST treat the corresponding request or response as malformed (Section 8.1.1). |
| Envoy | 98 | error | dropped | A field value MUST NOT contain line feed (ASCII LF, 0x0a). (Tested at the middle of the value) |
| Envoy | 99 | error | dropped | A field value MUST NOT contain line feed (ASCII LF, 0x0a). (Tested at the end of the value) |
| Envoy | 100 | error | dropped | A field value MUST NOT contain carriage return (ASCII CR, 0x0d). (Tested at the middle of the value) |
| Envoy | 101 | error | dropped | A field value MUST NOT contain carriage return (ASCII CR, 0x0d). (Tested at the end of the value) |
| Envoy | 102 | error | dropped | Pseudo-header fields MUST NOT appear in a trailer section. |
| Envoy | 103 | error | dropped | All HTTP/2 requests MUST include exactly one valid value for the ":method", ":scheme", and ":path" pseudo-header fields, unless they are CONNECT requests (Section 8.5). An HTTP request that omits mandatory pseudo-header fields is malformed (Section 8.1.1). (Tested with :path missing) |
| Envoy | 126 | error | dropped | Trailers MUST NOT include pseudo-header fields (Section 8.3). |
| Envoy | 135 | error | received | A field value MUST NOT start with an ASCII whitespace character (ASCII SP or HTAB, 0x20 or 0x09). |
| Envoy | 136 | error | received | A field value MUST NOT end with an ASCII whitespace character (ASCII SP or HTAB, 0x20 or 0x09). |
| Envoy | 160 | error | dropped | An endpoint that receives a HEADERS frame without the END_STREAM flag set after receiving the HEADERS frame that opens a request or after receiving a final (non-informational) status code MUST treat the corresponding request or response as malformed (Section 8.1.1). |
| Envoy | 165 | error | dropped | Pseudo-header fields MUST NOT appear in a trailer section. |
| H2O | 31 | error | dropped | With the CONNECT method, the " :scheme" and " :path" pseudo-header fields MUST be omitted. (Tested with only :path present) |
| H2O | 32 | error | dropped | With the CONNECT method, the " :scheme" and " :path" pseudo-header fields MUST be omitted. (Tested with only :scheme present) |
| H2O | 42 | error | dropped | Field names MUST NOT contain control characters (0x00-0x1F) |
| H2O | 43 | error | dropped | Field names MUST NOT contain ASCII SP (0x20) |
| H2O | 44 | error | dropped | Field names MUST NOT contain DEL character (0x7F) |
| H2O | 45 | error | dropped | Field names MUST NOT contain high byte characters (0x80-0xFF) |
| H2O | 46 | error | dropped | With the exception of pseudo-header fields (Section 8.3), which have a name that starts with a single colon, field names MUST NOT include a colon (ASCII COLON, 0x3a). |
| H2O | 47 | error | dropped | A field value MUST NOT contain line feed (ASCII LF, 0x0a). (Tested at the start of the value) |
| H2O | 48 | error | dropped | A field value MUST NOT contain carriage return (ASCII CR, 0x0d). (Tested at the start of the value) |
| H2O | 49 | error | dropped | A field value MUST NOT start with an ASCII whitespace character (ASCII SP or HTAB, 0x20 or 0x09). |
| H2O | 50 | error | dropped | A field value MUST NOT end with an ASCII whitespace character (ASCII SP or HTAB, 0x20 or 0x09). |
| H2O | 52 | error | dropped | An endpoint MUST NOT generate an HTTP/2 message containing proxy-connection header field (RFC9113 Section 8.2.2) |
| H2O | 53 | error | dropped | An endpoint MUST NOT generate an HTTP/2 message containing keep-alive header field (RFC9113 Section 8.2.2) |
| H2O | 58 | error | dropped | Pseudo-header fields defined for requests MUST NOT appear in responses. |
| H2O | 61 | error | dropped | All pseudo-header fields sent from a server MUST appear in a field block before all regular field lines. Any request or response that contains a pseudo-header field that appears in a field block after a regular field line MUST be treated as malformed (Section 8.1.1). |
| H2O | 64 | error | dropped | The same pseudo-header field name MUST NOT appear more than once in a field block. A field block for an HTTP request or response that contains a repeated pseudo-header field name MUST be treated as malformed (Section 8.1.1). Tested with a response frame with the same value. |
| H2O | 65 | error | dropped | The same pseudo-header field name MUST NOT appear more than once in a field block. A field block for an HTTP request or response that contains a repeated pseudo-header field name MUST be treated as malformed (Section 8.1.1). Tested with a response frame with different values. |
| H2O | 66 | error | dropped | Clients MUST NOT generate a request with a Host header field that differs from the ":authority" pseudo-header field. |
| H2O | 67 | error | dropped | ':authority' MUST NOT include the deprecated userinfo subcomponent for "http" or "https" schemed URIs. |
| H2O | 69 | error | dropped | All HTTP/2 requests MUST include exactly one valid value for the ":method", ":scheme", and ":path" pseudo-header fields, unless they are CONNECT requests (Section 8.5). An HTTP request that omits mandatory pseudo-header fields is malformed (Section 8.1.1). (Tested with :method missing) |
| H2O | 70 | error | dropped | All HTTP/2 requests MUST include exactly one valid value for the ":method", ":scheme", and ":path" pseudo-header fields, unless they are CONNECT requests (Section 8.5). An HTTP request that omits mandatory pseudo-header fields is malformed (Section 8.1.1). (Tested with :scheme missing) |
| H2O | 71 | error | dropped | For HTTP/2 responses, a single ":status" pseudo-header field is defined that carries the HTTP status code field. This pseudo-header field MUST be included in all responses, including interim responses; otherwise, the response is malformed. |
| H2O | 73 | error | dropped | In the PUSH_PROMISE frame, the server MUST include a method in the ":method" pseudo-header field that is safe and cacheable. |
| H2O | 74 | error | dropped | With the CONNECT method, the ":scheme" and ":path" pseudo-header fields MUST be omitted. (Tested with both present) |
| H2O | 75 | ignore | 500 | With the CONNECT method, The ":authority" pseudo-header field contains the host and port to connect to |
| H2O | 98 | error | dropped | A field value MUST NOT contain line feed (ASCII LF, 0x0a). (Tested at the middle of the value) |
| H2O | 99 | error | dropped | A field value MUST NOT contain line feed (ASCII LF, 0x0a). (Tested at the end of the value) |
| H2O | 100 | error | dropped | A field value MUST NOT contain carriage return (ASCII CR, 0x0d). (Tested at the middle of the value) |
| H2O | 101 | error | dropped | A field value MUST NOT contain carriage return (ASCII CR, 0x0d). (Tested at the end of the value) |
| H2O | 103 | error | dropped | All HTTP/2 requests MUST include exactly one valid value for the ":method", ":scheme", and ":path" pseudo-header fields, unless they are CONNECT requests (Section 8.5). An HTTP request that omits mandatory pseudo-header fields is malformed (Section 8.1.1). (Tested with :path missing) |
| H2O | 104 | error | dropped | Promised requests MUST be safe (see Section 9.2.1 of [HTTP]) and cacheable (see Section 9.2.3 of [HTTP]). |
| H2O | 126 | error | dropped | Trailers MUST NOT include pseudo-header fields (Section 8.3). |
| H2O | 127 | error | dropped | Field names MUST be converted to lowercase when constructing an HTTP/2 message. |
| H2O | 128 | error | dropped | Field names MUST NOT contain control characters (0x00-0x1F) |
| H2O | 129 | error | dropped | Field names MUST NOT contain ASCII SP (0x20) |
| H2O | 130 | error | dropped | Field names MUST NOT contain DEL character (0x7F) |
| H2O | 131 | error | dropped | Field names MUST NOT contain high byte characters (0x80-0xFF) |
| H2O | 132 | error | dropped | With the exception of pseudo-header fields (Section 8.3), which have a name that starts with a single colon, field names MUST NOT include a colon (ASCII COLON, 0x3a). |
| H2O | 133 | error | dropped | A field value MUST NOT contain line feed (ASCII LF, 0x0a). (Tested at the start of the value) |
| H2O | 134 | error | dropped | A field value MUST NOT contain carriage return (ASCII CR, 0x0d). (Tested at the start of the value) |
| H2O | 135 | error | dropped | A field value MUST NOT start with an ASCII whitespace character (ASCII SP or HTAB, 0x20 or 0x09). |
| H2O | 136 | error | dropped | A field value MUST NOT end with an ASCII whitespace character (ASCII SP or HTAB, 0x20 or 0x09). |
| H2O | 137 | error | dropped | An endpoint MUST NOT generate an HTTP/2 message containing connection header field (RFC9113 Section 8.2.2) |
| H2O | 138 | error | dropped | An endpoint MUST NOT generate an HTTP/2 message containing proxy-connection header field (RFC9113 Section 8.2.2) |
| H2O | 139 | error | dropped | An endpoint MUST NOT generate an HTTP/2 message containing keep-alive header field (RFC9113 Section 8.2.2) |
| H2O | 140 | error | dropped | An endpoint MUST NOT generate an HTTP/2 message containing transfer-encoding header field (RFC9113 Section 8.2.2) |
| H2O | 141 | error | dropped | An endpoint MUST NOT generate an HTTP/2 message containing upgrade header field (RFC9113 Section 8.2.2) |
| H2O | 142 | error | dropped | The TE header field MAY be present in an HTTP/2 request; when it is, it MUST NOT contain any value other than 'trailers'. |
| H2O | 143 | error | dropped | Pseudo-header fields are not HTTP header fields. Endpoints MUST NOT generate pseudo-header fields other than those defined in this document. |
| Cloudflare | 31 | error | dropped | With the CONNECT method, the " :scheme" and " :path" pseudo-header fields MUST be omitted. (Tested with only :path present) |
| Cloudflare | 32 | error | dropped | With the CONNECT method, the " :scheme" and " :path" pseudo-header fields MUST be omitted. (Tested with only :scheme present) |
| Cloudflare | 41 | error | dropped | Field names MUST be converted to lowercase when constructing an HTTP/2 message. |
| Cloudflare | 42 | error | dropped | Field names MUST NOT contain control characters (0x00-0x1F) |
| Cloudflare | 43 | error | dropped | Field names MUST NOT contain ASCII SP (0x20) |
| Cloudflare | 44 | error | dropped | Field names MUST NOT contain DEL character (0x7F) |
| Cloudflare | 45 | error | dropped | Field names MUST NOT contain high byte characters (0x80-0xFF) |
| Cloudflare | 46 | error | dropped | With the exception of pseudo-header fields (Section 8.3), which have a name that starts with a single colon, field names MUST NOT include a colon (ASCII COLON, 0x3a). |
| Cloudflare | 47 | error | dropped | A field value MUST NOT contain line feed (ASCII LF, 0x0a). (Tested at the start of the value) |
| Cloudflare | 48 | error | dropped | A field value MUST NOT contain carriage return (ASCII CR, 0x0d). (Tested at the start of the value) |
| Cloudflare | 49 | error | dropped | A field value MUST NOT start with an ASCII whitespace character (ASCII SP or HTAB, 0x20 or 0x09). |
| Cloudflare | 50 | error | dropped | A field value MUST NOT end with an ASCII whitespace character (ASCII SP or HTAB, 0x20 or 0x09). |
| Cloudflare | 51 | error | dropped | An endpoint MUST NOT generate an HTTP/2 message containing connection header field (RFC9113 Section 8.2.2) |
| Cloudflare | 52 | error | dropped | An endpoint MUST NOT generate an HTTP/2 message containing proxy-connection header field (RFC9113 Section 8.2.2) |
| Cloudflare | 53 | error | dropped | An endpoint MUST NOT generate an HTTP/2 message containing keep-alive header field (RFC9113 Section 8.2.2) |
| Cloudflare | 54 | error | dropped | An endpoint MUST NOT generate an HTTP/2 message containing transfer-encoding header field (RFC9113 Section 8.2.2) |
| Cloudflare | 55 | error | dropped | An endpoint MUST NOT generate an HTTP/2 message containing upgrade header field (RFC9113 Section 8.2.2) |
| Cloudflare | 56 | error | dropped | The TE header field MAY be present in an HTTP/2 request; when it is, it MUST NOT contain any value other than 'trailers'. |
| Cloudflare | 57 | error | dropped | Pseudo-header fields are not HTTP header fields. Endpoints MUST NOT generate pseudo-header fields other than those defined in this document. |
| Cloudflare | 58 | error | modified | Pseudo-header fields defined for requests MUST NOT appear in responses. |
| Cloudflare | 59 | error | dropped | Pseudo-header fields defined for responses MUST NOT appear in requests. |
| Cloudflare | 60 | error | dropped | All pseudo-header fields sent from a client MUST appear in a field block before all regular field lines. Any request or response that contains a pseudo-header field that appears in a field block after a regular field line MUST be treated as malformed (Section 8.1.1). |
| Cloudflare | 62 | error | dropped | The same pseudo-header field name MUST NOT appear more than once in a field block. A field block for an HTTP request or response that contains a repeated pseudo-header field name MUST be treated as malformed (Section 8.1.1). Tested with a request frame with the same value. |
| Cloudflare | 63 | error | dropped | The same pseudo-header field name MUST NOT appear more than once in a field block. A field block for an HTTP request or response that contains a repeated pseudo-header field name MUST be treated as malformed (Section 8.1.1). Tested with a request frame with different values. |
| Cloudflare | 66 | error | dropped | Clients MUST NOT generate a request with a Host header field that differs from the ":authority" pseudo-header field. |
| Cloudflare | 67 | error | dropped | ':authority' MUST NOT include the deprecated userinfo subcomponent for "http" or "https" schemed URIs. |
| Cloudflare | 68 | error | dropped | The ":path" pseudo-header field MUST NOT be empty for "http" or "https" URIs; "http" or "https" URIs that do not contain a path component MUST include a value of '/'. |
| Cloudflare | 69 | error | dropped | All HTTP/2 requests MUST include exactly one valid value for the ":method", ":scheme", and ":path" pseudo-header fields, unless they are CONNECT requests (Section 8.5). An HTTP request that omits mandatory pseudo-header fields is malformed (Section 8.1.1). (Tested with :method missing) |
| Cloudflare | 70 | error | dropped | All HTTP/2 requests MUST include exactly one valid value for the ":method", ":scheme", and ":path" pseudo-header fields, unless they are CONNECT requests (Section 8.5). An HTTP request that omits mandatory pseudo-header fields is malformed (Section 8.1.1). (Tested with :scheme missing) |
| Cloudflare | 71 | error | dropped | For HTTP/2 responses, a single ":status" pseudo-header field is defined that carries the HTTP status code field. This pseudo-header field MUST be included in all responses, including interim responses; otherwise, the response is malformed. |
| Cloudflare | 74 | error | dropped | With the CONNECT method, the ":scheme" and ":path" pseudo-header fields MUST be omitted. (Tested with both present) |
| Cloudflare | 97 | error | dropped | An endpoint that receives a HEADERS frame without the END_STREAM flag set after receiving the HEADERS frame that opens a request or after receiving a final (non-informational) status code MUST treat the corresponding request or response as malformed (Section 8.1.1). |
| Cloudflare | 98 | error | dropped | A field value MUST NOT contain line feed (ASCII LF, 0x0a). (Tested at the middle of the value) |
| Cloudflare | 99 | error | dropped | A field value MUST NOT contain line feed (ASCII LF, 0x0a). (Tested at the end of the value) |
| Cloudflare | 100 | error | dropped | A field value MUST NOT contain carriage return (ASCII CR, 0x0d). (Tested at the middle of the value) |
| Cloudflare | 101 | error | dropped | A field value MUST NOT contain carriage return (ASCII CR, 0x0d). (Tested at the end of the value) |
| Cloudflare | 103 | error | dropped | All HTTP/2 requests MUST include exactly one valid value for the ":method", ":scheme", and ":path" pseudo-header fields, unless they are CONNECT requests (Section 8.5). An HTTP request that omits mandatory pseudo-header fields is malformed (Section 8.1.1). (Tested with :path missing) |
| Cloudflare | 126 | error | received | Trailers MUST NOT include pseudo-header fields (Section 8.3). |
| Cloudflare | 128 | error | dropped | Field names MUST NOT contain control characters (0x00-0x1F) |
| Cloudflare | 130 | error | dropped | Field names MUST NOT contain DEL character (0x7F) |
| Cloudflare | 132 | error | dropped | With the exception of pseudo-header fields (Section 8.3), which have a name that starts with a single colon, field names MUST NOT include a colon (ASCII COLON, 0x3a). |
| Cloudflare | 135 | error | modified | A field value MUST NOT start with an ASCII whitespace character (ASCII SP or HTAB, 0x20 or 0x09). |
| Cloudflare | 141 | error | modified | An endpoint MUST NOT generate an HTTP/2 message containing upgrade header field (RFC9113 Section 8.2.2) |
| Cloudflare | 142 | error | dropped | The TE header field MAY be present in an HTTP/2 request; when it is, it MUST NOT contain any value other than 'trailers'. |
| Cloudflare | 160 | error | dropped | An endpoint that receives a HEADERS frame without the END_STREAM flag set after receiving the HEADERS frame that opens a request or after receiving a final (non-informational) status code MUST treat the corresponding request or response as malformed (Section 8.1.1). |
| Cloudflare | 162 | error | dropped | A field value MUST NOT contain line feed (ASCII LF, 0x0a). (Tested at the end of the value) |
| Cloudflare | 165 | error | dropped | Pseudo-header fields MUST NOT appear in a trailer section. |
| Mitmproxy | 31 | error | received | With the CONNECT method, the " :scheme" and " :path" pseudo-header fields MUST be omitted. (Tested with only :path present) |
| Mitmproxy | 32 | error | received | With the CONNECT method, the " :scheme" and " :path" pseudo-header fields MUST be omitted. (Tested with only :scheme present) |
| Mitmproxy | 40 | error | received | Trailers MUST NOT include pseudo-header fields (Section 8.3). |
| Mitmproxy | 41 | error | received | Field names MUST be converted to lowercase when constructing an HTTP/2 message. |
| Mitmproxy | 42 | error | received | Field names MUST NOT contain control characters (0x00-0x1F) |
| Mitmproxy | 43 | error | received | Field names MUST NOT contain ASCII SP (0x20) |
| Mitmproxy | 44 | error | received | Field names MUST NOT contain DEL character (0x7F) |
| Mitmproxy | 45 | error | received | Field names MUST NOT contain high byte characters (0x80-0xFF) |
| Mitmproxy | 46 | error | received | With the exception of pseudo-header fields (Section 8.3), which have a name that starts with a single colon, field names MUST NOT include a colon (ASCII COLON, 0x3a). |
| Mitmproxy | 47 | error | received | A field value MUST NOT contain line feed (ASCII LF, 0x0a). (Tested at the start of the value) |
| Mitmproxy | 48 | error | received | A field value MUST NOT contain carriage return (ASCII CR, 0x0d). (Tested at the start of the value) |
| Mitmproxy | 49 | error | received | A field value MUST NOT start with an ASCII whitespace character (ASCII SP or HTAB, 0x20 or 0x09). |
| Mitmproxy | 50 | error | received | A field value MUST NOT end with an ASCII whitespace character (ASCII SP or HTAB, 0x20 or 0x09). |
| Mitmproxy | 51 | error | received | An endpoint MUST NOT generate an HTTP/2 message containing connection header field (RFC9113 Section 8.2.2) |
| Mitmproxy | 52 | error | received | An endpoint MUST NOT generate an HTTP/2 message containing proxy-connection header field (RFC9113 Section 8.2.2) |
| Mitmproxy | 53 | error | received | An endpoint MUST NOT generate an HTTP/2 message containing keep-alive header field (RFC9113 Section 8.2.2) |
| Mitmproxy | 54 | error | received | An endpoint MUST NOT generate an HTTP/2 message containing transfer-encoding header field (RFC9113 Section 8.2.2) |
| Mitmproxy | 55 | error | received | An endpoint MUST NOT generate an HTTP/2 message containing upgrade header field (RFC9113 Section 8.2.2) |
| Mitmproxy | 56 | error | received | The TE header field MAY be present in an HTTP/2 request; when it is, it MUST NOT contain any value other than 'trailers'. |
| Mitmproxy | 57 | error | received | Pseudo-header fields are not HTTP header fields. Endpoints MUST NOT generate pseudo-header fields other than those defined in this document. |
| Mitmproxy | 58 | error | received | Pseudo-header fields defined for requests MUST NOT appear in responses. |
| Mitmproxy | 59 | error | received | Pseudo-header fields defined for responses MUST NOT appear in requests. |
| Mitmproxy | 60 | error | received | All pseudo-header fields sent from a client MUST appear in a field block before all regular field lines. Any request or response that contains a pseudo-header field that appears in a field block after a regular field line MUST be treated as malformed (Section 8.1.1). |
| Mitmproxy | 61 | error | received | All pseudo-header fields sent from a server MUST appear in a field block before all regular field lines. Any request or response that contains a pseudo-header field that appears in a field block after a regular field line MUST be treated as malformed (Section 8.1.1). |
| Mitmproxy | 62 | error | received | The same pseudo-header field name MUST NOT appear more than once in a field block. A field block for an HTTP request or response that contains a repeated pseudo-header field name MUST be treated as malformed (Section 8.1.1). Tested with a request frame with the same value. |
| Mitmproxy | 63 | error | received | The same pseudo-header field name MUST NOT appear more than once in a field block. A field block for an HTTP request or response that contains a repeated pseudo-header field name MUST be treated as malformed (Section 8.1.1). Tested with a request frame with different values. |
| Mitmproxy | 64 | error | received | The same pseudo-header field name MUST NOT appear more than once in a field block. A field block for an HTTP request or response that contains a repeated pseudo-header field name MUST be treated as malformed (Section 8.1.1). Tested with a response frame with the same value. |
| Mitmproxy | 65 | error | received | The same pseudo-header field name MUST NOT appear more than once in a field block. A field block for an HTTP request or response that contains a repeated pseudo-header field name MUST be treated as malformed (Section 8.1.1). Tested with a response frame with different values. |
| Mitmproxy | 66 | error | received | Clients MUST NOT generate a request with a Host header field that differs from the ":authority" pseudo-header field. |
| Mitmproxy | 67 | error | received | ':authority' MUST NOT include the deprecated userinfo subcomponent for "http" or "https" schemed URIs. |
| Mitmproxy | 68 | error | received | The ":path" pseudo-header field MUST NOT be empty for "http" or "https" URIs; "http" or "https" URIs that do not contain a path component MUST include a value of '/'. |
| Mitmproxy | 69 | error | received | All HTTP/2 requests MUST include exactly one valid value for the ":method", ":scheme", and ":path" pseudo-header fields, unless they are CONNECT requests (Section 8.5). An HTTP request that omits mandatory pseudo-header fields is malformed (Section 8.1.1). (Tested with :method missing) |
| Mitmproxy | 70 | error | received | All HTTP/2 requests MUST include exactly one valid value for the ":method", ":scheme", and ":path" pseudo-header fields, unless they are CONNECT requests (Section 8.5). An HTTP request that omits mandatory pseudo-header fields is malformed (Section 8.1.1). (Tested with :scheme missing) |
| Mitmproxy | 71 | error | received | For HTTP/2 responses, a single ":status" pseudo-header field is defined that carries the HTTP status code field. This pseudo-header field MUST be included in all responses, including interim responses; otherwise, the response is malformed. |
| Mitmproxy | 73 | error | received | In the PUSH_PROMISE frame, the server MUST include a method in the ":method" pseudo-header field that is safe and cacheable. |
| Mitmproxy | 74 | error | received | With the CONNECT method, the ":scheme" and ":path" pseudo-header fields MUST be omitted. (Tested with both present) |
| Mitmproxy | 75 | ignore | received | With the CONNECT method, The ":authority" pseudo-header field contains the host and port to connect to |
| Mitmproxy | 97 | error | received | An endpoint that receives a HEADERS frame without the END_STREAM flag set after receiving the HEADERS frame that opens a request or after receiving a final (non-informational) status code MUST treat the corresponding request or response as malformed (Section 8.1.1). |
| Mitmproxy | 98 | error | received | A field value MUST NOT contain line feed (ASCII LF, 0x0a). (Tested at the middle of the value) |
| Mitmproxy | 99 | error | received | A field value MUST NOT contain line feed (ASCII LF, 0x0a). (Tested at the end of the value) |
| Mitmproxy | 100 | error | received | A field value MUST NOT contain carriage return (ASCII CR, 0x0d). (Tested at the middle of the value) |
| Mitmproxy | 101 | error | received | A field value MUST NOT contain carriage return (ASCII CR, 0x0d). (Tested at the end of the value) |
| Mitmproxy | 102 | error | received | Pseudo-header fields MUST NOT appear in a trailer section. |
| Mitmproxy | 103 | error | received | All HTTP/2 requests MUST include exactly one valid value for the ":method", ":scheme", and ":path" pseudo-header fields, unless they are CONNECT requests (Section 8.5). An HTTP request that omits mandatory pseudo-header fields is malformed (Section 8.1.1). (Tested with :path missing) |
| Mitmproxy | 104 | error | received | Promised requests MUST be safe (see Section 9.2.1 of [HTTP]) and cacheable (see Section 9.2.3 of [HTTP]). |
| Mitmproxy | 126 | error | received | Trailers MUST NOT include pseudo-header fields (Section 8.3). |
| Mitmproxy | 127 | error | received | Field names MUST be converted to lowercase when constructing an HTTP/2 message. |
| Mitmproxy | 128 | error | received | Field names MUST NOT contain control characters (0x00-0x1F) |
| Mitmproxy | 129 | error | received | Field names MUST NOT contain ASCII SP (0x20) |
| Mitmproxy | 130 | error | received | Field names MUST NOT contain DEL character (0x7F) |
| Mitmproxy | 131 | error | received | Field names MUST NOT contain high byte characters (0x80-0xFF) |
| Mitmproxy | 132 | error | received | With the exception of pseudo-header fields (Section 8.3), which have a name that starts with a single colon, field names MUST NOT include a colon (ASCII COLON, 0x3a). |
| Mitmproxy | 133 | error | received | A field value MUST NOT contain line feed (ASCII LF, 0x0a). (Tested at the start of the value) |
| Mitmproxy | 134 | error | received | A field value MUST NOT contain carriage return (ASCII CR, 0x0d). (Tested at the start of the value) |
| Mitmproxy | 135 | error | received | A field value MUST NOT start with an ASCII whitespace character (ASCII SP or HTAB, 0x20 or 0x09). |
| Mitmproxy | 136 | error | received | A field value MUST NOT end with an ASCII whitespace character (ASCII SP or HTAB, 0x20 or 0x09). |
| Mitmproxy | 137 | error | received | An endpoint MUST NOT generate an HTTP/2 message containing connection header field (RFC9113 Section 8.2.2) |
| Mitmproxy | 138 | error | received | An endpoint MUST NOT generate an HTTP/2 message containing proxy-connection header field (RFC9113 Section 8.2.2) |
| Mitmproxy | 139 | error | received | An endpoint MUST NOT generate an HTTP/2 message containing keep-alive header field (RFC9113 Section 8.2.2) |
| Mitmproxy | 140 | error | received | An endpoint MUST NOT generate an HTTP/2 message containing transfer-encoding header field (RFC9113 Section 8.2.2) |
| Mitmproxy | 141 | error | received | An endpoint MUST NOT generate an HTTP/2 message containing upgrade header field (RFC9113 Section 8.2.2) |
| Mitmproxy | 142 | error | received | The TE header field MAY be present in an HTTP/2 request; when it is, it MUST NOT contain any value other than 'trailers'. |
| Mitmproxy | 143 | error | received | Pseudo-header fields are not HTTP header fields. Endpoints MUST NOT generate pseudo-header fields other than those defined in this document. |
| Mitmproxy | 160 | error | received | An endpoint that receives a HEADERS frame without the END_STREAM flag set after receiving the HEADERS frame that opens a request or after receiving a final (non-informational) status code MUST treat the corresponding request or response as malformed (Section 8.1.1). |
| Mitmproxy | 161 | error | received | A field value MUST NOT contain line feed (ASCII LF, 0x0a). (Tested at the middle of the value) |
| Mitmproxy | 162 | error | received | A field value MUST NOT contain line feed (ASCII LF, 0x0a). (Tested at the end of the value) |
| Mitmproxy | 163 | error | received | A field value MUST NOT contain carriage return (ASCII CR, 0x0d). (Tested at the middle of the value) |
| Mitmproxy | 164 | error | received | A field value MUST NOT contain carriage return (ASCII CR, 0x0d). (Tested at the end of the value) |
| Mitmproxy | 165 | error | received | Pseudo-header fields MUST NOT appear in a trailer section. |
| Mitmproxy | 166 | error | received | HTTP/2 does not support the 101 (Switching Protocols) informational status code (Section 15.2.2 of [HTTP]). |
| Azure-AG | 31 | error | dropped | With the CONNECT method, the " :scheme" and " :path" pseudo-header fields MUST be omitted. (Tested with only :path present) |
| Azure-AG | 32 | error | dropped | With the CONNECT method, the " :scheme" and " :path" pseudo-header fields MUST be omitted. (Tested with only :scheme present) |
| Azure-AG | 41 | error | dropped | Field names MUST be converted to lowercase when constructing an HTTP/2 message. |
| Azure-AG | 42 | error | dropped | Field names MUST NOT contain control characters (0x00-0x1F) |
| Azure-AG | 43 | error | dropped | Field names MUST NOT contain ASCII SP (0x20) |
| Azure-AG | 44 | error | received | Field names MUST NOT contain DEL character (0x7F) |
| Azure-AG | 45 | error | dropped | Field names MUST NOT contain high byte characters (0x80-0xFF) |
| Azure-AG | 46 | error | dropped | With the exception of pseudo-header fields (Section 8.3), which have a name that starts with a single colon, field names MUST NOT include a colon (ASCII COLON, 0x3a). |
| Azure-AG | 47 | error | dropped | A field value MUST NOT contain line feed (ASCII LF, 0x0a). (Tested at the start of the value) |
| Azure-AG | 48 | error | dropped | A field value MUST NOT contain carriage return (ASCII CR, 0x0d). (Tested at the start of the value) |
| Azure-AG | 49 | error | dropped | A field value MUST NOT start with an ASCII whitespace character (ASCII SP or HTAB, 0x20 or 0x09). |
| Azure-AG | 50 | error | dropped | A field value MUST NOT end with an ASCII whitespace character (ASCII SP or HTAB, 0x20 or 0x09). |
| Azure-AG | 51 | error | dropped | An endpoint MUST NOT generate an HTTP/2 message containing connection header field (RFC9113 Section 8.2.2) |
| Azure-AG | 52 | error | dropped | An endpoint MUST NOT generate an HTTP/2 message containing proxy-connection header field (RFC9113 Section 8.2.2) |
| Azure-AG | 53 | error | dropped | An endpoint MUST NOT generate an HTTP/2 message containing keep-alive header field (RFC9113 Section 8.2.2) |
| Azure-AG | 54 | error | dropped | An endpoint MUST NOT generate an HTTP/2 message containing transfer-encoding header field (RFC9113 Section 8.2.2) |
| Azure-AG | 55 | error | dropped | An endpoint MUST NOT generate an HTTP/2 message containing upgrade header field (RFC9113 Section 8.2.2) |
| Azure-AG | 56 | error | dropped | The TE header field MAY be present in an HTTP/2 request; when it is, it MUST NOT contain any value other than 'trailers'. |
| Azure-AG | 57 | error | dropped | Pseudo-header fields are not HTTP header fields. Endpoints MUST NOT generate pseudo-header fields other than those defined in this document. |
| Azure-AG | 59 | error | dropped | Pseudo-header fields defined for responses MUST NOT appear in requests. |
| Azure-AG | 60 | error | dropped | All pseudo-header fields sent from a client MUST appear in a field block before all regular field lines. Any request or response that contains a pseudo-header field that appears in a field block after a regular field line MUST be treated as malformed (Section 8.1.1). |
| Azure-AG | 62 | error | dropped | The same pseudo-header field name MUST NOT appear more than once in a field block. A field block for an HTTP request or response that contains a repeated pseudo-header field name MUST be treated as malformed (Section 8.1.1). Tested with a request frame with the same value. |
| Azure-AG | 63 | error | dropped | The same pseudo-header field name MUST NOT appear more than once in a field block. A field block for an HTTP request or response that contains a repeated pseudo-header field name MUST be treated as malformed (Section 8.1.1). Tested with a request frame with different values. |
| Azure-AG | 66 | error | dropped | Clients MUST NOT generate a request with a Host header field that differs from the ":authority" pseudo-header field. |
| Azure-AG | 67 | error | dropped | ':authority' MUST NOT include the deprecated userinfo subcomponent for "http" or "https" schemed URIs. |
| Azure-AG | 68 | error | dropped | The ":path" pseudo-header field MUST NOT be empty for "http" or "https" URIs; "http" or "https" URIs that do not contain a path component MUST include a value of '/'. |
| Azure-AG | 69 | error | dropped | All HTTP/2 requests MUST include exactly one valid value for the ":method", ":scheme", and ":path" pseudo-header fields, unless they are CONNECT requests (Section 8.5). An HTTP request that omits mandatory pseudo-header fields is malformed (Section 8.1.1). (Tested with :method missing) |
| Azure-AG | 70 | error | dropped | All HTTP/2 requests MUST include exactly one valid value for the ":method", ":scheme", and ":path" pseudo-header fields, unless they are CONNECT requests (Section 8.5). An HTTP request that omits mandatory pseudo-header fields is malformed (Section 8.1.1). (Tested with :scheme missing) |
| Azure-AG | 74 | error | dropped | With the CONNECT method, the ":scheme" and ":path" pseudo-header fields MUST be omitted. (Tested with both present) |
| Azure-AG | 98 | error | dropped | A field value MUST NOT contain line feed (ASCII LF, 0x0a). (Tested at the middle of the value) |
| Azure-AG | 99 | error | dropped | A field value MUST NOT contain line feed (ASCII LF, 0x0a). (Tested at the end of the value) |
| Azure-AG | 100 | error | dropped | A field value MUST NOT contain carriage return (ASCII CR, 0x0d). (Tested at the middle of the value) |
| Azure-AG | 101 | error | dropped | A field value MUST NOT contain carriage return (ASCII CR, 0x0d). (Tested at the end of the value) |
| Azure-AG | 103 | error | dropped | All HTTP/2 requests MUST include exactly one valid value for the ":method", ":scheme", and ":path" pseudo-header fields, unless they are CONNECT requests (Section 8.5). An HTTP request that omits mandatory pseudo-header fields is malformed (Section 8.1.1). (Tested with :path missing) |
| Nginx | 31 | error | dropped | With the CONNECT method, the " :scheme" and " :path" pseudo-header fields MUST be omitted. (Tested with only :path present) |
| Nginx | 32 | error | dropped | With the CONNECT method, the " :scheme" and " :path" pseudo-header fields MUST be omitted. (Tested with only :scheme present) |
| Nginx | 41 | error | dropped | Field names MUST be converted to lowercase when constructing an HTTP/2 message. |
| Nginx | 42 | error | dropped | Field names MUST NOT contain control characters (0x00-0x1F) |
| Nginx | 43 | error | dropped | Field names MUST NOT contain ASCII SP (0x20) |
| Nginx | 44 | error | dropped | Field names MUST NOT contain DEL character (0x7F) |
| Nginx | 45 | error | dropped | Field names MUST NOT contain high byte characters (0x80-0xFF) |
| Nginx | 46 | error | dropped | With the exception of pseudo-header fields (Section 8.3), which have a name that starts with a single colon, field names MUST NOT include a colon (ASCII COLON, 0x3a). |
| Nginx | 47 | error | dropped | A field value MUST NOT contain line feed (ASCII LF, 0x0a). (Tested at the start of the value) |
| Nginx | 48 | error | dropped | A field value MUST NOT contain carriage return (ASCII CR, 0x0d). (Tested at the start of the value) |
| Nginx | 49 | error | dropped | A field value MUST NOT start with an ASCII whitespace character (ASCII SP or HTAB, 0x20 or 0x09). |
| Nginx | 50 | error | dropped | A field value MUST NOT end with an ASCII whitespace character (ASCII SP or HTAB, 0x20 or 0x09). |
| Nginx | 51 | error | dropped | An endpoint MUST NOT generate an HTTP/2 message containing connection header field (RFC9113 Section 8.2.2) |
| Nginx | 52 | error | dropped | An endpoint MUST NOT generate an HTTP/2 message containing proxy-connection header field (RFC9113 Section 8.2.2) |
| Nginx | 53 | error | dropped | An endpoint MUST NOT generate an HTTP/2 message containing keep-alive header field (RFC9113 Section 8.2.2) |
| Nginx | 54 | error | dropped | An endpoint MUST NOT generate an HTTP/2 message containing transfer-encoding header field (RFC9113 Section 8.2.2) |
| Nginx | 55 | error | dropped | An endpoint MUST NOT generate an HTTP/2 message containing upgrade header field (RFC9113 Section 8.2.2) |
| Nginx | 56 | error | dropped | The TE header field MAY be present in an HTTP/2 request; when it is, it MUST NOT contain any value other than 'trailers'. |
| Nginx | 57 | error | dropped | Pseudo-header fields are not HTTP header fields. Endpoints MUST NOT generate pseudo-header fields other than those defined in this document. |
| Nginx | 59 | error | dropped | Pseudo-header fields defined for responses MUST NOT appear in requests. |
| Nginx | 60 | error | dropped | All pseudo-header fields sent from a client MUST appear in a field block before all regular field lines. Any request or response that contains a pseudo-header field that appears in a field block after a regular field line MUST be treated as malformed (Section 8.1.1). |
| Nginx | 62 | error | dropped | The same pseudo-header field name MUST NOT appear more than once in a field block. A field block for an HTTP request or response that contains a repeated pseudo-header field name MUST be treated as malformed (Section 8.1.1). Tested with a request frame with the same value. |
| Nginx | 63 | error | dropped | The same pseudo-header field name MUST NOT appear more than once in a field block. A field block for an HTTP request or response that contains a repeated pseudo-header field name MUST be treated as malformed (Section 8.1.1). Tested with a request frame with different values. |
| Nginx | 66 | error | dropped | Clients MUST NOT generate a request with a Host header field that differs from the ":authority" pseudo-header field. |
| Nginx | 67 | error | dropped | ':authority' MUST NOT include the deprecated userinfo subcomponent for "http" or "https" schemed URIs. |
| Nginx | 68 | error | dropped | The ":path" pseudo-header field MUST NOT be empty for "http" or "https" URIs; "http" or "https" URIs that do not contain a path component MUST include a value of '/'. |
| Nginx | 69 | error | dropped | All HTTP/2 requests MUST include exactly one valid value for the ":method", ":scheme", and ":path" pseudo-header fields, unless they are CONNECT requests (Section 8.5). An HTTP request that omits mandatory pseudo-header fields is malformed (Section 8.1.1). (Tested with :method missing) |
| Nginx | 70 | error | dropped | All HTTP/2 requests MUST include exactly one valid value for the ":method", ":scheme", and ":path" pseudo-header fields, unless they are CONNECT requests (Section 8.5). An HTTP request that omits mandatory pseudo-header fields is malformed (Section 8.1.1). (Tested with :scheme missing) |
| Nginx | 74 | error | dropped | With the CONNECT method, the ":scheme" and ":path" pseudo-header fields MUST be omitted. (Tested with both present) |
| Nginx | 98 | error | dropped | A field value MUST NOT contain line feed (ASCII LF, 0x0a). (Tested at the middle of the value) |
| Nginx | 99 | error | dropped | A field value MUST NOT contain line feed (ASCII LF, 0x0a). (Tested at the end of the value) |
| Nginx | 100 | error | dropped | A field value MUST NOT contain carriage return (ASCII CR, 0x0d). (Tested at the middle of the value) |
| Nginx | 101 | error | dropped | A field value MUST NOT contain carriage return (ASCII CR, 0x0d). (Tested at the end of the value) |
| Nginx | 103 | error | dropped | All HTTP/2 requests MUST include exactly one valid value for the ":method", ":scheme", and ":path" pseudo-header fields, unless they are CONNECT requests (Section 8.5). An HTTP request that omits mandatory pseudo-header fields is malformed (Section 8.1.1). (Tested with :path missing) |
| Lighttpd | 31 | error | dropped | With the CONNECT method, the " :scheme" and " :path" pseudo-header fields MUST be omitted. (Tested with only :path present) |
| Lighttpd | 32 | error | dropped | With the CONNECT method, the " :scheme" and " :path" pseudo-header fields MUST be omitted. (Tested with only :scheme present) |
| Lighttpd | 40 | error | dropped | Trailers MUST NOT include pseudo-header fields (Section 8.3). |
| Lighttpd | 41 | error | dropped | Field names MUST be converted to lowercase when constructing an HTTP/2 message. |
| Lighttpd | 42 | error | dropped | Field names MUST NOT contain control characters (0x00-0x1F) |
| Lighttpd | 43 | error | dropped | Field names MUST NOT contain ASCII SP (0x20) |
| Lighttpd | 44 | error | dropped | Field names MUST NOT contain DEL character (0x7F) |
| Lighttpd | 45 | error | dropped | Field names MUST NOT contain high byte characters (0x80-0xFF) |
| Lighttpd | 46 | error | dropped | With the exception of pseudo-header fields (Section 8.3), which have a name that starts with a single colon, field names MUST NOT include a colon (ASCII COLON, 0x3a). |
| Lighttpd | 47 | error | dropped | A field value MUST NOT contain line feed (ASCII LF, 0x0a). (Tested at the start of the value) |
| Lighttpd | 48 | error | dropped | A field value MUST NOT contain carriage return (ASCII CR, 0x0d). (Tested at the start of the value) |
| Lighttpd | 49 | error | dropped | A field value MUST NOT start with an ASCII whitespace character (ASCII SP or HTAB, 0x20 or 0x09). |
| Lighttpd | 50 | error | dropped | A field value MUST NOT end with an ASCII whitespace character (ASCII SP or HTAB, 0x20 or 0x09). |
| Lighttpd | 51 | error | dropped | An endpoint MUST NOT generate an HTTP/2 message containing connection header field (RFC9113 Section 8.2.2) |
| Lighttpd | 52 | error | dropped | An endpoint MUST NOT generate an HTTP/2 message containing proxy-connection header field (RFC9113 Section 8.2.2) |
| Lighttpd | 53 | error | dropped | An endpoint MUST NOT generate an HTTP/2 message containing keep-alive header field (RFC9113 Section 8.2.2) |
| Lighttpd | 54 | error | dropped | An endpoint MUST NOT generate an HTTP/2 message containing transfer-encoding header field (RFC9113 Section 8.2.2) |
| Lighttpd | 55 | error | dropped | An endpoint MUST NOT generate an HTTP/2 message containing upgrade header field (RFC9113 Section 8.2.2) |
| Lighttpd | 56 | error | dropped | The TE header field MAY be present in an HTTP/2 request; when it is, it MUST NOT contain any value other than 'trailers'. |
| Lighttpd | 57 | error | dropped | Pseudo-header fields are not HTTP header fields. Endpoints MUST NOT generate pseudo-header fields other than those defined in this document. |
| Lighttpd | 59 | error | dropped | Pseudo-header fields defined for responses MUST NOT appear in requests. |
| Lighttpd | 60 | error | dropped | All pseudo-header fields sent from a client MUST appear in a field block before all regular field lines. Any request or response that contains a pseudo-header field that appears in a field block after a regular field line MUST be treated as malformed (Section 8.1.1). |
| Lighttpd | 62 | error | dropped | The same pseudo-header field name MUST NOT appear more than once in a field block. A field block for an HTTP request or response that contains a repeated pseudo-header field name MUST be treated as malformed (Section 8.1.1). Tested with a request frame with the same value. |
| Lighttpd | 63 | error | dropped | The same pseudo-header field name MUST NOT appear more than once in a field block. A field block for an HTTP request or response that contains a repeated pseudo-header field name MUST be treated as malformed (Section 8.1.1). Tested with a request frame with different values. |
| Lighttpd | 66 | error | dropped | Clients MUST NOT generate a request with a Host header field that differs from the ":authority" pseudo-header field. |
| Lighttpd | 67 | error | dropped | ':authority' MUST NOT include the deprecated userinfo subcomponent for "http" or "https" schemed URIs. |
| Lighttpd | 68 | error | dropped | The ":path" pseudo-header field MUST NOT be empty for "http" or "https" URIs; "http" or "https" URIs that do not contain a path component MUST include a value of '/'. |
| Lighttpd | 69 | error | dropped | All HTTP/2 requests MUST include exactly one valid value for the ":method", ":scheme", and ":path" pseudo-header fields, unless they are CONNECT requests (Section 8.5). An HTTP request that omits mandatory pseudo-header fields is malformed (Section 8.1.1). (Tested with :method missing) |
| Lighttpd | 70 | error | dropped | All HTTP/2 requests MUST include exactly one valid value for the ":method", ":scheme", and ":path" pseudo-header fields, unless they are CONNECT requests (Section 8.5). An HTTP request that omits mandatory pseudo-header fields is malformed (Section 8.1.1). (Tested with :scheme missing) |
| Lighttpd | 74 | error | dropped | With the CONNECT method, the ":scheme" and ":path" pseudo-header fields MUST be omitted. (Tested with both present) |
| Lighttpd | 97 | error | dropped | An endpoint that receives a HEADERS frame without the END_STREAM flag set after receiving the HEADERS frame that opens a request or after receiving a final (non-informational) status code MUST treat the corresponding request or response as malformed (Section 8.1.1). |
| Lighttpd | 98 | error | dropped | A field value MUST NOT contain line feed (ASCII LF, 0x0a). (Tested at the middle of the value) |
| Lighttpd | 99 | error | dropped | A field value MUST NOT contain line feed (ASCII LF, 0x0a). (Tested at the end of the value) |
| Lighttpd | 100 | error | dropped | A field value MUST NOT contain carriage return (ASCII CR, 0x0d). (Tested at the middle of the value) |
| Lighttpd | 101 | error | dropped | A field value MUST NOT contain carriage return (ASCII CR, 0x0d). (Tested at the end of the value) |
| Lighttpd | 102 | error | dropped | Pseudo-header fields MUST NOT appear in a trailer section. |
| Lighttpd | 103 | error | dropped | All HTTP/2 requests MUST include exactly one valid value for the ":method", ":scheme", and ":path" pseudo-header fields, unless they are CONNECT requests (Section 8.5). An HTTP request that omits mandatory pseudo-header fields is malformed (Section 8.1.1). (Tested with :path missing) |
