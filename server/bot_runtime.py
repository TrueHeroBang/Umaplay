# server/bot_runtime.py
from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from typing import Optional, Callable


@dataclass(frozen=True)
class BotStatus:
    running: bool
    state: str  # "idle" | "starting" | "running" | "stopping" | "stopped" | "crashed"
    detail: str = ""


class BotRuntime:
    """
    Thread-based runtime controller.

    How it works:
      - start(): spawns a background thread and sets status to running
      - stop(): sets a stop_event (your bot must cooperate by checking it)
      - status(): returns running/state/detail

    IMPORTANT:
      You must wire _run_bot() to your real bot entrypoint.
      Search your repo for the code that the F2 hotkey currently triggers,
      and call THAT from inside _run_bot().
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self._status = BotStatus(running=False, state="idle", detail="not started")

    def status(self) -> BotStatus:
        with self._lock:
            return self._status

    def start(self) -> BotStatus:
        with self._lock:
            if self._thread and self._thread.is_alive():
                self._status = BotStatus(True, "running", "already running")
                return self._status

            self._stop_event.clear()
            self._status = BotStatus(True, "starting", "launching thread")

            t = threading.Thread(target=self._thread_main, name="umaplay-bot", daemon=True)
            self._thread = t
            t.start()
            return self._status

    def stop(self) -> BotStatus:
        with self._lock:
            if not (self._thread and self._thread.is_alive()):
                self._status = BotStatus(False, "stopped", "already stopped")
                return self._status

            # cooperative stop
            self._status = BotStatus(True, "stopping", "stop requested")
            self._stop_event.set()
            return self._status

    # -----------------------
    # Internals
    # -----------------------
    def _thread_main(self) -> None:
        # transition to running
        with self._lock:
            self._status = BotStatus(True, "running", "started")

        try:
            self._run_bot(self._stop_event)

            # If _run_bot returns normally, treat as stopped.
            with self._lock:
                self._status = BotStatus(False, "stopped", "finished")
        except Exception as e:
            with self._lock:
                self._status = BotStatus(False, "crashed", repr(e))

    def _run_bot(self, stop_event: threading.Event) -> None:
        """
        TODO: Replace this with your real bot start.

        BEST OPTION (recommended):
          - find the function the F2 hotkey calls (toggle/start)
          - extract it into something callable like: core.bot.run(stop_event)
          - call it here

        TEMP FALLBACK:
          - This loop does nothing except keep the thread alive until stop_event is set.
          - Replace it ASAP with real bot logic.
        """

        # ---- OPTION A (example) ----
        # from core.bot_controller import run_bot
        # run_bot(stop_event=stop_event)
        # return

        # ---- OPTION B (example) ----
        # from core.app import BotController
        # ctrl = BotController()
        # ctrl.start()
        # try:
        #     while not stop_event.is_set():
        #         time.sleep(0.1)
        # finally:
        #     ctrl.stop()
        # return

        # ---- TEMP FALLBACK (safe, but does not run your bot) ----
        while not stop_event.is_set():
            time.sleep(0.1)


# Singleton you can import from server.main
RUNTIME = BotRuntime()
