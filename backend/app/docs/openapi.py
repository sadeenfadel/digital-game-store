from flask import make_response
from flask_smorest import Api


SWAGGER_UI = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Digital Game Store API</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/5.11.0/swagger-ui.min.css">
    <style>
        :root {
            --bg: #ffffff; --bg2: #f8f9fa; --text: #1a1a1a; --text2: #666;
            --border: #e1e4e8; --accent: #0366d6; --get: #61affe; --post: #49cc90;
            --delete: #f93e3e; --card-bg: #ffffff;
        }
        .dark {
            --bg: #0d1117; --bg2: #161b22; --text: #e6edf3; --text2: #8b949e;
            --border: #30363d; --accent: #58a6ff; --get: #388bfd; --post: #3fb950;
            --delete: #f85149; --card-bg: #161b22;
        }
        html, body { background: var(--bg) !important; color: var(--text) !important; margin: 0; }
        #theme-toggle {
            position: fixed !important; top: 12px !important; right: 20px !important;
            z-index: 99999 !important; background: var(--bg2) !important;
            border: 2px solid var(--accent) !important; color: var(--accent) !important;
            padding: 8px 16px !important; border-radius: 8px !important;
            cursor: pointer !important; font-size: 14px !important; font-weight: 600 !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2) !important;
        }
        #theme-toggle:hover { background: var(--accent) !important; color: #fff !important; }
        .dark .swagger-ui .topbar { background: var(--bg2) !important; border-bottom: 1px solid var(--border) !important; }
        .dark .swagger-ui .scheme-container { background: var(--bg2) !important; border: 1px solid var(--border) !important; box-shadow: none !important; }
        .dark .swagger-ui .opblock { border-radius: 8px !important; border: 1px solid var(--border) !important; }
        .dark .swagger-ui .opblock .opblock-summary { border-radius: 8px !important; }
        .dark .swagger-ui .opblock.opblock-get { background: rgba(56,139,253,0.06) !important; border-color: #388bfd !important; }
        .dark .swagger-ui .opblock.opblock-get .opblock-summary-method { background: #388bfd !important; }
        .dark .swagger-ui .opblock.opblock-post { background: rgba(63,185,80,0.06) !important; border-color: #3fb950 !important; }
        .dark .swagger-ui .opblock.opblock-post .opblock-summary-method { background: #3fb950 !important; }
        .dark .swagger-ui .opblock.opblock-delete { background: rgba(248,81,73,0.06) !important; border-color: #f85149 !important; }
        .dark .swagger-ui .opblock.opblock-delete .opblock-summary-method { background: #f85149 !important; }
        .dark .swagger-ui .opblock .opblock-summary-description { color: #8b949e !important; }
        .dark .swagger-ui .model-box { background: #161b22 !important; border: 1px solid #30363d !important; }
        .dark .swagger-ui .model-title { color: #e6edf3 !important; }
        .dark .swagger-ui .prop-type { color: #f85149 !important; }
        .dark .swagger-ui .prop-format { color: #8b949e !important; }
        .dark .swagger-ui table thead tr th { color: #e6edf3 !important; border-bottom: 1px solid #30363d !important; }
        .dark .swagger-ui table tbody tr td { color: #e6edf3 !important; border-bottom: 1px solid #30363d !important; }
        .dark .swagger-ui .btn.authorize { color: #f85149 !important; border-color: #f85149 !important; }
        .dark .swagger-ui .btn.authorize svg { fill: #f85149 !important; }
        .dark .swagger-ui input[type="text"], .dark .swagger-ui textarea {
            background: #0d1117 !important; border: 1px solid #30363d !important; color: #e6edf3 !important;
        }
        .dark .swagger-ui .modal-ux { background: #161b22 !important; border: 1px solid #30363d !important; }
        .dark .swagger-ui .modal-ux-content { color: #e6edf3 !important; }
        .dark .swagger-ui .opblock-tag { color: #e6edf3 !important; border-bottom: 1px solid #30363d !important; }
        .dark .swagger-ui .opblock-tag:hover { color: #58a6ff !important; }
    </style>
</head>
<body>
    <button id="theme-toggle">Dark Mode</button>
    <div id="swagger-ui"></div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/5.11.0/swagger-ui-bundle.min.js"></script>
    <script>
        document.getElementById('theme-toggle').onclick = function() {
            document.documentElement.classList.toggle('dark');
            var isDark = document.documentElement.classList.contains('dark');
            this.textContent = isDark ? 'Light Mode' : 'Dark Mode';
        };
        SwaggerUIBundle({
            url: "/api/docs/openapi.json",
            dom_id: '#swagger-ui',
            presets: [SwaggerUIBundle.presets.apis, SwaggerUIBundle.SwaggerUIStandalonePreset],
            layout: "BaseLayout",
            deepLinking: true,
            defaultModelsExpandDepth: -1,
            docExpansion: "list",
            filter: true,
            tryItOutEnabled: true
        });
    </script>
</body>
</html>"""


def configure_swagger(app):
    api = Api(app)

    api.spec.components.security_scheme(
        "BearerAuth",
        {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        },
    )

    app.config["OPENAPI_SWAGGER_UI_PATH"] = None
    app.config["OPENAPI_SWAGGER_UI_URL"] = None

    @app.route("/docs")
    @app.route("/docs/")
    def swagger_ui():
        resp = make_response(SWAGGER_UI)
        resp.headers["Content-Type"] = "text/html"
        return resp

    return api
