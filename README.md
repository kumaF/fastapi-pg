TODO: check PT, PYI, DOC

[tool.ruff.lint.per-file-ignores]
"tests/**" = ["S101", "D", "ANN"]
"alembic/**" = ["D", "ANN", "INP001"]
"**/__init__.py" = ["F401"]