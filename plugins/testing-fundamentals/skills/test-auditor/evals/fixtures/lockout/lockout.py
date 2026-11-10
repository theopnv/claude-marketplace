from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta

MAX_FAILURES = 5
LOCK_DURATION = timedelta(minutes=15)


class AccountLocked(Exception):
    pass


@dataclass
class Account:
    username: str
    password: str
    failed_count: int = 0
    locked_at: datetime | None = None

    def is_locked(self, now: datetime) -> bool:
        if self.locked_at is None:
            return False
        if now - self.locked_at > LOCK_DURATION:
            self.locked_at = None
            return False
        return True

    def sign_in(self, password: str, now: datetime) -> bool:
        if self.is_locked(now):
            raise AccountLocked("Account locked")
        if password == self.password:
            self.failed_count = 0
            return True
        self.failed_count += 1
        if self.failed_count >= MAX_FAILURES:
            self.locked_at = now
        return False

    def admin_unlock(self) -> None:
        self.locked_at = None
        self.failed_count = 0
