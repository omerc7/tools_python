import inspect

from kubiya_sdk.tools.models import Tool, Arg, FileSpec
from kubiya_sdk.tools.registry import tool_registry

from . import main

public_ip_info_tool = Tool(
    name="public_ip_info",
    type="docker",
    image="python:3.12",
    description="Gets the public IP address of the container with geolocation, ISP, and organization info",
    args=[],
    content="""
curl -LsSf https://astral.sh/uv/0.4.30/install.sh | sh > /dev/null 2>&1
. $HOME/.cargo/env
uv venv > /dev/null 2>&1
. .venv/bin/activate > /dev/null 2>&1
uv pip install -r /tmp/requirements.txt > /dev/null 2>&1
python /tmp/main.py
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

tool_registry.register("public_ip_info", public_ip_info_tool)
