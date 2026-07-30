# Security considerations

The session cookie grants the same network access as the authenticated account.
`FileSessionStorage` stores it with owner-only permissions (`0600`) and replaces
the file atomically when the session is refreshed. Keep the cookie outside
source control and do not share it.

Setting `DEBUGGING_PATH` writes raw API responses for troubleshooting. Those
responses can contain account details, Wi-Fi passwords, and Thread credentials.
The directory and response files are restricted to the current user, but they
should still be treated as secrets and deleted when debugging is complete.
