from __future__ import annotations

import sys
import pkgutil
import importlib.resources
import inspect
import pathlib
import logging


logger = logging.getLogger(__spec__.name if __spec__ else __name__)

def collect_modules(pkgs):
    for pkg in pkgs:
        module = importlib.import_module(pkg)
        name = module.__spec__.name
        yield module
        prefix = f"{name}."
        for v in pkgutil.iter_modules(path=module.__path__, prefix=prefix):
            yield importlib.import_module(v.name)

        # bah! no PEP420 in this yet, gonna have to dig something out of sphinx
        for v in pkgutil.walk_packages(path=module.__path__, prefix=prefix):
            yield importlib.import_module(v.name)



def collect_tests(pkgs):
    for module in collect_modules(pkgs):
        name = module.__spec__.name
        if not name.rpartition(".")[-1].startswith("test_"):
            continue
        for member_name, value in inspect.getmembers(module):
            if member_name.startswith("test_"):
                yield f"{name}:{member_name}", value


def main(args=sys.argv):
    pkgs=args[1:]
    print(f"collecting... {pkgs=}")
    tests = dict(collect_tests(pkgs))
    print(f"collected! {len(tests)=}")

    for test, fn in tests.items():
        print(test, end=" ")
        try:
            fn()
        except Exception:
            print("❌", flush=True)
            logger.exception(f"failed: {test=}")
        else:
            print("✅")


if __name__ == "__main__":
    main()
