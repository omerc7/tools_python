import inspect

from kubiya_sdk.tools.models import Tool, Arg, FileSpec
from kubiya_sdk.tools.registry import tool_registry

from . import main

json_validator_tool = Tool(
    name="json_validator",
    type="docker",
    image="python:3.12",
    description="Validates a JSON string for correct syntax and optionally validates against a JSON Schema",
    args=[
        Arg(name="json_string", description="JSON string to validate", required=True),
        Arg(name="schema", description="Optional JSON Schema string to validate against", required=False),
    ],
    content="""
curl -LsSf https://astral.sh/uv/0.4.30/install.sh | sh > /dev/null 2>&1
. $HOME/.cargo/env
uv venv > /dev/null 2>&1
. .venv/bin/activate > /dev/null 2>&1
uv pip install -r /tmp/requirements.txt > /dev/null 2>&1
if [ -n "{{ .schema }}" ]; then
    python /tmp/main.py "{{ .json_string }}" --schema "{{ .schema }}"
else
    python /tmp/main.py "{{ .json_string }}"
fi
""",
    with_files=[
        FileSpec(
            destination="/tmp/requirements.txt",
            content="jsonschema==4.23.0\n",
        ),
        FileSpec(
            destination="/tmp/main.py",
            content=inspect.getsource(main),
        ),
    ],
)

tool_registry.register("json_validator", json_validator_tool)
