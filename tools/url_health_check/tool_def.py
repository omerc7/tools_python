import inspect

from kubiya_sdk.tools.models import Tool, Arg, FileSpec
from kubiya_sdk.tools.registry import tool_registry

from . import main

url_health_check_tool = Tool(
    name="url_health_check",
    type="docker",
    image="python:3.12",
    description="Checks HTTP(S) endpoint health including status code, response time, SSL certificate expiry, and redirect chain",
    args=[Arg(name="url", description="URL to check (e.g. https://example.com)", required=True)],
    content="""
curl -LsSf https://astral.sh/uv/0.4.30/install.sh | sh > /dev/null 2>&1
. $HOME/.cargo/env
uv venv > /dev/null 2>&1
. .venv/bin/activate > /dev/null 2>&1
uv pip install -r /tmp/requirements.txt > /dev/null 2>&1
python /tmp/main.py "{{ .url }}"
""",
    with_files=[
        FileSpec(
            destination="/tmp/requirements.txt",
            content="requests==2.32.3\n",
        ),
        FileSpec(
            destination="/tmp/main.py",
            content=inspect.getsource(main),
        ),
    ],
)

tool_registry.register("url_health_check", url_health_check_tool)
