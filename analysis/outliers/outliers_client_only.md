# Outlier Behaviors in HTTP/2 Conformance Tests - Client-Only Scope

This document lists tests where exactly one proxy behaved differently than all others.

Total outliers found: 16

## Outliers for Azure-AG

| Test ID | Description | Outlier Behavior | Common Behavior |
|---------|-------------|------------------|----------------|
| 20 | The stream identifier for a SETTINGS frame MUST be zero (0x00). | dropped | goaway |
| 30 | If a PING frame is received with a Stream Identifier field value other than 0x00, the recipient MUST respond with a connection error (Section 5.4.1) of type PROTOCOL_ERROR. | dropped | goaway |
| 33 | A receiver MUST treat the receipt of a WINDOW_UPDATE frame with a flow-control window increment of 0 as a stream error (Section 5.4.2) of type PROTOCOL_ERROR. | dropped | goaway |
| 81 | If a DATA frame is received whose Stream Identifier field is 0x00, the recipient MUST respond with a connection error (Section 5.4.1) of type PROTOCOL_ERROR. | dropped | goaway |

## Outliers for Lighttpd

| Test ID | Description | Outlier Behavior | Common Behavior |
|---------|-------------|------------------|----------------|
| 1 | Receiving any frame other than HEADERS or PRIORITY on a stream in this (idle) state MUST be treated as a connection error (Section 5.4.1) of type PROTOCOL_ERROR. | goaway | dropped |
| 7 | If an endpoint receives additional frames, other than WINDOW_UPDATE, PRIORITY, or RST_STREAM, for a stream that is in the half-closed (remote) state, it MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. | unmodified | dropped |
| 8 | Values greater than 16,384 MUST NOT be sent unless receiver has set larger SETTINGS_MAX_FRAME_SIZE | reset | unmodified |
| 40 | Trailers MUST NOT include pseudo-header fields (Section 8.3). | dropped | goaway |
| 76 | An endpoint MUST NOT send frames other than PRIORITY on a closed stream. | dropped | goaway |
| 77 | RST_STREAM frames MUST NOT be sent for a stream in the 'idle' state. | goaway | dropped |
| 78 | RST_STREAM frames MUST be associated with a stream. | goaway | dropped |
| 80 | DATA frames MUST be associated with a stream. | goaway | dropped |
| 82 | If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the idle state.) | goaway | dropped |
| 83 | If a DATA frame is received whose stream is not in the 'open' or 'half-closed (local)' state, the recipient MUST respond with a stream error (Section 5.4.2) of type STREAM_CLOSED. (Tested in the half-closed (remote) state.) | unmodified | dropped |
| 97 | An endpoint that receives a HEADERS frame without the END_STREAM flag set after receiving the HEADERS frame that opens a request or after receiving a final (non-informational) status code MUST treat the corresponding request or response as malformed (Section 8.1.1). | dropped | goaway |
| 102 | Pseudo-header fields MUST NOT appear in a trailer section. | dropped | goaway |

