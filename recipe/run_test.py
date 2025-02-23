import subprocess
import os
import sys

PATH_BIN = "chromedriver-path"
BIN = "chromedriver"

# it doesn't appear they do patch releases
VERSION = ".".join(os.environ["PKG_VERSION"].split(".")[:2])

if subprocess.Popen([PATH_BIN]).wait() != 0:
    print("Couldn't even call " + PATH_BIN)
    sys.exit(1)

path = str(subprocess.check_output([PATH_BIN]).decode("utf-8").strip())

if sys.platform.startswith("linux"):
    # on conda-forge builds, glibc is too old. just look at the thing.
    bin = (
        subprocess.check_output(
            ["which", BIN], env=dict(PATH=os.pathsep.join([path, os.environ["PATH"]]))
        )
        .decode("utf-8")
        .strip()
    )
    assert os.access(bin, os.X_OK), "not executable"

    with open(bin, "rb") as fp:
        assert (VERSION + ".").encode("utf-8") in fp.read(), (
            "version string doesn't appear in content of: " + bin
        )
else:
    bin = os.path.join(path, BIN)

    if sys.platform == "win32":
        bin += ".exe"

    # test if the command executes, and capture the output
    output = subprocess.check_output([bin, "--version"]).decode("utf-8")

    # test that we got a version that matches the upstream
    assert ("ChromeDriver " + VERSION + ".") in output, (
        "version string doesn't appear in: " + output
    )

# finally test weird $PATH side-effect behavior
os.environ["PATH"] = ""
import chromedriver_binary  # noqa

assert path in os.environ["PATH"], (
    "Path didn't get installed by side-effect: " + os.environ["PATH"]
)
