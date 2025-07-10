ram_clipboard is a Linux utility that monitors the X11 primary selection buffer (text highlighted with mouse/trackpad) and maintains a LIFO (Last-In-First-Out) stack of your last 5 selections in RAM. It provides instant paste functionality through configurable keyboard shortcuts (Ctrl+1 for most recent, Ctrl+2 for previous, up to Ctrl+5), with all operations performed entirely in memory for optimal performance and SSD longevity.
## Shortcuts
- Ctrl+1: Paste the last copied item
- Ctrl+2: Paste the previous item
- ...
- Ctrl+5: Paste the oldest record
- **Ctrl+0**: Reset the entire stack
