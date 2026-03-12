# Cortex4 Gate API Reference

Technical reference for the SAS-AM email gate API, hosted on the Cortex4 server behind a Cloudflare Tunnel.

---

## Base URL

```
https://gate.sas-am.com
```

The API base URL is exposed via Cloudflare Tunnel. All requests use HTTPS.

---

## Endpoints

### POST `/gate`

Submit a gated download request. Captures lead data and returns a time-limited download URL.

#### Request

**Content-Type:** `application/json`

**Payload Schema:**

| Field              | Type   | Required | Description                                                        |
|--------------------|--------|----------|--------------------------------------------------------------------|
| `name`             | string | Yes      | Full name of the person requesting the download.                   |
| `role`             | string | Yes      | Job title or role (e.g. "Maintenance Manager").                    |
| `email`            | string | Yes      | Work email address. Validated server-side for format.              |
| `company`          | string | No       | Company or organisation name. Defaults to empty string if omitted. |
| `resource`         | string | Yes      | Resource slug identifying the artefact (e.g. `maintenance-business-case`, `pm-effectiveness-checklist`). |
| `source`           | string | Yes      | Origin of the request. Use `webflow-gate` for Webflow embeds.      |
| `turnstile_token`  | string | Yes      | Cloudflare Turnstile verification token from the client widget.    |

**Example Request Body:**

```json
{
  "name": "Jane Smith",
  "role": "Maintenance Manager",
  "email": "jane.smith@example.com",
  "company": "Acme Mining",
  "resource": "maintenance-business-case",
  "source": "webflow-gate",
  "turnstile_token": "0.aBcDeFgHiJkLmNoPqRsT..."
}
```

#### Response (Success)

**Status:** `200 OK`

**Body:**

```json
{
  "download_url": "/download/a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

The `download_url` is a **relative path**. Construct the full download URL by prepending the API base:

```
https://gate.sas-am.com/download/a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

The download token is single-use and time-limited. Once the user clicks the link, the server serves the artefact file and invalidates the token.

#### Response (Error)

**Status:** `4xx` or `5xx`

**Body:**

```json
{
  "detail": "Human-readable error message."
}
```

Common error scenarios:

| Status | `detail` message                                         | Cause                                           |
|--------|----------------------------------------------------------|--------------------------------------------------|
| 400    | `"Invalid email address."`                               | Email format validation failed.                  |
| 400    | `"Resource not found."`                                  | The `resource` slug does not match a known artefact. |
| 403    | `"Turnstile verification failed."`                       | The Cloudflare Turnstile token was invalid or expired. |
| 429    | `"Too many requests. Please try again later."`           | Rate limit exceeded.                             |
| 500    | `"Something went wrong. Please try again."`              | Internal server error.                           |

---

## Cloudflare Turnstile Integration

The gate form uses Cloudflare Turnstile for bot protection. Turnstile is a privacy-preserving alternative to reCAPTCHA that runs as an invisible or managed challenge.

### Client-Side Setup

1. **Load the Turnstile script** in the HTML head or body:

   ```html
   <script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>
   ```

2. **Add the Turnstile widget** inside the form:

   ```html
   <div class="cf-turnstile" data-sitekey="0x4AAAAAACfsXoEwP0T4dL86"></div>
   ```

3. **Extract the token** before submitting:

   ```javascript
   var tokenEl = form.querySelector('[name=cf-turnstile-response]');
   var token = tokenEl ? tokenEl.value : '';
   ```

4. **Send the token** as `turnstile_token` in the API payload.

5. **Reset on error** so the user can retry:

   ```javascript
   if (window.turnstile) {
     window.turnstile.reset();
   }
   ```

### Sitekey

| Environment | Sitekey                            |
|-------------|------------------------------------|
| Production  | `0x4AAAAAACfsXoEwP0T4dL86`         |

The sitekey is public and safe to embed in client-side HTML. The corresponding secret key is stored server-side on the Cortex4 server.

---

## Download Flow

The full user journey from form submission to file download:

```
1. User fills in name, role, email
2. Cloudflare Turnstile generates a verification token
3. Client POST to /gate with lead data + turnstile_token
4. Server validates Turnstile token with Cloudflare
5. Server stores lead data in the database
6. Server generates a single-use download token
7. Server returns { download_url: "/download/{token}" }
8. Client constructs full URL: API_BASE + download_url
9. Client shows success state with download button
10. User clicks download button
11. Server serves the artefact file and invalidates the token
```

### Token Behaviour

- Tokens are **single-use** -- once the download starts, the token is consumed.
- Tokens have a **time-to-live (TTL)** -- expired tokens return a 404.
- If the user needs to re-download, they must submit the form again. The server recognises returning email addresses and does not create duplicate lead records.

---

## Resource Slugs

Resource slugs identify the downloadable artefact. They follow kebab-case convention and must match an artefact registered on the Cortex4 server.

**Examples of existing slugs:**

| Slug                              | Artefact                            |
|-----------------------------------|-------------------------------------|
| `maintenance-business-case`       | Maintenance Business Case Template  |
| `internal-benchmarking-scorecard` | Internal Benchmarking Scorecard     |
| `pm-effectiveness-checklist`      | PM Effectiveness Audit Checklist    |

When creating a new gated download, the resource slug must be registered on the Cortex4 server before the gate form will work. Coordinate with the server administrator to register new slugs.

---

## Brand Colours

All gate forms use the SAS-AM brand palette:

| Colour          | Hex       | Usage                                      |
|-----------------|-----------|---------------------------------------------|
| SAS Blue        | `#002244` | Header background, primary brand colour     |
| SAS Green       | `#69BE28` | Buttons, accents, focus rings, icons        |
| SAS Green Hover | `#5AA822` | Button hover state                          |
| Error Red       | `#EF4444` | Validation errors, required field indicators |
| Background      | `#ffffff` | Card body background                       |
| Footer BG       | `#f7f7f7` | Footer strip background                    |
| Text Primary    | `#1a1a1a` | Form labels, success heading                |
| Text Muted      | `#6b7280` | Footer text, success message body           |

---

## CORS and Security

- The API accepts cross-origin requests from `*.sas-am.com` domains.
- All requests must include a valid Cloudflare Turnstile token.
- Rate limiting is applied per IP address.
- No authentication headers are required -- the Turnstile token serves as the anti-abuse mechanism.
- The `source` field allows the server to track where submissions originate (e.g. `webflow-gate`, `linkedin-campaign`, `direct`).
