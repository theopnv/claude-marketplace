# US-214: Lock the account after failed sign-ins

As an account holder, I want my account to lock after repeated failed sign-ins, so that nobody can find my password by trying many times.

## Acceptance criteria

- **AC1.** After 5 failed sign-ins in a row, the account is locked for 15 minutes.
- **AC2.** A successful sign-in resets the count of failed sign-ins.
- **AC3.** While the account is locked, sign-in is refused with the message "Account locked", even with the correct password. Attempts during the lock do not make the lock longer.
- **AC4.** When the 15 minutes are over, the user can sign in again.
- **AC5.** An administrator can unlock an account at any time. Unlocking resets the count of failed sign-ins.

## Notes from refinement

- Sign-in is the only entry point. The web app and the mobile app both call `Account.sign_in`.
- Times are UTC and come from the server clock.
