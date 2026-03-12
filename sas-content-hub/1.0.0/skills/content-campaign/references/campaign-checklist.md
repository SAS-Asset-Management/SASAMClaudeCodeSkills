# Content Campaign Pre-Flight Checklist

Use this checklist before and during campaign execution to ensure nothing is missed.

## Pre-Production

- [ ] Campaign topic defined and validated with user
- [ ] Target sector confirmed
- [ ] Artefact type and scope agreed
- [ ] Real evidence gathered (no fabrication)
- [ ] CTA goal aligned with business objectives
- [ ] WEBFLOW_TOKEN environment variable set
- [ ] sas-presentation plugin installed
- [ ] nano-banana-2 plugin installed and configured (Google AI Studio API key)

## Stage 1: Artefact

- [ ] Artefact created via sas-presentation
- [ ] Interactive elements working (scoring, calculations, etc.)
- [ ] SAS-AM branding applied
- [ ] User approved the artefact
- [ ] File saved to accessible location for gate hosting

## Stage 2: Email Gate

- [ ] Gate HTML generated from template
- [ ] Resource slug is URL-safe and descriptive
- [ ] Cloudflare Turnstile site key configured
- [ ] API base URL correct (https://gate.sas-am.com)
- [ ] Form fields: name, role, email (all required)
- [ ] Success message and download button text appropriate
- [ ] Gate HTML tested (if possible)
- [ ] User approved the gate

## Stage 3: Hero Image

- [ ] Image generated via nano-banana-2
- [ ] Aspect ratio: 16:9 for article hero
- [ ] Post-processing applied (SAS watermark)
- [ ] Image is professional and sector-appropriate
- [ ] User approved the image

## Stage 4: Article

- [ ] Article drafted with real evidence only
- [ ] Australian English spelling throughout
- [ ] SEO title under 60 characters
- [ ] SEO description under 160 characters
- [ ] Card description under 200 characters
- [ ] Alt text for hero image under 125 characters
- [ ] Gate HTML embedded in article body
- [ ] CTA clear and aligned with campaign goal
- [ ] No fabricated stories, quotes, or statistics
- [ ] User approved the article

## Stage 5: Webflow Publishing

- [ ] Site ID confirmed with user
- [ ] Collection ID confirmed (resources collection)
- [ ] Hero image uploaded as Webflow asset
- [ ] CMS item created with all required fields:
  - name, slug, sector, content-type, topic-tags
  - featured-image, featured-image-alt
  - description, body-content
  - seo-title, seo-description
  - publish-date, author, reading-time
- [ ] Draft reviewed in Webflow before publishing live
- [ ] User confirmed publish live (or left as draft)

## Stage 6: LinkedIn Promotion

- [ ] Interview material fed to linkedin-post-generator
- [ ] All eligible formats produced in parallel
- [ ] Best format recommended with rationale
- [ ] Post links to the published article URL
- [ ] No emojis, no hashtags
- [ ] Australian English throughout
- [ ] User approved the post
- [ ] Post ready for manual LinkedIn publishing

## Post-Campaign

- [ ] Campaign summary presented to user
- [ ] All file paths documented
- [ ] Lead capture flowing to Cortex4 (gate.sas-am.com)
- [ ] Article accessible on sas-am.com/resources
- [ ] LinkedIn post published or scheduled
