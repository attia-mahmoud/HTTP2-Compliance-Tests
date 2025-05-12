Test Outcomes by Test ID

Test #4 Client preface must include a SETTINGS frame
Received: Azure-AG, Lighttpd-1.4.76, Nginx-1.26.0, Varnish-7.7.0
Received modified: Cloudflare

Test #8 Values greater than 16,384 MUST NOT be sent unless receiver has set larger SETTINGS_MAX_FRAME_SIZE
Received: Azure-AG, Nginx-1.26.0

Test #7 If an endpoint receives additional frames, other than WINDOW_UPDATE, PRIORITY, or RST_STREAM, for a stream that is in the half-closed (remote) state, it MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED.
Received: Lighttpd-1.4.76

Test #110 A reserved 1-bit field. The semantics of this bit are undefined, and the bit MUST remain unset (0x00) when sending and MUST be ignored when receiving. (server side)
Received unmodified: Caddy-2.9.1, Cloudflare, Envoy-1.32.2, HAproxy-2.9.10, Nghttpx-1.62.1, Node-20.16.0

Test #83 If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the half-closed (remote) state.)
Received: Lighttpd-1.4.76

Test #75 With the CONNECT method, The ":authority" pseudo-header field contains the host and port to connect to
Received modified: H2O-26b116e95
Received unmodified: Nghttpx-1.62.1

Test #40 Trailers MUST NOT include pseudo-header fields (Section 8.3).
Received: Varnish-7.7.0

Test #49 A field value MUST NOT start with an ASCII whitespace character (ASCII SP or HTAB, 0x20 or 0x09).
Received unmodified: Envoy-1.32.2, HAproxy-2.9.10

Test #50 A field value MUST NOT end with an ASCII whitespace character (ASCII SP or HTAB, 0x20 or 0x09).
Received unmodified: Envoy-1.32.2, HAproxy-2.9.10

Test #51 An endpoint MUST NOT generate an HTTP/2 message containing connection header field (RFC9113 Section 8.2.2)
Received: Varnish-7.7.0

Test #53 An endpoint MUST NOT generate an HTTP/2 message containing keep-alive header field (RFC9113 Section 8.2.2)
Received: Varnish-7.7.0

Test #54 An endpoint MUST NOT generate an HTTP/2 message containing transfer-encoding header field (RFC9113 Section 8.2.2)
Received: Varnish-7.7.0

Test #56 The TE header field MAY be present in an HTTP/2 request; when it is, it MUST NOT contain any value other than 'trailers'.
Received: Varnish-7.7.0

Test #66 Clients MUST NOT generate a request with a Host header field that differs from the ":authority" pseudo-header field.
Received modified: HAproxy-2.9.10, Nghttpx-1.62.1

Test #67 ':authority' MUST NOT include the deprecated userinfo subcomponent for "http" or "https" schemed URIs.
Received: Varnish-7.7.0
Received unmodified: HAproxy-2.9.10, Nghttpx-1.62.1

Test #10 A reserved 1-bit field. The semantics of this bit are undefined, and the bit MUST remain unset (0x00) when sending and MUST be ignored when receiving.
Received: Varnish-7.7.0
Received unmodified: Nghttpx-1.62.1

Test #139 An endpoint MUST NOT generate an HTTP/2 message containing keep-alive header field (RFC9113 Section 8.2.2)
Received modified: Caddy-2.9.1

Test #58 Pseudo-header fields defined for requests MUST NOT appear in responses.
Received modified: Cloudflare

Test #151 If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the half-closed (remote) state.)
Received unmodified: Caddy-2.9.1, Cloudflare, Envoy-1.32.2, HAproxy-2.9.10, Nghttpx-1.62.1, Node-20.16.0

Test #71 For HTTP/2 responses, a single ":status" pseudo-header field is defined that carries the HTTP status code field. This pseudo-header field MUST be included in all responses, including interim responses; otherwise, the response is malformed.
Received unmodified: Cloudflare

Test #140 An endpoint MUST NOT generate an HTTP/2 message containing transfer-encoding header field (RFC9113 Section 8.2.2)
Received modified: Caddy-2.9.1

Test #141 An endpoint MUST NOT generate an HTTP/2 message containing upgrade header field (RFC9113 Section 8.2.2)
Received modified: Caddy-2.9.1, Cloudflare

Test #166 HTTP/2 does not support the 101 (Switching Protocols) informational status code (Section 15.2.2 of [HTTP]).
Received unmodified: Caddy-2.9.1

Test #126 Trailers MUST NOT include pseudo-header fields (Section 8.3). (server side)
Received modified: Cloudflare, HAproxy-2.9.10

Test #128 Field names MUST NOT contain control characters (0x00-0x1F)
Received modified: Node-20.16.0

Test #129 Field names MUST NOT contain ASCII SP (0x20)
Received modified: Node-20.16.0

Test #131 Field names MUST NOT contain high byte characters (0x80-0xFF)
Received modified: Node-20.16.0

Test #132 With the exception of pseudo-header fields (Section 8.3), which have a name that starts with a single colon, field names MUST NOT include a colon (ASCII COLON, 0x3a).
Received modified: Node-20.16.0

Test #133 A field value MUST NOT contain line feed (ASCII LF, 0x0a). (Tested at the start of the value)
Received modified: Node-20.16.0

Test #134 A field value MUST NOT contain carriage return (ASCII CR, 0x0d). (Tested at the start of the value)
Received modified: Node-20.16.0

Test #135 A field value MUST NOT start with an ASCII whitespace character (ASCII SP or HTAB, 0x20 or 0x09).
Received modified: Cloudflare, Node-20.16.0
Received unmodified: Caddy-2.9.1, Envoy-1.32.2, HAproxy-2.9.10

Test #136 A field value MUST NOT end with an ASCII whitespace character (ASCII SP or HTAB, 0x20 or 0x09).
Received modified: Cloudflare, Node-20.16.0
Received unmodified: Caddy-2.9.1, Envoy-1.32.2, HAproxy-2.9.10

Test #137 An endpoint MUST NOT generate an HTTP/2 message containing connection header field (RFC9113 Section 8.2.2)
Received modified: Caddy-2.9.1

Test #142 The TE header field MAY be present in an HTTP/2 request; when it is, it MUST NOT contain any value other than 'trailers'.
Received modified: Caddy-2.9.1
Received unmodified: HAproxy-2.9.10

Test #52 An endpoint MUST NOT generate an HTTP/2 message containing proxy-connection header field (RFC9113 Section 8.2.2)
Received: Varnish-7.7.0

Test #55 An endpoint MUST NOT generate an HTTP/2 message containing upgrade header field (RFC9113 Section 8.2.2)
Received: Varnish-7.7.0

Test #60 All pseudo-header fields sent from a client MUST appear in a field block before all regular field lines. Any request or response that contains a pseudo-header field that appears in a field block after a regular field line MUST be treated as malformed (Section 8.1.1).
Received: Varnish-7.7.0

Test #138 An endpoint MUST NOT generate an HTTP/2 message containing proxy-connection header field (RFC9113 Section 8.2.2)
Received modified: Caddy-2.9.1

