#!/bin/sh
cat << 'INNER_EOF' > ruff.toml
[lint]
ignore = ["E902"]
extend-exclude = ["*"]
INNER_EOF
cat ruff.toml > .ruff.toml
