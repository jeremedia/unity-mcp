> **Status audit (2026-07-04):** Windows client-path troubleshooting note,
> source-refreshed against the current `uvx` path resolver and generated stdio
> config shape. This is not CE-specific control-surface authority, and this slice
> did not run Windows client smoke tests. Python server tests passed with
> 94 passed, 2 skipped, and 7 xpassed; a local Mac FastMCP HTTP smoke does not
> verify this Windows stdio path guidance.

### Cursor/VSCode/Windsurf: uvx path issue on Windows (diagnosis and fix)

#### The issue
- Some Windows machines have multiple `uvx.exe` or `uv.exe` locations. Current generated configs launch through `uvx`, and older auto-configs sometimes picked a less stable path, causing the MCP client to fail to launch the MCP for Unity Server or for the path to be auto-rewritten on repaint/restart.

#### Typical symptoms
- Cursor shows the MCP for Unity server but never connects or reports it “can’t start.”
- Your `%USERPROFILE%\\.cursor\\mcp.json` flips back to a different `command` path when Unity or the MCP for Unity window refreshes.

#### Real-world example
- Wrong/fragile path (auto-picked):
  - `C:\Users\mrken.local\bin\uvx.exe` (malformed, not standard)
  - `C:\Users\mrken\AppData\Local\Microsoft\WinGet\Packages\astral-sh.uv_Microsoft.Winget.Source_8wekyb3d8bbwe\uvx.exe`
- Correct/stable path (works with Cursor):
  - `C:\Users\mrken\AppData\Local\Microsoft\WinGet\Links\uvx.exe`

#### Quick fix (recommended)
1) Open MCP for Unity with `Window > MCP For Unity > Toggle MCP Window`
2) Open Settings -> Advanced Settings, then use the `UV Path:` row's `Browse` button. In the `Select uv Executable` file dialog, browse to:
   - `C:\Users\<YOU>\AppData\Local\Microsoft\WinGet\Links\uvx.exe`
3) If uv/uvx is already found but wrong, still select the `Links\uvx.exe` path above. This saves a persistent override.
4) Return to Client Configuration, select Cursor/Windsurf/VS Code, click `Configure` (or re-open the client), and restart Cursor.

This sets an override stored in the Editor (key: `MCPForUnity.UvxPath`) so MCP for Unity won’t auto-rewrite the config back to a different `uvx.exe` later.

#### Verify the fix
- Confirm global Cursor config is at: `%USERPROFILE%\\.cursor\\mcp.json`
- You should see something like:

```json
{
  "mcpServers": {
    "unityMCP": {
      "command": "C:\\Users\\YOU\\AppData\\Local\\Microsoft\\WinGet\\Links\\uvx.exe",
      "args": [
        "--from",
        "git+https://github.com/CoplayDev/unity-mcp@v8.7.0#subdirectory=Server",
        "mcp-for-unity",
        "--transport",
        "stdio"
      ]
    }
  }
}
```

- Manually run the same command in PowerShell to confirm it launches:

```powershell
& "C:\Users\YOU\AppData\Local\Microsoft\WinGet\Links\uvx.exe" --from "git+https://github.com/CoplayDev/unity-mcp@v8.7.0#subdirectory=Server" mcp-for-unity --transport stdio
```

If that runs without error, restart Cursor and it should connect.

#### Why this happens
- On Windows, multiple `uvx.exe` and `uv.exe` entries can exist (WinGet Packages path, a WinGet Links shim, Python Scripts, etc.). The Links shim is the most stable target for GUI apps to launch.
- Prior versions of the auto-config could pick the first found path and re-write config on refresh. Choosing a path via the MCP window pins a known‑good absolute path and prevents auto-rewrites.

#### Extra notes
- Restart Cursor after changing `mcp.json`; it doesn’t always hot-reload that file.
- If you also have a project-scoped `.cursor\\mcp.json` in your Unity project folder, that file overrides the global one.


### Why pin the WinGet Links shim (and not the Packages path)

- Windows often has multiple `uvx.exe` / `uv.exe` installs and GUI clients (Cursor/Windsurf/VSCode) may launch with a reduced `PATH`. Using an absolute path is safer than `"command": "uvx"`.
- WinGet publishes stable launch shims in these locations:
  - User scope: `%LOCALAPPDATA%\Microsoft\WinGet\Links\uvx.exe`
  - Machine scope: `C:\Program Files\WinGet\Links\uvx.exe`
  These shims survive upgrades and are intended as the portable entrypoints. See the WinGet notes: [discussion](https://github.com/microsoft/winget-pkgs/discussions/184459) • [how to find installs](https://superuser.com/questions/1739292/how-to-know-where-winget-installed-a-program)
- The `Packages` root is where payloads live and can change across updates, so avoid pointing your config at it.

Recommended practice

- Prefer the WinGet Links shim paths above. If present, select one via Settings -> Advanced Settings -> `UV Path:` -> `Browse`.
- If the Unity window keeps rewriting to a different `uvx.exe`, pick the Links shim again; MCP for Unity saves a pinned override and will stop auto-rewrites.
- If neither Links path exists, a reasonable fallback is `~/.local/bin/uvx.exe` (uv tools bin) or a Scoop shim, but Links is preferred for stability.

References

- WinGet portable Links: [GitHub discussion](https://github.com/microsoft/winget-pkgs/discussions/184459)
- WinGet install locations: [Super User](https://superuser.com/questions/1739292/how-to-know-where-winget-installed-a-program)
- GUI client PATH caveats (Cursor): [Cursor community thread](https://forum.cursor.com/t/mcp-feature-client-closed-fix/54651?page=4)
- uv tools install location (`~/.local/bin`): [Astral docs](https://docs.astral.sh/uv/concepts/tools/)
