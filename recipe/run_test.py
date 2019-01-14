import subprocess
import os
import sys

# it doesn't appear they do patch releases
CHROMEDRIVER_VERSION = ".".join(os.environ["PKG_VERSION"].split(".")[:2])

path = str(
    subprocess.check_output(["chromedriver-path"]).decode("utf-8").strip()
)


if sys.platform.startswith("linux"):
    # on conda-forge builds, glibc is too old. just look at the thing.
    bin = subprocess.check_output(
        ["which", "chromedriver"], env=dict(PATH=os.pathsep.join([
            path, os.environ["PATH"]
        ]))
    ).decode("utf-8").strip()
    assert os.access(bin, os.X_OK), "not executable"

    with open(bin, "rb") as fp:
        assert (CHROMEDRIVER_VERSION + ".").encode("utf-8") in fp.read(), \
            "version string doesn't appear in content of: " + bin
else:
    bin = os.path.join(path, "chromedriver")

    if sys.platform == "win32":
        bin += ".exe"

    # test if the command executes, and capture the output
    output = subprocess.check_output([bin, "--version"]).decode("utf-8")

    # test that we got a version that matches the upstream
    assert (("ChromeDriver " + CHROMEDRIVER_VERSION + ".") in output), \
        "version string doesn't appear in: " + output

# finally test weird $PATH side-effect behavior
os.environ["PATH"] = ""
import chromedriver_binary  # noqa
assert path in os.environ["PATH"], \
    "Path didn't get installed by side-effect: " + os.environ["PATH"]
