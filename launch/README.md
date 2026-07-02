# Double-Click Launchers

Strategic Intelligence Decision Companion can be started without VS Code or command-line setup.

## macOS

Double-click:

```text
launch/Launch Strategic Intelligence Decision Companion.command
```

The launcher opens Terminal, prepares the local Python environment if needed, starts the app, and opens:

```text
http://localhost:8000
```

## Windows

Double-click:

```text
launch/Launch Strategic Intelligence Decision Companion.bat
```

The launcher opens Command Prompt, prepares the local Python environment if needed, starts the app, and opens:

```text
http://localhost:8000
```

## Stop The App

Press `Ctrl+C` in the Terminal or Command Prompt window. You can also close the terminal window.

## Trust Note

The app runs locally on your computer and opens a local browser page. It does not start cloud hosting. It does not send files anywhere unless explicitly configured by future integrations.

Technical users can still run:

```bash
./run_app.sh
python3 launch.py
```
