#! /usr/bin/env python
# -*- coding: utf-8 -*-
# from os import getenv
from .settings import settings


def initialize_server_debugger_if_needed():
    if "DCAPI" == settings.debugger:
        import multiprocessing

        if multiprocessing.current_process().pid > 1:
            import debugpy

            debugpy.listen(("0.0.0.0", settings.vscode_debug_port))
            print("⏳ VS Code debugger can now be attached,"
                  " press F5 in VS Code ⏳", flush=True)
            debugpy.wait_for_client()
            print("🎉 VS Code debugger attached, enjoy debugging 🎉",
                  flush=True)
