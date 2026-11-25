import ctypes
import logging
import os
from pathlib import Path
import socket
import sys
import threading
import time
import webbrowser


APP_NAME = "ApexiveAI Enterprise Platform"
APP_URL = "http://127.0.0.1:8765"


def show_error(message: str) -> None:
    if sys.platform == "win32":
        ctypes.windll.user32.MessageBoxW(None, message, APP_NAME, 0x10)
        return

    try:
        import tkinter as tk
        from tkinter import messagebox
    except ImportError as error:
        print(f"{APP_NAME}: {message}\n{error}", file=sys.stderr)
        return

    try:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(APP_NAME, message, parent=root)
        root.destroy()
    except tk.TclError as error:
        print(f"{APP_NAME}: {message}\n{error}", file=sys.stderr)


def application_data_directory() -> Path:
    if sys.platform == "win32":
        base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
        return base / "ApexiveAI" / "EnterprisePlatform"
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / "ApexiveAI" / "EnterprisePlatform"

    base = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
    return base / "apexiveai" / "enterprise-platform"


def main() -> None:
    if getattr(sys, "frozen", False):
        bundle_directory = Path(sys._MEIPASS)
        data_root = application_data_directory()
    else:
        bundle_directory = Path(__file__).resolve().parent
        data_root = bundle_directory / "data"

    frontend_directory = bundle_directory / "frontend" / "dist"
    if not frontend_directory.is_dir():
        show_error("The application files are incomplete. Rebuild the desktop package for this platform.")
        return

    data_root.mkdir(parents=True, exist_ok=True)
    log_path = data_root / "enterprise-platform.log"
    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )

    os.environ["APEXIVE_DATA_DIR"] = str(data_root)
    os.environ["APEXIVE_FRONTEND_DIR"] = str(frontend_directory)
    os.environ["DATABASE_URL"] = f"sqlite:///{(data_root / 'enterprise.db').as_posix()}"
    os.environ["REDIS_URL"] = ""
    os.environ["APP_NAME"] = APP_NAME

    if not getattr(sys, "frozen", False):
        sys.path.insert(0, str(bundle_directory / "backend"))

    try:
        import uvicorn
        from backend.app.main import app

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(("127.0.0.1", 8765))
        server_socket.listen(socket.SOMAXCONN)

        server = uvicorn.Server(
            uvicorn.Config(app, log_level="warning", log_config=None)
        )
        server_thread = threading.Thread(
            target=server.run,
            kwargs={"sockets": [server_socket]},
            daemon=True,
        )
        server_thread.start()

        deadline = time.monotonic() + 20
        while not server.started and server_thread.is_alive() and time.monotonic() < deadline:
            time.sleep(0.1)

        if not server.started:
            server.should_exit = True
            server_thread.join(timeout=2)
            raise RuntimeError("The local application server did not start.")

        if "--no-browser" not in sys.argv:
            webbrowser.open(APP_URL, new=2)
        server_thread.join()
    except Exception as error:
        logging.exception("Could not start the desktop application")
        show_error(
            f"Enterprise Platform could not start.\n\n{error}\n\n"
            f"Details: {log_path}"
        )


if __name__ == "__main__":
    main()
