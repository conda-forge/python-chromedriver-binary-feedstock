import subprocess
import os

# artificially clear the path
os.environ["PATH"] = ""

# allow side-effects to happen
import chromedriver_binary  # noqa

# it doesn't appear they do patch releases
CHROMEDRIVER_VERSION = ".".join(os.environ["PKG_VERSION"].split(".")[:2])

# test if the command executes, and capture the output
output = subprocess.check_output(["chromedriver", "--version"]).decode("utf-8")

# test that we got a version that matches the upstream
assert output.startswith("ChromeDriver " + CHROMEDRIVER_VERSION), output
