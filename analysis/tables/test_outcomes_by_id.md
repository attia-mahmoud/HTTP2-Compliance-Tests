Test Outcomes by Test ID

4 Client preface must include a SETTINGS frame
Received modified: Azure-AG, Cloudflare, Lighttpd, Nginx

7 If an endpoint receives additional frames, other than WINDOW_UPDATE, PRIORITY, or RST_STREAM, for a stream that is in the half-closed (remote) state, it MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED.
Received unmodified: Lighttpd

8 Values greater than 16,384 MUST NOT be sent unless receiver has set larger SETTINGS_MAX_FRAME_SIZE
Received unmodified: Azure-AG, Cloudflare, Nginx

58 Pseudo-header fields defined for requests MUST NOT appear in responses.
Received modified: Cloudflare

71 For HTTP/2 responses, a single ":status" pseudo-header field is defined that carries the HTTP status code field. This pseudo-header field MUST be included in all responses, including interim responses; otherwise, the response is malformed.
Received unmodified: Cloudflare

83 If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the half-closed (remote) state.)
Received unmodified: Lighttpd

87 A SETTINGS frame MUST be sent by both endpoints at the start of a connection and MAY be sent at any other time by either endpoint over the lifetime of the connection. (Tested from the client side.)
Received modified: Azure-AG, Cloudflare, Lighttpd, Nginx

110 A reserved 1-bit field. The semantics of this bit are undefined, and the bit MUST remain unset (0x00) when sending and MUST be ignored when receiving. (server side)
Received unmodified: Caddy, Cloudflare, Envoy, HAproxy, Nghttpx, Node

126 Trailers MUST NOT include pseudo-header fields (Section 8.3).
Received modified: Cloudflare, HAproxy

128 Field names MUST NOT contain control characters (0x00-0x1F)
Received modified: Node

129 Field names MUST NOT contain ASCII SP (0x20)
Received modified: Node

131 Field names MUST NOT contain high byte characters (0x80-0xFF)
Received modified: Node

132 With the exception of pseudo-header fields (Section 8.3), which have a name that starts with a single colon, field names MUST NOT include a colon (ASCII COLON, 0x3a).
Received modified: Node

133 A field value MUST NOT contain line feed (ASCII LF, 0x0a). (Tested at the start of the value)
Received modified: Node

134 A field value MUST NOT contain carriage return (ASCII CR, 0x0d). (Tested at the start of the value)
Received modified: Node

135 A field value MUST NOT start with an ASCII whitespace character (ASCII SP or HTAB, 0x20 or 0x09).
Received modified: Cloudflare, Node
Received unmodified: Caddy, Envoy, HAproxy

136 A field value MUST NOT end with an ASCII whitespace character (ASCII SP or HTAB, 0x20 or 0x09).
Received modified: Cloudflare, Node
Received unmodified: Caddy, Envoy, HAproxy

137 An endpoint MUST NOT generate an HTTP/2 message containing connection header field (RFC9113 Section 8.2.2)
Received modified: Caddy

138 An endpoint MUST NOT generate an HTTP/2 message containing proxy-connection header field (RFC9113 Section 8.2.2)
Received modified: Caddy

139 An endpoint MUST NOT generate an HTTP/2 message containing keep-alive header field (RFC9113 Section 8.2.2)
Received modified: Caddy

140 An endpoint MUST NOT generate an HTTP/2 message containing transfer-encoding header field (RFC9113 Section 8.2.2)
Received modified: Caddy

141 An endpoint MUST NOT generate an HTTP/2 message containing upgrade header field (RFC9113 Section 8.2.2)
Received modified: Caddy, Cloudflare

142 The TE header field MAY be present in an HTTP/2 request; when it is, it MUST NOT contain any value other than 'trailers'.
Received modified: Caddy
Received unmodified: HAproxy

151 If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the half-closed (remote) state.)
Received unmodified: Caddy, Cloudflare, Envoy, HAproxy, Nghttpx, Node

165 Pseudo-header fields MUST NOT appear in a trailer section.
Received modified: Cloudflare, HAproxy

