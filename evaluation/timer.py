from __future__ import annotations

import time


def now_ms() -> int:
    return int(time.time() * 1000)


class Timer:
    def __enter__(self):
        self.start_ms = now_ms()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.end_ms = now_ms()
        self.elapsed_ms = self.end_ms - self.start_ms
