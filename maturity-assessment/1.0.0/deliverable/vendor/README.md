# Vendored libraries

## plotly.min.js

- Library: Plotly.js
- Version: 2.35.3 (latest 2.x minified build at time of vendoring)
- Source: https://cdn.plot.ly/plotly-2.35.3.min.js
- Licence: MIT (Copyright Plotly, Inc.) — see https://github.com/plotly/plotly.js/blob/master/LICENSE
- Fetched with:

```bash
curl -sfo vendor/plotly.min.js https://cdn.plot.ly/plotly-2.35.3.min.js
```

The dashboard builder inlines this file into every generated surface so the deliverable works fully offline from `file://` with no CDN reference at runtime. If this file is missing, `buildDashboard.py` fails loudly and quotes the fetch command above — it never falls back to a CDN URL.
