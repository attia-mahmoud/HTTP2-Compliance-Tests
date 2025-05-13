Test Outcomes by Test ID

Test #2 the connection preface starts with the string: PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n
Received unmodified: Mitmproxy-11.1.0

Test #3 Client preface must include a SETTINGS frame
Received: Azure-AG, Lighttpd-1.4.76, Nginx-1.26.0, Varnish-7.7.0
Received modified: Cloudflare
Received unmodified: Mitmproxy-11.1.0

Test #4 Values greater than 16,384 MUST NOT be sent unless receiver has set larger SETTINGS_MAX_FRAME_SIZE
Received: Azure-AG, Nginx-1.26.0
Received unmodified: Mitmproxy-11.1.0

Test #6 A reserved 1-bit field. The semantics of this bit are undefined, and the bit MUST remain unset (0x00) when sending and MUST be ignored when receiving.
Received unmodified: Apache-2.4.62, Caddy-2.9.1, Envoy-1.32.2, HAproxy-2.9.10, Nghttpx-1.62.1, Node-20.16.0

Test #7 Receiving any frame other than HEADERS or PRIORITY on a stream in this (idle) state MUST be treated as a connection error (Section 5.4.1) of type PROTOCOL_ERROR.
Received unmodified: Mitmproxy-11.1.0

Test #8 If an endpoint receives additional frames, other than WINDOW_UPDATE, PRIORITY, or RST_STREAM, for a stream that is in the half-closed (remote) state, it MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED.
Received: Lighttpd-1.4.76
Received unmodified: Mitmproxy-11.1.0

Test #10 Streams initiated by a client MUST use odd-numbered stream identifiers.
Received unmodified: Mitmproxy-11.1.0

Test #11 The identifier of a newly established stream MUST be numerically greater than all streams that the initiating endpoint has opened or reserved.
Received unmodified: Mitmproxy-11.1.0

Test #12 DATA frames MUST be associated with a stream.
Received unmodified: Mitmproxy-11.1.0

Test #13 If a DATA frame is received whose Stream Identifier field is 0x00, the recipient MUST respond with a connection error (Section 5.4.1) of type PROTOCOL_ERROR.
Received unmodified: Mitmproxy-11.1.0

Test #14 If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the idle state.)
Received unmodified: Mitmproxy-11.1.0

Test #15 If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the half-closed (remote) state.)
Received: Lighttpd-1.4.76
Received unmodified: Mitmproxy-11.1.0

Test #17 A HEADERS frame without the END_HEADERS flag set MUST be followed by a CONTINUATION frame for the same stream.
Received unmodified: Mitmproxy-11.1.0

Test #18 If a HEADERS frame is received whose Stream Identifier field is 0x00, the recipient MUST respond with a connection error (Section 5.4.1) of type PROTOCOL_ERROR.
Received unmodified: Mitmproxy-11.1.0

Test #19 If a PRIORITY frame is received with a stream identifier of 0x00, the recipient MUST respond with a connection error of type PROTOCOL_ERROR
Received unmodified: Mitmproxy-11.1.0

Test #25 The stream identifier for a SETTINGS frame MUST be zero (0x00).
Received unmodified: Mitmproxy-11.1.0

Test #26 A SETTINGS frame with a length other than a multiple of 6 octets MUST be treated as a connection error (Section 5.4.1) of type FRAME_SIZE_ERROR.
Received unmodified: Mitmproxy-11.1.0

Test #27 The initial value of SETTINGS_ENABLE_PUSH is 1. Any value other than 0 or 1 MUST be treated as a connection error (Section 5.4.1) of type PROTOCOL_ERROR.
Received unmodified: Mitmproxy-11.1.0

Test #28 For SETTINGS_INITIAL_WINDOW_SIZE, values above the maximum flow-control window size of 2^31-1 (2147483647) MUST be treated as a connection error (Section 5.4.1) of type FLOW_CONTROL_ERROR.
Received unmodified: Mitmproxy-11.1.0

Test #29 The value advertised by an endpoint MUST be between initial value (2^14 = 16,384) and maximum allowed frame size (2^24-1 = 16,777,215 octets), inclusive.
Received unmodified: Mitmproxy-11.1.0

Test #30 An endpoint that receives a SETTINGS frame with any unknown or unsupported identifier MUST ignore that setting.
Received unmodified: Mitmproxy-11.1.0

Test #31 Unsupported settings MUST be ignored.
Received unmodified: Mitmproxy-11.1.0

Test #32 If a PING frame is received with a Stream Identifier field value other than 0x00, the recipient MUST respond with a connection error (Section 5.4.1) of type PROTOCOL_ERROR.
Received unmodified: Mitmproxy-11.1.0

Test #36 If a CONTINUATION frame is received with a Stream Identifier field of 0x00, the recipient MUST respond with a connection error (Section 5.4.1) of type PROTOCOL_ERROR.
Received unmodified: Mitmproxy-11.1.0

Test #37 A CONTINUATION frame MUST be preceded by a HEADERS, PUSH_PROMISE or CONTINUATION frame without the END_HEADERS flag set. (Using HEADERS frame with END_HEADERS flag set)
Received unmodified: Mitmproxy-11.1.0

Test #38 CONTINUATION frames MUST be associated with a stream.
Received unmodified: Mitmproxy-11.1.0

Test #39 If the END_HEADERS flag is not set, this frame MUST be followed by another CONTINUATION frame. A receiver MUST treat the receipt of any other type of frame or a frame on a different stream as a connection error (Section 5.4.1) of type PROTOCOL_ERROR.
Received unmodified: Mitmproxy-11.1.0

Test #40 Trailers MUST NOT include pseudo-header fields (Section 8.3).
Received: Varnish-7.7.0
Received unmodified: Mitmproxy-11.1.0

Test #41 Other frames (from any stream) MUST NOT occur between the HEADERS frame and any CONTINUATION frames that might follow.
Received unmodified: Mitmproxy-11.1.0

Test #42 An endpoint that receives a HEADERS frame without the END_STREAM flag set after receiving the HEADERS frame that opens a request or after receiving a final (non-informational) status code MUST treat the corresponding request or response as malformed (Section 8.1.1).
Received unmodified: Mitmproxy-11.1.0

Test #43 Field names MUST be converted to lowercase when constructing an HTTP/2 message.
Received unmodified: Mitmproxy-11.1.0

Test #44 Field names MUST NOT contain control characters (0x00-0x1F)
Received unmodified: Mitmproxy-11.1.0

Test #45 Field names MUST NOT contain ASCII SP (0x20)
Received unmodified: Mitmproxy-11.1.0

Test #46 Field names MUST NOT contain DEL character (0x7F)
Received unmodified: Mitmproxy-11.1.0

Test #47 Field names MUST NOT contain high byte characters (0x80-0xFF)
Received unmodified: Mitmproxy-11.1.0

Test #48 With the exception of pseudo-header fields (Section 8.3), which have a name that starts with a single colon, field names MUST NOT include a colon (ASCII COLON, 0x3a).
Received unmodified: Mitmproxy-11.1.0

Test #49 A field value MUST NOT contain line feed (ASCII LF, 0x0a). (Tested at the start of the value)
Received unmodified: Mitmproxy-11.1.0

Test #50 A field value MUST NOT contain carriage return (ASCII CR, 0x0d). (Tested at the start of the value)
Received unmodified: Mitmproxy-11.1.0

Test #51 A field value MUST NOT start with an ASCII whitespace character (ASCII SP or HTAB, 0x20 or 0x09).
Received unmodified: Envoy-1.32.2, HAproxy-2.9.10, Mitmproxy-11.1.0

Test #52 A field value MUST NOT end with an ASCII whitespace character (ASCII SP or HTAB, 0x20 or 0x09).
Received unmodified: Envoy-1.32.2, HAproxy-2.9.10, Mitmproxy-11.1.0

Test #53 A field value MUST NOT contain line feed (ASCII LF, 0x0a). (Tested at the middle of the value)
Received unmodified: Mitmproxy-11.1.0

Test #54 A field value MUST NOT contain line feed (ASCII LF, 0x0a). (Tested at the end of the value)
Received unmodified: Mitmproxy-11.1.0

Test #55 A field value MUST NOT contain carriage return (ASCII CR, 0x0d). (Tested at the middle of the value)
Received unmodified: Mitmproxy-11.1.0

Test #56 A field value MUST NOT contain carriage return (ASCII CR, 0x0d). (Tested at the end of the value)
Received unmodified: Mitmproxy-11.1.0

Test #57 An endpoint MUST NOT generate an HTTP/2 message containing connection header field (RFC9113 Section 8.2.2)
Received: Varnish-7.7.0
Received unmodified: Mitmproxy-11.1.0

Test #58 An endpoint MUST NOT generate an HTTP/2 message containing proxy-connection header field (RFC9113 Section 8.2.2)
Received: Varnish-7.7.0
Received unmodified: Mitmproxy-11.1.0

Test #59 An endpoint MUST NOT generate an HTTP/2 message containing keep-alive header field (RFC9113 Section 8.2.2)
Received: Varnish-7.7.0
Received unmodified: Mitmproxy-11.1.0

Test #60 An endpoint MUST NOT generate an HTTP/2 message containing transfer-encoding header field (RFC9113 Section 8.2.2)
Received: Varnish-7.7.0
Received unmodified: Mitmproxy-11.1.0

Test #61 An endpoint MUST NOT generate an HTTP/2 message containing upgrade header field (RFC9113 Section 8.2.2)
Received: Varnish-7.7.0
Received unmodified: Mitmproxy-11.1.0

Test #62 The TE header field MAY be present in an HTTP/2 request; when it is, it MUST NOT contain any value other than 'trailers'.
Received: Varnish-7.7.0
Received unmodified: Mitmproxy-11.1.0

Test #63 Pseudo-header fields are not HTTP header fields. Endpoints MUST NOT generate pseudo-header fields other than those defined in this document.
Received unmodified: Mitmproxy-11.1.0

Test #64 Pseudo-header fields defined for responses MUST NOT appear in requests.
Received unmodified: Mitmproxy-11.1.0

Test #65 All pseudo-header fields sent from a client MUST appear in a field block before all regular field lines. Any request or response that contains a pseudo-header field that appears in a field block after a regular field line MUST be treated as malformed (Section 8.1.1).
Received: Varnish-7.7.0
Received unmodified: Mitmproxy-11.1.0

Test #66 The same pseudo-header field name MUST NOT appear more than once in a field block. A field block for an HTTP request or response that contains a repeated pseudo-header field name MUST be treated as malformed (Section 8.1.1). Tested with a request frame with the same value.
Received unmodified: Mitmproxy-11.1.0

Test #67 The same pseudo-header field name MUST NOT appear more than once in a field block. A field block for an HTTP request or response that contains a repeated pseudo-header field name MUST be treated as malformed (Section 8.1.1). Tested with a request frame with different values.
Received unmodified: Mitmproxy-11.1.0

Test #68 Clients MUST NOT generate a request with a Host header field that differs from the ":authority" pseudo-header field.
Received modified: HAproxy-2.9.10, Nghttpx-1.62.1
Received unmodified: Mitmproxy-11.1.0

Test #69 ':authority' MUST NOT include the deprecated userinfo subcomponent for "http" or "https" schemed URIs.
Received: Varnish-7.7.0
Received unmodified: HAproxy-2.9.10, Mitmproxy-11.1.0, Nghttpx-1.62.1

Test #70 The ":path" pseudo-header field MUST NOT be empty for "http" or "https" URIs; "http" or "https" URIs that do not contain a path component MUST include a value of '/'.
Received unmodified: Mitmproxy-11.1.0

Test #71 All HTTP/2 requests MUST include exactly one valid value for the ":method", ":scheme", and ":path" pseudo-header fields, unless they are CONNECT requests (Section 8.5). An HTTP request that omits mandatory pseudo-header fields is malformed (Section 8.1.1). (Tested with :method missing)
Received unmodified: Mitmproxy-11.1.0

Test #72 All HTTP/2 requests MUST include exactly one valid value for the ":method", ":scheme", and ":path" pseudo-header fields, unless they are CONNECT requests (Section 8.5). An HTTP request that omits mandatory pseudo-header fields is malformed (Section 8.1.1). (Tested with :scheme missing)
Received unmodified: Mitmproxy-11.1.0

Test #73 All HTTP/2 requests MUST include exactly one valid value for the ":method", ":scheme", and ":path" pseudo-header fields, unless they are CONNECT requests (Section 8.5). An HTTP request that omits mandatory pseudo-header fields is malformed (Section 8.1.1). (Tested with :path missing)
Received unmodified: Mitmproxy-11.1.0

Test #74 A client cannot push. Thus, servers MUST treat the receipt of a PUSH_PROMISE frame as a connection error (Section 5.4.1) of type PROTOCOL_ERROR.
Received unmodified: Mitmproxy-11.1.0

Test #75 With the CONNECT method, the " :scheme" and " :path" pseudo-header fields MUST be omitted. (Tested with only :path present)
Received unmodified: Mitmproxy-11.1.0

Test #76 With the CONNECT method, the " :scheme" and " :path" pseudo-header fields MUST be omitted. (Tested with only :scheme present)
Received unmodified: Mitmproxy-11.1.0

Test #77 With the CONNECT method, the ":scheme" and ":path" pseudo-header fields MUST be omitted. (Tested with both present)
Received unmodified: Mitmproxy-11.1.0

Test #78 With the CONNECT method, The ":authority" pseudo-header field contains the host and port to connect to
Received modified: H2O-26b116e95
Received unmodified: Mitmproxy-11.1.0, Nghttpx-1.62.1

Test #79 Values greater than 16,384 MUST NOT be sent unless receiver has set larger SETTINGS_MAX_FRAME_SIZE. (server side)
Received unmodified: Mitmproxy-11.1.0

Test #81 A reserved 1-bit field. The semantics of this bit are undefined, and the bit MUST remain unset (0x00) when sending and MUST be ignored when receiving. (server side)
Received unmodified: Caddy-2.9.1, Cloudflare, HAproxy-2.9.10, Mitmproxy-11.1.0, Nghttpx-1.62.1

Test #82 If this stream (initially in the idle state) is initiated by the server, as described in Section 5.1.1, then receiving a HEADERS frame MUST also be treated as a connection error (Section 5.4.1) of type PROTOCOL_ERROR.  (server side)
Received unmodified: Mitmproxy-11.1.0

Test #83 An endpoint MUST NOT send any type of frame other than HEADERS, RST_STREAM, or PRIORITY in the reserved (local) state. (server side)
Received unmodified: Mitmproxy-11.1.0

Test #84 Receiving any frame other than HEADERS or PRIORITY on a stream in this (idle) state MUST be treated as a connection error (Section 5.4.1) of type PROTOCOL_ERROR. (server side)
Received unmodified: Mitmproxy-11.1.0

Test #85 If an endpoint receives additional frames, other than WINDOW_UPDATE, PRIORITY, or RST_STREAM, for a stream that is in the half-closed (remote) state, it MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (server side)
Received unmodified: Mitmproxy-11.1.0

Test #87 Streams initiated by a server MUST use even-numbered stream identifiers. (server side)
Received unmodified: Mitmproxy-11.1.0

Test #89 DATA frames MUST be associated with a stream. (server side) (server side)
Received unmodified: Mitmproxy-11.1.0

Test #90 If a DATA frame is received whose Stream Identifier field is 0x00, the recipient MUST respond with a connection error (Section 5.4.1) of type PROTOCOL_ERROR. (server side)
Received unmodified: Mitmproxy-11.1.0

Test #91 If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the idle state.) (server side)
Received unmodified: Mitmproxy-11.1.0

Test #94 A HEADERS frame without the END_HEADERS flag set MUST be followed by a CONTINUATION frame for the same stream. (server side)
Received unmodified: Mitmproxy-11.1.0

Test #95 If a HEADERS frame is received whose Stream Identifier field is 0x00, the recipient MUST respond with a connection error (Section 5.4.1) of type PROTOCOL_ERROR. (server side)
Received unmodified: Mitmproxy-11.1.0

Test #96 If a PRIORITY frame is received with a stream identifier of 0x00, the recipient MUST respond with a connection error of type PROTOCOL_ERROR. (server side)
Received unmodified: Mitmproxy-11.1.0

Test #103 The stream identifier for a SETTINGS frame MUST be zero (0x00). (server side)
Received unmodified: Mitmproxy-11.1.0

Test #104 A SETTINGS frame with a length other than a multiple of 6 octets MUST be treated as a connection error (Section 5.4.1) of type FRAME_SIZE_ERROR. (server side)
Received unmodified: Mitmproxy-11.1.0

Test #105 A server MUST NOT explicitly set this value (SETTINGS_ENABLE_PUSH) to 1. A server MAY choose to omit this setting (SETTINGS_ENABLE_PUSH) when it sends a SETTINGS frame, but if a server does include a value, it MUST be 0. (server side)
Received unmodified: Mitmproxy-11.1.0

Test #106 A server MUST NOT send a PUSH_PROMISE frame if it receives the SETTINGS_ENABLE_PUSH (0x02) parameter set to a value of 0. (server side)
Received unmodified: Mitmproxy-11.1.0

Test #107 For SETTINGS_INITIAL_WINDOW_SIZE, values above the maximum flow-control window size of 2^31-1 (2147483647) MUST be treated as a connection error (Section 5.4.1) of type FLOW_CONTROL_ERROR. (server side)
Received unmodified: Mitmproxy-11.1.0

Test #108 The value advertised by an endpoint MUST be between initial value (2^14 = 16,384) and maximum allowed frame size (2^24-1 = 16,777,215 octets), inclusive. (server side)
Received unmodified: Mitmproxy-11.1.0

Test #109 An endpoint that receives a SETTINGS frame with any unknown or unsupported identifier MUST ignore that setting. (server side)
Received unmodified: Mitmproxy-11.1.0

Test #110 Unsupported settings MUST be ignored. (server side)
Received unmodified: Mitmproxy-11.1.0

Test #111 If the Stream Identifier field of a PUSH_PROMISE frame specifies the value 0x00, a recipient MUST respond with a connection error (Section 5.4.1) of type PROTOCOL_ERROR. (server side)
Received unmodified: Mitmproxy-11.1.0

Test #112 The promised stream identifier MUST be a valid choice for the next stream sent by the sender (see 'new stream identifier' in Section 5.1.1). (Using Odd-numbered Stream ID (Invalid for Server)) (server side)
Received unmodified: Mitmproxy-11.1.0

Test #113 The promised stream identifier MUST be a valid choice for the next stream sent by the sender (see 'new stream identifier' in Section 5.1.1). (Using Already Used Stream ID) (server side)
Received unmodified: Mitmproxy-11.1.0

Test #114 The promised stream identifier MUST be a valid choice for the next stream sent by the sender (see 'new stream identifier' in Section 5.1.1). (Using Lower Stream ID) (server side)
Received unmodified: Mitmproxy-11.1.0

Test #115 A PUSH_PROMISE frame without the END_HEADERS flag set MUST be followed by a CONTINUATION frame for the same stream. (server side)
Received unmodified: Mitmproxy-11.1.0

Test #116 If a PING frame is received with a Stream Identifier field value other than 0x00, the recipient MUST respond with a connection error (Section 5.4.1) of type PROTOCOL_ERROR. (server side)
Received unmodified: Mitmproxy-11.1.0

Test #120 A CONTINUATION frame MUST be preceded by a HEADERS, PUSH_PROMISE or CONTINUATION frame without the END_HEADERS flag set. (Using PUSH_PROMISE frame with END_HEADERS flag set) (server side)
Received unmodified: Mitmproxy-11.1.0

Test #121 If a CONTINUATION frame is received with a Stream Identifier field of 0x00, the recipient MUST respond with a connection error (Section 5.4.1) of type PROTOCOL_ERROR. (server side)
Received unmodified: Mitmproxy-11.1.0

Test #122 A CONTINUATION frame MUST be preceded by a HEADERS, PUSH_PROMISE or CONTINUATION frame without the END_HEADERS flag set. (Using HEADERS frame with END_HEADERS flag set) (server side)
Received unmodified: Mitmproxy-11.1.0

Test #123 CONTINUATION frames MUST be associated with a stream. (server side)
Received unmodified: Mitmproxy-11.1.0

Test #124 If the END_HEADERS flag is not set, this frame MUST be followed by another CONTINUATION frame. A receiver MUST treat the receipt of any other type of frame or a frame on a different stream as a connection error (Section 5.4.1) of type PROTOCOL_ERROR. (server side)
Received unmodified: Mitmproxy-11.1.0

Test #125 Trailers MUST NOT include pseudo-header fields (Section 8.3). (server side)
Received modified: Cloudflare, HAproxy-2.9.10
Received unmodified: Mitmproxy-11.1.0

Test #126 Other frames (from any stream) MUST NOT occur between the HEADERS frame and any CONTINUATION frames that might follow. (server side)
Received unmodified: Mitmproxy-11.1.0

Test #127 An endpoint that receives a HEADERS frame without the END_STREAM flag set after receiving the HEADERS frame that opens a request or after receiving a final (non-informational) status code MUST treat the corresponding request or response as malformed (Section 8.1.1). (server side)
Received unmodified: Mitmproxy-11.1.0

Test #128 Field names MUST be converted to lowercase when constructing an HTTP/2 message. (server side)
Received unmodified: Mitmproxy-11.1.0

Test #129 Field names MUST NOT contain control characters (0x00-0x1F) (server side)
Received modified: Node-20.16.0
Received unmodified: Mitmproxy-11.1.0

Test #130 Field names MUST NOT contain ASCII SP (0x20) (server side)
Received modified: Node-20.16.0
Received unmodified: Mitmproxy-11.1.0

Test #131 Field names MUST NOT contain DEL character (0x7F) (server side)
Received unmodified: Mitmproxy-11.1.0

Test #132 Field names MUST NOT contain high byte characters (0x80-0xFF) (server side)
Received modified: Node-20.16.0
Received unmodified: Mitmproxy-11.1.0

Test #133 With the exception of pseudo-header fields (Section 8.3), which have a name that starts with a single colon, field names MUST NOT include a colon (ASCII COLON, 0x3a). (server side)
Received modified: Node-20.16.0
Received unmodified: Mitmproxy-11.1.0

Test #134 A field value MUST NOT contain line feed (ASCII LF, 0x0a). (Tested at the start of the value) (server side)
Received modified: Node-20.16.0
Received unmodified: Mitmproxy-11.1.0

Test #135 A field value MUST NOT contain carriage return (ASCII CR, 0x0d). (Tested at the start of the value) (server side)
Received modified: Node-20.16.0
Received unmodified: Mitmproxy-11.1.0

Test #136 A field value MUST NOT start with an ASCII whitespace character (ASCII SP or HTAB, 0x20 or 0x09). (server side)
Received modified: Cloudflare, Node-20.16.0
Received unmodified: Caddy-2.9.1, Envoy-1.32.2, HAproxy-2.9.10, Mitmproxy-11.1.0

Test #137 A field value MUST NOT end with an ASCII whitespace character (ASCII SP or HTAB, 0x20 or 0x09). (server side)
Received modified: Cloudflare, Node-20.16.0
Received unmodified: Caddy-2.9.1, Envoy-1.32.2, HAproxy-2.9.10, Mitmproxy-11.1.0

Test #138 A field value MUST NOT contain line feed (ASCII LF, 0x0a). (Tested at the middle of the value) (server side)
Received unmodified: Mitmproxy-11.1.0

Test #139 A field value MUST NOT contain line feed (ASCII LF, 0x0a). (Tested at the end of the value) (server side)
Received unmodified: Mitmproxy-11.1.0

Test #140 A field value MUST NOT contain carriage return (ASCII CR, 0x0d). (Tested at the middle of the value) (server side)
Received unmodified: Mitmproxy-11.1.0

Test #141 A field value MUST NOT contain carriage return (ASCII CR, 0x0d). (Tested at the end of the value) (server side)
Received unmodified: Mitmproxy-11.1.0

Test #142 An endpoint MUST NOT generate an HTTP/2 message containing connection header field (RFC9113 Section 8.2.2) (server side)
Received modified: Caddy-2.9.1
Received unmodified: Mitmproxy-11.1.0

Test #143 An endpoint MUST NOT generate an HTTP/2 message containing proxy-connection header field (RFC9113 Section 8.2.2) (server side)
Received modified: Caddy-2.9.1
Received unmodified: Mitmproxy-11.1.0

Test #144 An endpoint MUST NOT generate an HTTP/2 message containing keep-alive header field (RFC9113 Section 8.2.2) (server side)
Received modified: Caddy-2.9.1
Received unmodified: Mitmproxy-11.1.0

Test #145 An endpoint MUST NOT generate an HTTP/2 message containing transfer-encoding header field (RFC9113 Section 8.2.2) (server side)
Received modified: Caddy-2.9.1
Received unmodified: Mitmproxy-11.1.0

Test #146 An endpoint MUST NOT generate an HTTP/2 message containing upgrade header field (RFC9113 Section 8.2.2) (server side)
Received modified: Caddy-2.9.1, Cloudflare
Received unmodified: Mitmproxy-11.1.0

Test #147 The TE header field MAY be present in an HTTP/2 request; when it is, it MUST NOT contain any value other than 'trailers'. (server side)
Received modified: Caddy-2.9.1
Received unmodified: HAproxy-2.9.10, Mitmproxy-11.1.0

Test #148 Pseudo-header fields defined for requests MUST NOT appear in responses. (server side)
Received modified: Cloudflare
Received unmodified: Mitmproxy-11.1.0

Test #149 All pseudo-header fields sent from a server MUST appear in a field block before all regular field lines. Any request or response that contains a pseudo-header field that appears in a field block after a regular field line MUST be treated as malformed (Section 8.1.1). (server side)
Received unmodified: Mitmproxy-11.1.0

Test #150 The same pseudo-header field name MUST NOT appear more than once in a field block. A field block for an HTTP request or response that contains a repeated pseudo-header field name MUST be treated as malformed (Section 8.1.1). Tested with a response frame with the same value. (server side)
Received unmodified: Mitmproxy-11.1.0

Test #151 The same pseudo-header field name MUST NOT appear more than once in a field block. A field block for an HTTP request or response that contains a repeated pseudo-header field name MUST be treated as malformed (Section 8.1.1). Tested with a response frame with different values. (server side)
Received unmodified: Mitmproxy-11.1.0

Test #152 Pseudo-header fields are not HTTP header fields. Endpoints MUST NOT generate pseudo-header fields other than those defined in this document. (server side)
Received unmodified: Mitmproxy-11.1.0

Test #153 For HTTP/2 responses, a single ":status" pseudo-header field is defined that carries the HTTP status code field. This pseudo-header field MUST be included in all responses, including interim responses; otherwise, the response is malformed. (server side)
Received modified: Cloudflare
Received unmodified: Mitmproxy-11.1.0

Test #154 The header fields in PUSH_PROMISE and any subsequent CONTINUATION frames MUST be a valid and complete set of request header fields. (server side)
Received unmodified: Mitmproxy-11.1.0

Test #155 In the PUSH_PROMISE frame, the server MUST include a method in the ":method" pseudo-header field that is safe and cacheable. (server side)
Received unmodified: Mitmproxy-11.1.0

Test #156 HTTP/2 does not support the 101 (Switching Protocols) informational status code (Section 15.2.2 of [HTTP]). (server side)
Received unmodified: Caddy-2.9.1, Mitmproxy-11.1.0

