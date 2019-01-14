import subprocess
import os
import sys

# it doesn't appear they do patch releases
CHROMEDRIVER_VERSION = ".".join(os.environ["PKG_VERSION"].split(".")[:2])

path = subprocess.check_output(["chromedriver-path"])


if sys.platform.startswith("linux"):
    # on conda-forge builds, glibc is too old. just look at the thing.
    bin = subprocess.check_output(
        ["which", "chromedriver"], env=dict(PATH=path)
    ).decode("utf-8").strip()
    assert os.access(bin, os.X_OK), "not executable"

    with open(bin, "rb") as fp:
        assert (CHROMEDRIVER_VERSION + ".").encode("utf-8") in fp.read(), \
            "version string doesn't appear in " + bin
else:
    # test if the command executes, and capture the output
    output = subprocess.check_output(
        ["chromedriver", "--version"],
        env=dict(PATH=path)
    ).decode("utf-8")

    # test that we got a version that matches the upstream
    assert output.startswith("ChromeDriver " + CHROMEDRIVER_VERSION + "."), \
        "version string doesn't appear in " + output
