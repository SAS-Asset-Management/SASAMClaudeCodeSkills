---
name: email-gate
description: Generate SAS-AM branded email capture forms for gated downloads. Use when the user asks to create a gated download, generate an email capture form, gate this artefact, create a download gate, build a lead capture form, or gate a presentation behind an email wall. Outputs a standalone HTML snippet for Webflow Custom Code Embed that captures name, role, and email before granting access to a downloadable artefact via the Cortex4 gate API.
---

# SAS-AM Email Gate Skill

Generate SAS-AM branded email capture HTML snippets for embedding in Webflow pages via Custom Code Embed elements. The gate pattern captures lead data (name, role, email) and sends it to the Cortex4 server, which returns a single-use download URL for the gated artefact.

## Purpose

SAS-AM uses email-gated downloads to capture qualified leads from content marketing. When a visitor wants to download a free artefact -- such as an interactive HTML presentation, a benchmarking scorecard, or an audit checklist -- they fill in a short form. The form submits to the Cortex4 gate API at `https://gate.sas-am.com/gate`, which stores the lead data and returns a time-limited download link.

The output of this skill is a single, self-contained HTML file that can be pasted directly into a Webflow Custom Code Embed element. It includes all CSS, HTML structure, Cloudflare Turnstile integration, and JavaScript -- no external dependencies beyond the Turnstile script and the gate API.

## Relationship to Other Skills

This skill sits within the **sas-content-hub** plugin pipeline. The typical workflow is:

1. **sas-presentation** creates the downloadable artefact (e.g. a Reveal.js HTML presentation).
2. **email-gate** (this skill) creates the gated download form that captures leads before granting access to the artefact.
3. **webflow-content-creator** publishes a Webflow article that embeds the gate form via a Custom Code Embed block.
4. **linkedin-post-generator** promotes the article on LinkedIn to drive traffic.

The artefacts behind the gate are typically created using the **sas-presentation** dependency. Coordinate with that skill when the user needs both the artefact and the gate form.

## Discovery Interview

Before generating a gate form, conduct a brief interview to gather the required details. Ask one question at a time and wait for the user's answer before proceeding.

### Question 1: What is the downloadable artefact?

Ask for the title and a short description of the artefact being gated.

> "What artefact are you gating? Give me the title and a one-line description."
>
> For example:
> - A) "Maintenance Business Case Template -- an interactive HTML template for building maintenance investment cases"
> - B) "Internal Benchmarking Scorecard -- score your maintenance crews across five performance dimensions"
> - C) "PM Effectiveness Audit Checklist -- 25 questions across five key areas of PM programme health"
> - D) Something else (describe it)

Use the title as `{{GATE_TITLE}}` and the description as `{{GATE_SUBTITLE}}`. The subtitle should read as an instruction, e.g. "Fill in your details to download the interactive template."

### Question 2: What resource slug should be used?

Suggest a slug based on the title and ask the user to confirm or override.

> "Based on the title, I'd suggest the resource slug: `[suggested-slug]`. This is what the Cortex4 server uses to identify the artefact. Does that work, or would you prefer a different slug?"
>
> Rules for slugs:
> - A) Kebab-case (lowercase, hyphens between words)
> - B) No special characters
> - C) Must match the slug registered on the Cortex4 server

The slug becomes `{{RESOURCE_SLUG}}`.

### Question 3: What icon type best represents this artefact?

Offer four standard icon options and allow a custom SVG path.

> "Which icon best represents this artefact in the header?"
>
> - A) **Document** -- a page with lines (for templates, reports, guides)
> - B) **Chart** -- a bar chart (for scorecards, dashboards, analytics tools)
> - C) **Checklist** -- a clipboard with checkmarks (for checklists, audits, assessments)
> - D) **Scorecard** -- a grid/table layout (for comparison matrices, evaluation tools)
> - E) **Custom** -- provide your own SVG path data

Map the user's choice to the corresponding SVG path for `{{GATE_ICON_SVG}}`:

| Icon Type   | SVG Path (`d` attribute)                                                                                                                                      |
|-------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Document    | `M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8l-6-6zm-1 2l5 5h-5V4zM8 17h8v-2H8v2zm0-4h8v-2H8v2z`                                              |
| Chart       | `M3 3v18h18V3H3zm16 16H5V5h14v14zM7 12h2v5H7v-5zm4-3h2v8h-2V9zm4-2h2v10h-2V7z`                                                                              |
| Checklist   | `M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2M9 5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2M9 5h6m-3 7l2 2 4-4`                          |
| Scorecard   | `M3 3h18v18H3V3zm2 2v14h14V5H5zm2 3h4v2H7V8zm6 0h4v2h-4V8zm-6 4h4v2H7v-2zm6 0h4v2h-4v-2zm-6 4h4v2H7v-2zm6 0h4v2h-4v-2z`                                    |

### Question 4: What button text should the form use?

Suggest defaults based on the artefact type and let the user override.

> "What text should appear on the submit button and the download button?"
>
> Suggested defaults based on your artefact:
> - A) **Template**: Submit = "Get the Template", Download = "Download Template"
> - B) **Scorecard**: Submit = "Get the Scorecard", Download = "Download Scorecard"
> - C) **Checklist**: Submit = "Get the Checklist", Download = "Download Checklist"
> - D) **Guide/Report**: Submit = "Get the Guide", Download = "Download Guide"
> - E) **Custom**: specify your own text for both buttons

The submit button text becomes `{{BUTTON_TEXT}}` and the download link text becomes `{{DOWNLOAD_BUTTON_TEXT}}`.

Also set the success state text. Default values:

- `{{SUCCESS_TITLE}}`: "You're all set!"
- `{{SUCCESS_MESSAGE}}`: "Your download is ready. Click below to get the [artefact description]."

Adjust the success message to reference the specific artefact, e.g. "Click below to get the interactive business case template." or "Click below to get the Internal Benchmarking Scorecard."

### Question 5: API base URL and Turnstile sitekey?

Most of the time the defaults are correct. Only ask if there is reason to believe the user needs a different environment.

> "The default API base URL is `https://gate.sas-am.com` and the Turnstile sitekey is `0x4AAAAAACfsXoEwP0T4dL86`. Are you using the production environment, or do you need different values?"
>
> - A) **Production defaults** (recommended)
> - B) **Custom** -- provide the API base URL and/or sitekey

Defaults:

- `{{API_BASE}}`: `https://gate.sas-am.com`
- `{{TURNSTILE_SITEKEY}}`: `0x4AAAAAACfsXoEwP0T4dL86`

## Template Generation

Once all interview questions are answered, generate the gate HTML by reading the template and replacing placeholders.

### Step 1: Read the Template

Read the template file at `assets/gateTemplate.html` (relative to this skill's directory). The template is a complete, self-contained HTML snippet with CSS, markup, and JavaScript. It contains placeholder tokens in the format `{{PLACEHOLDER_NAME}}`.

### Step 2: Replace Placeholders

Replace every placeholder token with the value gathered during the interview.

| Placeholder              | Source                     | Example Value                                                              |
|--------------------------|----------------------------|----------------------------------------------------------------------------|
| `{{GATE_TITLE}}`         | Question 1                 | `Maintenance Business Case Template`                                       |
| `{{GATE_SUBTITLE}}`      | Question 1                 | `Fill in your details to download the interactive template.`               |
| `{{GATE_ICON_SVG}}`      | Question 3                 | `M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8l-6-6zm-1 2l5 5h-5V4zM8 17h8v-2H8v2zm0-4h8v-2H8v2z` |
| `{{RESOURCE_SLUG}}`      | Question 2                 | `maintenance-business-case`                                                |
| `{{BUTTON_TEXT}}`         | Question 4                 | `Get the Template`                                                         |
| `{{SUCCESS_TITLE}}`      | Question 4                 | `You're all set!`                                                          |
| `{{SUCCESS_MESSAGE}}`    | Question 4                 | `Your download is ready. Click below to get the interactive business case template.` |
| `{{DOWNLOAD_BUTTON_TEXT}}`| Question 4                | `Download Template`                                                        |
| `{{API_BASE}}`           | Question 5                 | `https://gate.sas-am.com`                                                  |
| `{{TURNSTILE_SITEKEY}}`  | Question 5                 | `0x4AAAAAACfsXoEwP0T4dL86`                                                |

Note that `{{BUTTON_TEXT}}` appears twice in the template: once in the submit button markup and once in the `resetButton()` JavaScript function. Replace both occurrences.

### Step 3: Write the Output File

Write the completed HTML to the file path specified by the user. If the user does not specify a path, suggest a sensible default based on the resource slug, e.g.:

```
./[resource-slug]Gate.html
```

Follow camelCase naming conventions per the global rules. For example:
- `maintenanceBusinessCaseGate.html`
- `benchmarkingScorecardGate.html`
- `pmChecklistGate.html`

### Step 4: Confirm and Advise

After writing the file, confirm to the user and provide integration guidance:

> "Gate form created at `[path]`.
>
> **To deploy:**
> 1. Ensure the resource slug `[slug]` is registered on the Cortex4 server.
> 2. In Webflow, add a Custom Code Embed element to your page.
> 3. Paste the entire contents of the generated file into the embed.
> 4. Publish the page.
>
> **The form captures:** name, role, and email address.
> **On success:** the visitor sees a download button linked to the Cortex4-generated token URL.
> **Bot protection:** Cloudflare Turnstile (invisible challenge)."

## API Reference

Refer to `references/gate-api.md` for full details on the Cortex4 gate API, including:

- The POST `/gate` endpoint and its payload schema
- Response format and error codes
- Cloudflare Turnstile integration details
- Download token behaviour (single-use, time-limited)
- Resource slug conventions
- CORS and security considerations
- Brand colour reference

When troubleshooting gate forms or answering user questions about the API, consult this reference file.

## Template Architecture

The gate template is a single HTML snippet designed for Webflow Custom Code Embed. It contains three layers.

### CSS Layer

All styles are scoped under the `.sas-dl-gate` class to prevent conflicts with Webflow's own styles. CSS custom properties define the brand palette (SAS Blue `#002244`, SAS Green `#69BE28`) and UI tokens (backgrounds, borders, shadows, radii). The `!important` declarations on button colours are intentional -- they override Webflow's aggressive default styles on buttons and links.

The template includes a `prefers-reduced-motion` media query that disables all animations and transitions for users who have requested reduced motion in their OS settings.

### HTML Layer

The markup consists of a card with four sections:

1. **Header** -- SAS Blue background with an icon circle, title (`h3`), and subtitle (`p`).
2. **Form body** -- three required fields (name, role, email), a Turnstile widget container, an API error message container, and the submit button.
3. **Success state** -- hidden by default; shown after a successful API response. Contains a checkmark icon, success heading, success message, and a download link styled as a button.
4. **Footer** -- privacy policy link.

The form and success sections are mutually exclusive. On successful submission, the form wrapper is hidden (`display: none`) and the success container is shown (`.visible` class).

### JavaScript Layer

A self-invoking function handles:

- **Client-side validation** -- checks that name, role, and email are non-empty, and that the email matches a basic regex pattern.
- **Turnstile token extraction** -- reads the `cf-turnstile-response` hidden input injected by the Turnstile widget.
- **API submission** -- POSTs the payload to `API_BASE + '/gate'` as JSON.
- **Success handling** -- constructs the full download URL from `API_BASE + data.download_url` and displays the success state.
- **Error handling** -- shows the API error message, resets the submit button, and resets the Turnstile widget so the user can retry.
- **Spinner state** -- replaces the button text with a CSS spinner animation during submission.

## Icon Reference

Four standard icons are provided for common artefact types. Each is a 24x24 SVG viewBox path.

### Document Icon
For templates, reports, guides, and PDF-style documents.
```
M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8l-6-6zm-1 2l5 5h-5V4zM8 17h8v-2H8v2zm0-4h8v-2H8v2z
```

### Chart Icon
For scorecards, dashboards, analytics tools, and data-heavy artefacts.
```
M3 3v18h18V3H3zm16 16H5V5h14v14zM7 12h2v5H7v-5zm4-3h2v8h-2V9zm4-2h2v10h-2V7z
```

### Checklist Icon
For checklists, audits, assessments, and evaluation tools.
```
M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2M9 5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2M9 5h6m-3 7l2 2 4-4
```

### Scorecard Icon
For comparison matrices, evaluation grids, and tabular tools.
```
M3 3h18v18H3V3zm2 2v14h14V5H5zm2 3h4v2H7V8zm6 0h4v2h-4V8zm-6 4h4v2H7v-2zm6 0h4v2h-4v-2zm-6 4h4v2H7v-2zm6 0h4v2h-4v-2z
```

## Output Conventions

### File Naming

Gate files follow camelCase naming with a `Gate` suffix:

| Resource Slug                     | File Name                           |
|-----------------------------------|-------------------------------------|
| `maintenance-business-case`       | `maintenanceBusinessCaseGate.html`  |
| `internal-benchmarking-scorecard` | `benchmarkingScorecardGate.html`    |
| `pm-effectiveness-checklist`      | `pmChecklistGate.html`              |
| `reliability-maturity-assessment` | `reliabilityMaturityGate.html`      |

### Webflow Embedding

The generated HTML file is designed to be pasted in its entirety into a Webflow Custom Code Embed element. The embed should be placed within the article body, typically after the introductory paragraphs and before the main content. This positions the gate as a clear call-to-action that the reader encounters naturally.

The CSS is fully self-contained and scoped to `.sas-dl-gate`, so it will not interfere with Webflow's styles. The JavaScript uses an IIFE (immediately invoked function expression) to avoid polluting the global scope.

### Multiple Gates on One Page

If multiple gate forms appear on the same page, the element IDs will conflict (`sas-dl-form`, `sas-dl-name`, etc.). For multi-gate pages, manually suffix the IDs with a unique identifier (e.g. `sas-dl-form-1`, `sas-dl-form-2`) and update the JavaScript references accordingly. This is an edge case -- most pages have a single gate.

## Pre-Deployment Checklist

Before embedding the gate form in Webflow, verify:

- [ ] Resource slug is registered on the Cortex4 server
- [ ] The downloadable artefact file is uploaded and associated with the slug on the server
- [ ] `{{GATE_TITLE}}` and `{{GATE_SUBTITLE}}` are replaced (no template placeholders remain)
- [ ] `{{RESOURCE_SLUG}}` matches the server-side registration exactly
- [ ] `{{API_BASE}}` points to the correct environment (`https://gate.sas-am.com` for production)
- [ ] `{{TURNSTILE_SITEKEY}}` matches the Cloudflare Turnstile site configuration
- [ ] The form submits successfully in a browser test (check the Network tab for the POST to `/gate`)
- [ ] The download link works after successful submission
- [ ] The form displays correctly on mobile (max-width 480px, centred)
- [ ] Australian English is used in all user-facing text
- [ ] Privacy policy link (`/privacy`) resolves on the target domain
