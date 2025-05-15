Test Outcomes by Test ID

Test #3 Client preface must include a SETTINGS frame
Received: Azure-AG, Lighttpd-1.4.76, Nginx-1.28.0, Varnish-7.7.0
Received modified: Cloudflare, Envoy-1.34.1

Test #4 Values greater than 16,384 MUST NOT be sent unless receiver has set larger SETTINGS_MAX_FRAME_SIZE
Received: Azure-AG, Nginx-1.28.0

Test #6 A reserved 1-bit field. The semantics of this bit are undefined, and the bit MUST remain unset (0x00) when sending and MUST be ignored when receiving.
Received: Varnish-7.7.0
Received unmodified: Apache-2.4.63, Caddy-2.9.1, Envoy-1.34.1, HAproxy-3.2.0, Nghttpx-1.62.1, Node-20.16.0

Test #8 If an endpoint receives additional frames, other than WINDOW_UPDATE, PRIORITY, or RST_STREAM, for a stream that is in the half-closed (remote) state, it MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED.
Received: Lighttpd-1.4.76

Test #15 If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the half-closed (remote) state.)
Received: Lighttpd-1.4.76

Test #40 Trailers MUST NOT include pseudo-header fields (Section 8.3).
Received: Varnish-7.7.0

Test #51 A field value MUST NOT start with an ASCII whitespace character (ASCII SP or HTAB, 0x20 or 0x09).
Received modified: HAproxy-3.2.0

Test #52 A field value MUST NOT end with an ASCII whitespace character (ASCII SP or HTAB, 0x20 or 0x09).
Received modified: HAproxy-3.2.0

Test #57 An endpoint MUST NOT generate an HTTP/2 message containing connection header field (RFC9113 Section 8.2.2)
Received: Varnish-7.7.0

Test #58 An endpoint MUST NOT generate an HTTP/2 message containing proxy-connection header field (RFC9113 Section 8.2.2)
Received: Varnish-7.7.0

Test #59 An endpoint MUST NOT generate an HTTP/2 message containing keep-alive header field (RFC9113 Section 8.2.2)
Received: Varnish-7.7.0

Test #60 An endpoint MUST NOT generate an HTTP/2 message containing transfer-encoding header field (RFC9113 Section 8.2.2)
Received: Varnish-7.7.0

Test #61 An endpoint MUST NOT generate an HTTP/2 message containing upgrade header field (RFC9113 Section 8.2.2)
Received: Varnish-7.7.0

Test #62 The TE header field MAY be present in an HTTP/2 request; when it is, it MUST NOT contain any value other than 'trailers'.
Received: Varnish-7.7.0

Test #65 All pseudo-header fields sent from a client MUST appear in a field block before all regular field lines. Any request or response that contains a pseudo-header field that appears in a field block after a regular field line MUST be treated as malformed (Section 8.1.1).
Received: Varnish-7.7.0

Test #68 Clients MUST NOT generate a request with a Host header field that differs from the ":authority" pseudo-header field.
Received modified: HAproxy-3.2.0, Nghttpx-1.62.1

Test #69 ':authority' MUST NOT include the deprecated userinfo subcomponent for "http" or "https" schemed URIs.
Received: Varnish-7.7.0
Received unmodified: HAproxy-3.2.0, Nghttpx-1.62.1

Test #78 With the CONNECT method, The ":authority" pseudo-header field contains the host and port to connect to
Received modified: H2O-26b116e95
Received unmodified: HAproxy-3.2.0, Nghttpx-1.62.1

Test #81 A reserved 1-bit field. The semantics of this bit are undefined, and the bit MUST remain unset (0x00) when sending and MUST be ignored when receiving. (server side)
Received unmodified: Caddy-2.9.1, Cloudflare, Envoy-1.34.1, HAproxy-3.2.0, Nghttpx-1.62.1, Node-20.16.0

Test #92 If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the half-closed (remote) state.) (server side)
Received unmodified: Caddy-2.9.1, Cloudflare, Nghttpx-1.62.1, Node-20.16.0

Test #125 Trailers MUST NOT include pseudo-header fields (Section 8.3). (server side)
Received modified: Cloudflare

Test #129 Field names MUST NOT contain control characters (0x00-0x1F) (server side)
Received modified: Node-20.16.0

Test #130 Field names MUST NOT contain ASCII SP (0x20) (server side)
Received modified: Node-20.16.0

Test #132 Field names MUST NOT contain high byte characters (0x80-0xFF) (server side)
Received modified: Node-20.16.0

Test #133 With the exception of pseudo-header fields (Section 8.3), which have a name that starts with a single colon, field names MUST NOT include a colon (ASCII COLON, 0x3a). (server side)
Received modified: Node-20.16.0

Test #134 A field value MUST NOT contain line feed (ASCII LF, 0x0a). (Tested at the start of the value) (server side)
Received modified: Node-20.16.0

Test #135 A field value MUST NOT contain carriage return (ASCII CR, 0x0d). (Tested at the start of the value) (server side)
Received modified: Node-20.16.0

Test #136 A field value MUST NOT start with an ASCII whitespace character (ASCII SP or HTAB, 0x20 or 0x09). (server side)
Received modified: Cloudflare, HAproxy-3.2.0, Node-20.16.0
Received unmodified: Caddy-2.9.1, Envoy-1.34.1

Test #137 A field value MUST NOT end with an ASCII whitespace character (ASCII SP or HTAB, 0x20 or 0x09). (server side)
Received modified: Cloudflare, HAproxy-3.2.0, Node-20.16.0
Received unmodified: Caddy-2.9.1, Envoy-1.34.1

Test #142 An endpoint MUST NOT generate an HTTP/2 message containing connection header field (RFC9113 Section 8.2.2) (server side)
Received modified: Caddy-2.9.1

Test #143 An endpoint MUST NOT generate an HTTP/2 message containing proxy-connection header field (RFC9113 Section 8.2.2) (server side)
Received modified: Caddy-2.9.1

Test #144 An endpoint MUST NOT generate an HTTP/2 message containing keep-alive header field (RFC9113 Section 8.2.2) (server side)
Received modified: Caddy-2.9.1

Test #145 An endpoint MUST NOT generate an HTTP/2 message containing transfer-encoding header field (RFC9113 Section 8.2.2) (server side)
Received modified: Caddy-2.9.1

Test #146 An endpoint MUST NOT generate an HTTP/2 message containing upgrade header field (RFC9113 Section 8.2.2) (server side)
Received modified: Caddy-2.9.1, Cloudflare

Test #147 The TE header field MAY be present in an HTTP/2 request; when it is, it MUST NOT contain any value other than 'trailers'. (server side)
Received modified: Caddy-2.9.1
Received unmodified: HAproxy-3.2.0

Test #148 Pseudo-header fields defined for requests MUST NOT appear in responses. (server side)
Received modified: Cloudflare

Test #149 All pseudo-header fields sent from a server MUST appear in a field block before all regular field lines. Any request or response that contains a pseudo-header field that appears in a field block after a regular field line MUST be treated as malformed (Section 8.1.1). (server side)
Received modified: Envoy-1.34.1

Test #153 For HTTP/2 responses, a single ":status" pseudo-header field is defined that carries the HTTP status code field. This pseudo-header field MUST be included in all responses, including interim responses; otherwise, the response is malformed. (server side)
Received modified: Cloudflare

Test #156 HTTP/2 does not support the 101 (Switching Protocols) informational status code (Section 15.2.2 of [HTTP]). (server side)
Received unmodified: Caddy-2.9.1

