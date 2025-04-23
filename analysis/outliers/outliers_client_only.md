# Outlier Behaviors in HTTP/2 Conformance Tests - Client-Only Scope

This document lists tests where exactly one proxy behaved differently than all others.

Total outliers found: 31

## Outliers for Azure-AG

| Test ID | Description | Outlier Behavior | Common Behavior |
|---------|-------------|------------------|----------------|
| 20 | The stream identifier for a SETTINGS frame MUST be zero (0x00). | dropped | goaway |
| 30 | If a PING frame is received with a Stream Identifier field value other than 0x00, the recipient MUST respond with a connection error (Section 5.4.1) of type PROTOCOL_ERROR. | dropped | goaway |
| 33 | A receiver MUST treat the receipt of a WINDOW_UPDATE frame with a flow-control window increment of 0 as a stream error (Section 5.4.2) of type PROTOCOL_ERROR. | dropped | goaway |
| 81 | If a DATA frame is received whose Stream Identifier field is 0x00, the recipient MUST respond with a connection error (Section 5.4.1) of type PROTOCOL_ERROR. | dropped | goaway |

## Outliers for Fastly

| Test ID | Description | Outlier Behavior | Common Behavior |
|---------|-------------|------------------|----------------|
| 7 | If an endpoint receives additional frames, other than WINDOW_UPDATE, PRIORITY, or RST_STREAM, for a stream that is in the half-closed (remote) state, it MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. | reset | dropped |
| 31 | With the CONNECT method, the " :scheme" and " :path" pseudo-header fields MUST be omitted. (Tested with only :path present) | reset | dropped |
| 32 | With the CONNECT method, the " :scheme" and " :path" pseudo-header fields MUST be omitted. (Tested with only :scheme present) | reset | dropped |
| 41 | Field names MUST be converted to lowercase when constructing an HTTP/2 message. | goaway | dropped |
| 57 | Pseudo-header fields are not HTTP header fields. Endpoints MUST NOT generate pseudo-header fields other than those defined in this document. | goaway | dropped |
| 59 | Pseudo-header fields defined for responses MUST NOT appear in requests. | goaway | dropped |
| 62 | The same pseudo-header field name MUST NOT appear more than once in a field block. A field block for an HTTP request or response that contains a repeated pseudo-header field name MUST be treated as malformed (Section 8.1.1). Tested with a request frame with the same value. | goaway | dropped |
| 63 | The same pseudo-header field name MUST NOT appear more than once in a field block. A field block for an HTTP request or response that contains a repeated pseudo-header field name MUST be treated as malformed (Section 8.1.1). Tested with a request frame with different values. | goaway | dropped |
| 68 | The ":path" pseudo-header field MUST NOT be empty for "http" or "https" URIs; "http" or "https" URIs that do not contain a path component MUST include a value of '/'. | goaway | dropped |
| 69 | All HTTP/2 requests MUST include exactly one valid value for the ":method", ":scheme", and ":path" pseudo-header fields, unless they are CONNECT requests (Section 8.5). An HTTP request that omits mandatory pseudo-header fields is malformed (Section 8.1.1). (Tested with :method missing) | reset | dropped |
| 70 | All HTTP/2 requests MUST include exactly one valid value for the ":method", ":scheme", and ":path" pseudo-header fields, unless they are CONNECT requests (Section 8.5). An HTTP request that omits mandatory pseudo-header fields is malformed (Section 8.1.1). (Tested with :scheme missing) | reset | dropped |
| 74 | With the CONNECT method, the ":scheme" and ":path" pseudo-header fields MUST be omitted. (Tested with both present) | reset | dropped |
| 83 | If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the half-closed (remote) state.) | reset | dropped |
| 84 | If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the closed state.) | reset | dropped |
| 103 | All HTTP/2 requests MUST include exactly one valid value for the ":method", ":scheme", and ":path" pseudo-header fields, unless they are CONNECT requests (Section 8.5). An HTTP request that omits mandatory pseudo-header fields is malformed (Section 8.1.1). (Tested with :path missing) | reset | dropped |

## Outliers for Lighttpd

| Test ID | Description | Outlier Behavior | Common Behavior |
|---------|-------------|------------------|----------------|
| 8 | Values greater than 16,384 MUST NOT be sent unless receiver has set larger SETTINGS_MAX_FRAME_SIZE | reset | received |
| 76 | An endpoint MUST NOT send frames other than PRIORITY on a closed stream. | dropped | goaway |

## Outliers for Varnish

| Test ID | Description | Outlier Behavior | Common Behavior |
|---------|-------------|------------------|----------------|
| 10 | A reserved 1-bit field. The semantics of this bit are undefined, and the bit MUST remain unset (0x00) when sending and MUST be ignored when receiving. | received | dropped |
| 40 | Trailers MUST NOT include pseudo-header fields (Section 8.3). | received | goaway |
| 51 | An endpoint MUST NOT generate an HTTP/2 message containing connection header field (RFC9113 Section 8.2.2) | received | dropped |
| 52 | An endpoint MUST NOT generate an HTTP/2 message containing proxy-connection header field (RFC9113 Section 8.2.2) | received | dropped |
| 53 | An endpoint MUST NOT generate an HTTP/2 message containing keep-alive header field (RFC9113 Section 8.2.2) | received | dropped |
| 54 | An endpoint MUST NOT generate an HTTP/2 message containing transfer-encoding header field (RFC9113 Section 8.2.2) | received | dropped |
| 55 | An endpoint MUST NOT generate an HTTP/2 message containing upgrade header field (RFC9113 Section 8.2.2) | received | dropped |
| 56 | The TE header field MAY be present in an HTTP/2 request; when it is, it MUST NOT contain any value other than 'trailers'. | received | dropped |
| 60 | All pseudo-header fields sent from a client MUST appear in a field block before all regular field lines. Any request or response that contains a pseudo-header field that appears in a field block after a regular field line MUST be treated as malformed (Section 8.1.1). | received | dropped |
| 67 | ':authority' MUST NOT include the deprecated userinfo subcomponent for "http" or "https" schemed URIs. | received | dropped |

