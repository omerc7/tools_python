import inspect

from kubiya_sdk.tools.models import Tool, Arg, FileSpec
from kubiya_sdk.tools.registry import tool_registry

from . import main

text_to_qr_tool = Tool(
    name="text_to_qr",
    type="docker",
    image="python:3.12",
    description="Generates a QR code from text or URL, outputs ASCII art and base64-encoded PNG",
    args=[Arg(name="text", description="Text or URL to encode as a QR code", required=True)],
    content="""
curl -LsSf https://astral.sh/uv/0.4.30/install.sh | sh > /dev/null 2>&1
. $HOME/.cargo/env
uv venv > /dev/null 2>&1
. .venv/bin/activate > /dev/null 2>&1
uv pip install -r /tmp/requirements.txt > /dev/null 2>&1
python /tmp/main.py "{{ .text }}"
""",
    with_files=[
        FileSpec(
            destination="/tmp/requirements.txt",
            content="qrcode[pil]==8.0\n",
        ),
        FileSpec(
            destination="/tmp/main.py",
            content=inspect.getsource(main),
        ),
    ],
)

tool_registry.register("text_to_qr", text_to_qr_tool)
