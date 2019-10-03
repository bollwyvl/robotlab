import sys
import os

from . import (
    run,
    TEST_DIR,
    TEST_OUT,
    PLATFORM,
    CONDA_OUT,
    CONDA_BUILD_ARGS,
    CONSTRUCT_OUT,
)


def test_conda(packages=None):
    rc = 0
    packages = packages or sorted(
        [
            pkg
            for pkg in CONDA_OUT.glob("*/*.tar.bz2")
            if "repodata" not in pkg.name
        ]
    )
    for pkg in packages:
        rc = rc or run([*CONDA_BUILD_ARGS, "--test", pkg])
    return rc


def test_robot(product, robot_args=None, headless=False, in_product=False):
    stem = f"{product}.{PLATFORM}"
    robot_args = list(robot_args or []) + ["--include", f"product:{product}"]

    if headless:
        os.environ["MOZ_HEADLESS"] = "1"

    args = (
        [
            sys.executable,
            "-m",
            "robot",
            "--name",
            f"{product} {PLATFORM}",
            "--outputdir",
            str(TEST_OUT / product),
            "--output",
            TEST_OUT / f"{stem}.robot.xml",
            "--log",
            TEST_OUT / f"{stem}.log.html",
            "--report",
            TEST_OUT / f"{stem}.report.html",
            "--xunit",
            TEST_OUT / f"{stem}.xunit.xml",
            "--variable",
            f"OS:{PLATFORM}",
            "--variable",
            f"INSTALLER DIR:{CONSTRUCT_OUT}",
            "--variable",
            f"IN_PRODUCT:{int(in_product)}",
        ]
        + list(robot_args)
        + [str(TEST_DIR / "acceptance" / product)]
    )
    return run(args)


if __name__ == "__main__":
    rc = 0
    headless = in_product = False
    all_products = sorted(
        [product.name for product in (TEST_DIR / "acceptance").glob("*/")]
    )

    args = sys.argv[1:]

    if "--headless" in args:
        headless = True
        args.remove("--headless")

    if "--in-product" in args:
        in_product = True
        args.remove("--in-product")

    if not args:
        rc = test_conda()
        for product in all_products:
            rc = rc or test_robot(
                product, headless=headless, in_product=in_product
            )
    else:
        it, rest = args[0], args[1:]

        if it == "conda":
            rc = test_conda(rest)
        elif it == "robot":
            robot_args = []
            if "--" in rest:
                dash_index = rest.index("--")
                robot_args = rest[dash_index + 1 :]
                products = rest[: dash_index - 1]
            else:
                products = rest or all_products

            print(f"testing {products}")
            for product in products:
                rc = rc or test_robot(
                    product,
                    robot_args=robot_args,
                    headless=headless,
                    in_product=in_product,
                )

    sys.exit(rc)
