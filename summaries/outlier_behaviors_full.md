# Outlier Behaviors in HTTP/2 Conformance Tests - Full Scope

This document lists tests where exactly one proxy behaved differently than all others.

Total outliers found: 144

## Outliers for Apache

| Test ID | Description | Outlier Behavior | Common Behavior |
|---------|-------------|------------------|----------------|
| 126 | Trailers MUST NOT include pseudo-header fields (Section 8.3). | goaway | dropped |
| 152 | If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the closed state.) | goaway | dropped |

## Outliers for Caddy

| Test ID | Description | Outlier Behavior | Common Behavior |
|---------|-------------|------------------|----------------|
| 4 | Client preface must include a SETTINGS frame | 500 | goaway |
| 8 | Values greater than 16,384 MUST NOT be sent unless receiver has set larger SETTINGS_MAX_FRAME_SIZE | 500 | goaway |
| 87 | A SETTINGS frame MUST be sent by both endpoints at the start of a connection and MAY be sent at any other time by either endpoint over the lifetime of the connection. (Tested from the client side.) | 500 | goaway |
| 142 | The TE header field MAY be present in an HTTP/2 request; when it is, it MUST NOT contain any value other than 'trailers'. | modified | 500 |

## Outliers for Cloudflare

| Test ID | Description | Outlier Behavior | Common Behavior |
|---------|-------------|------------------|----------------|
| 2 | Client must send connection preface after TLS establishment | dropped | 500 |
| 123 | An endpoint MUST treat a change to SETTINGS_INITIAL_WINDOW_SIZE that causes any flow-control window to exceed the maximum size as a connection error (Section 5.4.1) of type FLOW_CONTROL_ERROR. | 500 | goaway |
| 156 | The sender MUST NOT send a flow-controlled frame with a length that exceeds the space available in either of the flow-control windows advertised by the receiver. | reset | dropped |

## Outliers for H2O

| Test ID | Description | Outlier Behavior | Common Behavior |
|---------|-------------|------------------|----------------|
| 110 | A reserved 1-bit field. The semantics of this bit are undefined, and the bit MUST remain unset (0x00) when sending and MUST be ignored when receiving. (server side) | dropped | unmodified |
| 135 | A field value MUST NOT start with an ASCII whitespace character (ASCII SP or HTAB, 0x20 or 0x09). | dropped | unmodified |
| 136 | A field value MUST NOT end with an ASCII whitespace character (ASCII SP or HTAB, 0x20 or 0x09). | dropped | unmodified |
| 151 | If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the half-closed (remote) state.) | dropped | unmodified |

## Outliers for Mitmproxy

| Test ID | Description | Outlier Behavior | Common Behavior |
|---------|-------------|------------------|----------------|
| 1 | Receiving any frame other than HEADERS or PRIORITY on a stream in this (idle) state MUST be treated as a connection error (Section 5.4.1) of type PROTOCOL_ERROR. | unmodified | goaway |
| 3 | the connection preface starts with the string: PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n | unmodified | dropped |
| 5 | If this stream (initially in the idle state) is initiated by the server, as described in Section 5.1.1, then receiving a HEADERS frame MUST also be treated as a connection error (Section 5.4.1) of type PROTOCOL_ERROR. | unmodified | goaway |
| 6 | An endpoint MUST NOT send any type of frame other than HEADERS, RST_STREAM, or PRIORITY in the reserved (local) state. | unmodified | 500 |
| 7 | If an endpoint receives additional frames, other than WINDOW_UPDATE, PRIORITY, or RST_STREAM, for a stream that is in the half-closed (remote) state, it MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. | unmodified | goaway |
| 10 | A reserved 1-bit field. The semantics of this bit are undefined, and the bit MUST remain unset (0x00) when sending and MUST be ignored when receiving. | unmodified | dropped |
| 11 | Streams initiated by a client MUST use odd-numbered stream identifiers. | unmodified | goaway |
| 12 | Streams initiated by a server MUST use even-numbered stream identifiers. | unmodified | goaway |
| 13 | The identifier of a newly established stream MUST be numerically greater than all streams that the initiating endpoint has opened or reserved. | unmodified | dropped |
| 15 | If a PRIORITY frame is received with a stream identifier of 0x00, the recipient MUST respond with a connection error of type PROTOCOL_ERROR | unmodified | goaway |
| 17 | If a RST_STREAM frame is received with a stream identifier of 0x00, the recipient MUST treat this as a connection error (Section 5.4.1) of type PROTOCOL_ERROR. | reset | goaway |
| 20 | The stream identifier for a SETTINGS frame MUST be zero (0x00). | unmodified | goaway |
| 21 | A SETTINGS frame with a length other than a multiple of 6 octets MUST be treated as a connection error (Section 5.4.1) of type FRAME_SIZE_ERROR. | unmodified | goaway |
| 22 | The initial value of SETTINGS_ENABLE_PUSH is 1. Any value other than 0 or 1 MUST be treated as a connection error (Section 5.4.1) of type PROTOCOL_ERROR. | unmodified | goaway |
| 23 | A server MUST NOT explicitly set this value (SETTINGS_ENABLE_PUSH) to 1. A server MAY choose to omit this setting (SETTINGS_ENABLE_PUSH) when it sends a SETTINGS frame, but if a server does include a value, it MUST be 0. | unmodified | goaway |
| 24 | A server MUST NOT send a PUSH_PROMISE frame if it receives the SETTINGS_ENABLE_PUSH (0x02) parameter set to a value of 0. | unmodified | 500 |
| 25 | For SETTINGS_INITIAL_WINDOW_SIZE, values above the maximum flow-control window size of 2^31-1 (2147483647) MUST be treated as a connection error (Section 5.4.1) of type FLOW_CONTROL_ERROR. | unmodified | goaway |
| 26 | The value advertised by an endpoint MUST be between initial value (2^14 = 16,384) and maximum allowed frame size (2^24-1 = 16,777,215 octets), inclusive. | unmodified | goaway |
| 27 | An endpoint that receives a SETTINGS frame with any unknown or unsupported identifier MUST ignore that setting. | unmodified | dropped |
| 28 | If the Stream Identifier field of a PUSH_PROMISE frame specifies the value 0x00, a recipient MUST respond with a connection error (Section 5.4.1) of type PROTOCOL_ERROR. | unmodified | goaway |
| 29 | The promised stream identifier MUST be a valid choice for the next stream sent by the sender (see 'new stream identifier' in Section 5.1.1). (Using Odd-numbered Stream ID (Invalid for Server)) | unmodified | goaway |
| 30 | If a PING frame is received with a Stream Identifier field value other than 0x00, the recipient MUST respond with a connection error (Section 5.4.1) of type PROTOCOL_ERROR. | unmodified | goaway |
| 31 | With the CONNECT method, the " :scheme" and " :path" pseudo-header fields MUST be omitted. (Tested with only :path present) | unmodified | dropped |
| 32 | With the CONNECT method, the " :scheme" and " :path" pseudo-header fields MUST be omitted. (Tested with only :scheme present) | unmodified | dropped |
| 35 | An endpoint MUST treat a change to SETTINGS_INITIAL_WINDOW_SIZE that causes any flow-control window to exceed the maximum size as a connection error (Section 5.4.1) of type FLOW_CONTROL_ERROR. | unmodified | goaway |
| 36 | If a CONTINUATION frame is received with a Stream Identifier field of 0x00, the recipient MUST respond with a connection error (Section 5.4.1) of type PROTOCOL_ERROR. | unmodified | goaway |
| 37 | A CONTINUATION frame MUST be preceded by a HEADERS, PUSH_PROMISE or CONTINUATION frame without the END_HEADERS flag set. (Using HEADERS frame with END_HEADERS flag set) | unmodified | goaway |
| 38 | A CONTINUATION frame MUST be preceded by a HEADERS, PUSH_PROMISE or CONTINUATION frame without the END_HEADERS flag set. (Using PUSH_PROMISE frame with END_HEADERS flag set) | unmodified | 500 |
| 39 | The header fields in PUSH_PROMISE and any subsequent CONTINUATION frames MUST be a valid and complete set of request header fields. | unmodified | 500 |
| 40 | Trailers MUST NOT include pseudo-header fields (Section 8.3). | unmodified | dropped |
| 41 | Field names MUST be converted to lowercase when constructing an HTTP/2 message. | unmodified | dropped |
| 42 | Field names MUST NOT contain control characters (0x00-0x1F) | unmodified | dropped |
| 43 | Field names MUST NOT contain ASCII SP (0x20) | unmodified | dropped |
| 44 | Field names MUST NOT contain DEL character (0x7F) | unmodified | dropped |
| 45 | Field names MUST NOT contain high byte characters (0x80-0xFF) | unmodified | dropped |
| 46 | With the exception of pseudo-header fields (Section 8.3), which have a name that starts with a single colon, field names MUST NOT include a colon (ASCII COLON, 0x3a). | unmodified | dropped |
| 47 | A field value MUST NOT contain line feed (ASCII LF, 0x0a). (Tested at the start of the value) | unmodified | dropped |
| 48 | A field value MUST NOT contain carriage return (ASCII CR, 0x0d). (Tested at the start of the value) | unmodified | dropped |
| 49 | A field value MUST NOT start with an ASCII whitespace character (ASCII SP or HTAB, 0x20 or 0x09). | unmodified | dropped |
| 50 | A field value MUST NOT end with an ASCII whitespace character (ASCII SP or HTAB, 0x20 or 0x09). | unmodified | dropped |
| 51 | An endpoint MUST NOT generate an HTTP/2 message containing connection header field (RFC9113 Section 8.2.2) | unmodified | dropped |
| 52 | An endpoint MUST NOT generate an HTTP/2 message containing proxy-connection header field (RFC9113 Section 8.2.2) | unmodified | dropped |
| 53 | An endpoint MUST NOT generate an HTTP/2 message containing keep-alive header field (RFC9113 Section 8.2.2) | unmodified | dropped |
| 54 | An endpoint MUST NOT generate an HTTP/2 message containing transfer-encoding header field (RFC9113 Section 8.2.2) | unmodified | dropped |
| 55 | An endpoint MUST NOT generate an HTTP/2 message containing upgrade header field (RFC9113 Section 8.2.2) | unmodified | dropped |
| 56 | The TE header field MAY be present in an HTTP/2 request; when it is, it MUST NOT contain any value other than 'trailers'. | unmodified | dropped |
| 57 | Pseudo-header fields are not HTTP header fields. Endpoints MUST NOT generate pseudo-header fields other than those defined in this document. | unmodified | dropped |
| 58 | Pseudo-header fields defined for requests MUST NOT appear in responses. | unmodified | 500 |
| 59 | Pseudo-header fields defined for responses MUST NOT appear in requests. | unmodified | dropped |
| 60 | All pseudo-header fields sent from a client MUST appear in a field block before all regular field lines. Any request or response that contains a pseudo-header field that appears in a field block after a regular field line MUST be treated as malformed (Section 8.1.1). | unmodified | dropped |
| 61 | All pseudo-header fields sent from a server MUST appear in a field block before all regular field lines. Any request or response that contains a pseudo-header field that appears in a field block after a regular field line MUST be treated as malformed (Section 8.1.1). | unmodified | 500 |
| 62 | The same pseudo-header field name MUST NOT appear more than once in a field block. A field block for an HTTP request or response that contains a repeated pseudo-header field name MUST be treated as malformed (Section 8.1.1). Tested with a request frame with the same value. | unmodified | dropped |
| 63 | The same pseudo-header field name MUST NOT appear more than once in a field block. A field block for an HTTP request or response that contains a repeated pseudo-header field name MUST be treated as malformed (Section 8.1.1). Tested with a request frame with different values. | unmodified | dropped |
| 64 | The same pseudo-header field name MUST NOT appear more than once in a field block. A field block for an HTTP request or response that contains a repeated pseudo-header field name MUST be treated as malformed (Section 8.1.1). Tested with a response frame with the same value. | unmodified | 500 |
| 65 | The same pseudo-header field name MUST NOT appear more than once in a field block. A field block for an HTTP request or response that contains a repeated pseudo-header field name MUST be treated as malformed (Section 8.1.1). Tested with a response frame with different values. | unmodified | 500 |
| 66 | Clients MUST NOT generate a request with a Host header field that differs from the ":authority" pseudo-header field. | unmodified | dropped |
| 67 | ':authority' MUST NOT include the deprecated userinfo subcomponent for "http" or "https" schemed URIs. | unmodified | dropped |
| 68 | The ":path" pseudo-header field MUST NOT be empty for "http" or "https" URIs; "http" or "https" URIs that do not contain a path component MUST include a value of '/'. | unmodified | dropped |
| 69 | All HTTP/2 requests MUST include exactly one valid value for the ":method", ":scheme", and ":path" pseudo-header fields, unless they are CONNECT requests (Section 8.5). An HTTP request that omits mandatory pseudo-header fields is malformed (Section 8.1.1). (Tested with :method missing) | unmodified | dropped |
| 70 | All HTTP/2 requests MUST include exactly one valid value for the ":method", ":scheme", and ":path" pseudo-header fields, unless they are CONNECT requests (Section 8.5). An HTTP request that omits mandatory pseudo-header fields is malformed (Section 8.1.1). (Tested with :scheme missing) | unmodified | dropped |
| 71 | For HTTP/2 responses, a single ":status" pseudo-header field is defined that carries the HTTP status code field. This pseudo-header field MUST be included in all responses, including interim responses; otherwise, the response is malformed. | unmodified | 500 |
| 72 | A client cannot push. Thus, servers MUST treat the receipt of a PUSH_PROMISE frame as a connection error (Section 5.4.1) of type PROTOCOL_ERROR. | unmodified | goaway |
| 73 | In the PUSH_PROMISE frame, the server MUST include a method in the ":method" pseudo-header field that is safe and cacheable. | unmodified | 500 |
| 74 | With the CONNECT method, the ":scheme" and ":path" pseudo-header fields MUST be omitted. (Tested with both present) | unmodified | dropped |
| 75 | With the CONNECT method, The ":authority" pseudo-header field contains the host and port to connect to | unmodified | dropped |
| 80 | DATA frames MUST be associated with a stream. | unmodified | goaway |
| 81 | If a DATA frame is received whose Stream Identifier field is 0x00, the recipient MUST respond with a connection error (Section 5.4.1) of type PROTOCOL_ERROR. | unmodified | goaway |
| 82 | If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the idle state.) | unmodified | goaway |
| 83 | If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the half-closed (remote) state.) | unmodified | goaway |
| 85 | A HEADERS frame without the END_HEADERS flag set MUST be followed by a CONTINUATION frame for the same stream. | unmodified | goaway |
| 86 | If a HEADERS frame is received whose Stream Identifier field is 0x00, the recipient MUST respond with a connection error (Section 5.4.1) of type PROTOCOL_ERROR. | unmodified | goaway |
| 88 | Unsupported settings MUST be ignored. | unmodified | dropped |
| 89 | The promised stream identifier MUST be a valid choice for the next stream sent by the sender (see 'new stream identifier' in Section 5.1.1). (Using Already Used Stream ID) | unmodified | 500 |
| 90 | The promised stream identifier MUST be a valid choice for the next stream sent by the sender (see 'new stream identifier' in Section 5.1.1). (Using Lower Stream ID) | unmodified | 500 |
| 91 | A PUSH_PROMISE frame without the END_HEADERS flag set MUST be followed by a CONTINUATION frame for the same stream. | unmodified | 500 |
| 92 | PUSH_PROMISE MUST NOT be sent if the SETTINGS_ENABLE_PUSH setting of the peer endpoint is set to 0. | unmodified | 500 |
| 94 | CONTINUATION frames MUST be associated with a stream. | unmodified | goaway |
| 95 | If the END_HEADERS flag is not set, this frame MUST be followed by another CONTINUATION frame. A receiver MUST treat the receipt of any other type of frame or a frame on a different stream as a connection error (Section 5.4.1) of type PROTOCOL_ERROR. | unmodified | goaway |
| 96 | Other frames (from any stream) MUST NOT occur between the HEADERS frame and any CONTINUATION frames that might follow. | unmodified | goaway |
| 97 | An endpoint that receives a HEADERS frame without the END_STREAM flag set after receiving the HEADERS frame that opens a request or after receiving a final (non-informational) status code MUST treat the corresponding request or response as malformed (Section 8.1.1). | unmodified | dropped |
| 98 | A field value MUST NOT contain line feed (ASCII LF, 0x0a). (Tested at the middle of the value) | unmodified | dropped |
| 99 | A field value MUST NOT contain line feed (ASCII LF, 0x0a). (Tested at the end of the value) | unmodified | dropped |
| 100 | A field value MUST NOT contain carriage return (ASCII CR, 0x0d). (Tested at the middle of the value) | unmodified | dropped |
| 101 | A field value MUST NOT contain carriage return (ASCII CR, 0x0d). (Tested at the end of the value) | unmodified | dropped |
| 102 | Pseudo-header fields MUST NOT appear in a trailer section. | unmodified | dropped |
| 103 | All HTTP/2 requests MUST include exactly one valid value for the ":method", ":scheme", and ":path" pseudo-header fields, unless they are CONNECT requests (Section 8.5). An HTTP request that omits mandatory pseudo-header fields is malformed (Section 8.1.1). (Tested with :path missing) | unmodified | dropped |
| 104 | Promised requests MUST be safe (see Section 9.2.1 of [HTTP]) and cacheable (see Section 9.2.3 of [HTTP]). | unmodified | 500 |
| 105 | PUSH_PROMISE frames MUST NOT be sent by the client. | unmodified | goaway |
| 106 | Receiving any frame other than HEADERS or PRIORITY on a stream in this (idle) state MUST be treated as a connection error (Section 5.4.1) of type PROTOCOL_ERROR. (server side) | unmodified | goaway |
| 107 | If an endpoint receives additional frames, other than WINDOW_UPDATE, PRIORITY, or RST_STREAM, for a stream that is in the half-closed (remote) state, it MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (server side) | unmodified | goaway |
| 108 | Values greater than 16,384 MUST NOT be sent unless receiver has set larger SETTINGS_MAX_FRAME_SIZE. (server side) | unmodified | goaway |
| 111 | If a PRIORITY frame is received with a stream identifier of 0x00, the recipient MUST respond with a connection error of type PROTOCOL_ERROR. (server side) | unmodified | goaway |
| 112 | If a RST_STREAM frame is received with a stream identifier of 0x00, the recipient MUST treat this as a connection error (Section 5.4.1) of type PROTOCOL_ERROR. (server side) | reset | goaway |
| 115 | The stream identifier for a SETTINGS frame MUST be zero (0x00). | unmodified | goaway |
| 116 | A SETTINGS frame with a length other than a multiple of 6 octets MUST be treated as a connection error (Section 5.4.1) of type FRAME_SIZE_ERROR. | unmodified | goaway |
| 118 | The value advertised by an endpoint MUST be between initial value (2^14 = 16,384) and maximum allowed frame size (2^24-1 = 16,777,215 octets), inclusive. | unmodified | goaway |
| 119 | An endpoint that receives a SETTINGS frame with any unknown or unsupported identifier MUST ignore that setting. | unmodified | 500 |
| 120 | If a PING frame is received with a Stream Identifier field value other than 0x00, the recipient MUST respond with a connection error (Section 5.4.1) of type PROTOCOL_ERROR. | unmodified | goaway |
| 121 | A receiver MUST treat the receipt of a WINDOW_UPDATE frame with a flow-control window increment of 0 as a stream error (Section 5.4.2) of type PROTOCOL_ERROR. | dropped | goaway |
| 124 | If a CONTINUATION frame is received with a Stream Identifier field of 0x00, the recipient MUST respond with a connection error (Section 5.4.1) of type PROTOCOL_ERROR. | unmodified | goaway |
| 125 | A CONTINUATION frame MUST be preceded by a HEADERS, PUSH_PROMISE or CONTINUATION frame without the END_HEADERS flag set. (Using HEADERS frame with END_HEADERS flag set) | unmodified | goaway |
| 127 | Field names MUST be converted to lowercase when constructing an HTTP/2 message. | unmodified | 500 |
| 128 | Field names MUST NOT contain control characters (0x00-0x1F) | unmodified | 500 |
| 129 | Field names MUST NOT contain ASCII SP (0x20) | unmodified | 500 |
| 130 | Field names MUST NOT contain DEL character (0x7F) | unmodified | 500 |
| 131 | Field names MUST NOT contain high byte characters (0x80-0xFF) | unmodified | 500 |
| 132 | With the exception of pseudo-header fields (Section 8.3), which have a name that starts with a single colon, field names MUST NOT include a colon (ASCII COLON, 0x3a). | unmodified | 500 |
| 133 | A field value MUST NOT contain line feed (ASCII LF, 0x0a). (Tested at the start of the value) | unmodified | 500 |
| 134 | A field value MUST NOT contain carriage return (ASCII CR, 0x0d). (Tested at the start of the value) | unmodified | 500 |
| 137 | An endpoint MUST NOT generate an HTTP/2 message containing connection header field (RFC9113 Section 8.2.2) | unmodified | 500 |
| 138 | An endpoint MUST NOT generate an HTTP/2 message containing proxy-connection header field (RFC9113 Section 8.2.2) | unmodified | 500 |
| 139 | An endpoint MUST NOT generate an HTTP/2 message containing keep-alive header field (RFC9113 Section 8.2.2) | unmodified | 500 |
| 140 | An endpoint MUST NOT generate an HTTP/2 message containing transfer-encoding header field (RFC9113 Section 8.2.2) | unmodified | 500 |
| 141 | An endpoint MUST NOT generate an HTTP/2 message containing upgrade header field (RFC9113 Section 8.2.2) | unmodified | 500 |
| 143 | Pseudo-header fields are not HTTP header fields. Endpoints MUST NOT generate pseudo-header fields other than those defined in this document. | unmodified | 500 |
| 145 | RST_STREAM frames MUST NOT be sent for a stream in the 'idle' state. | reset | goaway |
| 146 | RST_STREAM frames MUST be associated with a stream. | reset | goaway |
| 148 | DATA frames MUST be associated with a stream. | unmodified | goaway |
| 149 | If a DATA frame is received whose Stream Identifier field is 0x00, the recipient MUST respond with a connection error (Section 5.4.1) of type PROTOCOL_ERROR. | unmodified | goaway |
| 150 | If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the idle state.) | unmodified | goaway |
| 153 | A HEADERS frame without the END_HEADERS flag set MUST be followed by a CONTINUATION frame for the same stream. | unmodified | goaway |
| 154 | If a HEADERS frame is received whose Stream Identifier field is 0x00, the recipient MUST respond with a connection error (Section 5.4.1) of type PROTOCOL_ERROR. | unmodified | goaway |
| 155 | Unsupported settings MUST be ignored. | unmodified | 500 |
| 157 | CONTINUATION frames MUST be associated with a stream. | unmodified | goaway |
| 158 | If the END_HEADERS flag is not set, this frame MUST be followed by another CONTINUATION frame. A receiver MUST treat the receipt of any other type of frame or a frame on a different stream as a connection error (Section 5.4.1) of type PROTOCOL_ERROR. | unmodified | goaway |
| 159 | Other frames (from any stream) MUST NOT occur between the HEADERS frame and any CONTINUATION frames that might follow. | unmodified | goaway |
| 160 | An endpoint that receives a HEADERS frame without the END_STREAM flag set after receiving the HEADERS frame that opens a request or after receiving a final (non-informational) status code MUST treat the corresponding request or response as malformed (Section 8.1.1). | unmodified | dropped |
| 161 | A field value MUST NOT contain line feed (ASCII LF, 0x0a). (Tested at the middle of the value) | unmodified | 500 |
| 162 | A field value MUST NOT contain line feed (ASCII LF, 0x0a). (Tested at the end of the value) | unmodified | 500 |
| 163 | A field value MUST NOT contain carriage return (ASCII CR, 0x0d). (Tested at the middle of the value) | unmodified | 500 |
| 164 | A field value MUST NOT contain carriage return (ASCII CR, 0x0d). (Tested at the end of the value) | unmodified | 500 |

