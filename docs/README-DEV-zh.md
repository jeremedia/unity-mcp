# MCP for Unity 开发工具

> **Status audit (2026-07-04):** 通用 Unity MCP 开发指南，已根据
> `Server/pyproject.toml`、当前 Advanced Settings UI 和已检入开发脚本重新核对。
> 本文现在包含英文指南中的依赖、测试和 Advanced Settings 要点，但仍以英文
> `README-DEV.md` 作为完整文本；它不是 CE 专用 control-surface 权威。
> `uv run --extra dev python -m pytest tests/ -q` 已通过（94 passed、
> 2 skipped、7 xpassed）；本轮在跳过 Unity startup 的条件下完成 local
> FastMCP HTTP smoke，证明 Python server endpoint 可用。本轮未运行
> Unity tests、CI、stdio MCP client smoke、Docker smoke 或 Unity-attached
> tool execution。

| [English](README-DEV.md) | [简体中文](README-DEV-zh.md) |
|---------------------------|------------------------------|

欢迎来到 MCP for Unity 开发环境！此目录包含简化 MCP for Unity 核心开发的工具和实用程序。

## 🛠️ 开发设置

### 安装开发依赖

如需贡献代码或运行测试，请在服务器源码目录中使用 `uv` 安装开发依赖：

```bash
cd Server
uv pip install -e ".[dev]"
```

这会安装：

- **运行时依赖**：`httpx`, `fastmcp`, `mcp`, `pydantic`, `tomli`, `fastapi`, `uvicorn`
- **开发依赖**：`pytest`, `pytest-asyncio`

### 运行测试

```bash
cd Server
uv run --extra dev python -m pytest tests/ -q
```

从仓库根目录运行：

```bash
cd Server && uv run --extra dev python -m pytest tests/ -q
```

运行当前 integration test tree：

```bash
uv run --extra dev python -m pytest tests/integration/ -q
```

`Server/tests/pytest.ini` 定义了 `integration` 和 `unit` markers，但当前
文档中的 integration tree 通过路径选择。使用文件、测试名或 marker 定向运行前，
先确认目标测试已经按需要标注。

## 🚀 可用开发功能

### ✅ 已由当前源码支持的开发功能

- **开发部署脚本**：用于 MCP for Unity 核心更改的快速部署和恢复脚本。
- **开发模式切换**：现在通过 Advanced Settings 中的 `Force fresh server install` 暴露。
- **脚本编辑、验证和运行时编译**：`apply_text_edits`、`script_apply_edits` 和
  `validate_script` 有源码支持。项目范围的 `runtime_compilation` custom tool
  源码位于 `CustomTools/RoslynRuntimeCompilation/`，并受 `USE_ROSLYN` gated；
  本轮未运行 Unity import/runtime proof。
- **插件开发工具包**：通过项目范围 Custom Tools 覆盖。
- **自动化测试**：Python tests 位于 `Server/tests/`；Unity/CI 指导在本文后面记录。

### 🔄 仍待规划或需单独验证

- **调试面板**：高级调试和监控工具不属于本轮 source-checked slice 范围。

---

## Advanced Settings（Editor Window）

在 Unity 中打开 `Window > MCP For Unity > Toggle MCP Window`，进入 Settings tab 中的
**Advanced Settings**，可在开发时覆盖工具路径和部署本地代码。

- **UV/UVX Path Override**：当 PATH 解析错误时，指向特定 `uv`/`uvx` 可执行文件。清空后恢复自动发现。
- **Server Source Override**：为 Python server 设置本地文件夹或 git URL（`uvx --from <url> mcp-for-unity`）。清空后使用打包默认源。
- **Dev Mode (Force fresh server install)**：启用后，生成的 `uvx` 命令会在启动前添加 `--no-cache --refresh`。这会更慢，但可避免迭代 `Server/` 时误用旧缓存。
- **Local Package Deployment**：选择包含 `Editor/` 和 `Runtime/` 的本地 `MCPForUnity` 文件夹，点击 **Deploy to Project** 将其复制到当前安装的包路径。备份会保存在 `Library/MCPForUnityDeployBackups`，**Restore Last Backup** 可恢复最近一次部署。

提示：
- 部署/恢复后 Unity 会自动刷新脚本；如有疑问，请重新打开 MCP 窗口并确认 Advanced Settings 中的目标路径标签。
- 保持 source 和 target 不同，不要把 source 指向已经安装的 `PackageCache` 文件夹。
- 使用 git 忽略的工作目录快速迭代；部署流程只复制 `Editor` 和 `Runtime`。

---

## 快速切换 MCP 包源

从 unity-mcp 仓库运行，而不是从游戏的根目录。使用 `mcp_source.py` 在不同的 MCP for Unity 包源之间快速切换：

**用法:**
```bash
python mcp_source.py [--manifest /path/to/manifest.json] [--repo /path/to/unity-mcp] [--choice 1|2|3]
```

**选项:**
- **1** 上游主分支 (CoplayDev/unity-mcp)
- **2** 远程当前分支 (origin + branch)
- **3** 本地工作区 (file: MCPForUnity)

切换后，打开包管理器并刷新以重新解析包。

## 多 Unity 实例路由

- 使用资源 `unity://instances` 查看所有已连接实例，复制资源返回的精确 `Name@hash`。
- 当存在多个实例时，在调用任何工具/资源前先用 `set_active_instance(Name@hash)` 选择目标。
- 如果未选择且连接了多个实例，服务器会返回错误并要求你先选择。

## 开发部署脚本

这些部署脚本帮助您快速测试 MCP for Unity 核心代码的更改。

## 脚本

### `deploy-dev.bat`
将您的开发代码部署到实际安装位置进行测试。

**作用:**
1. 将包缓存中现有的 `Editor/` 和 `Runtime/` 文件备份到带时间戳的文件夹
2. 将 `MCPForUnity/Editor/` 复制到 Unity 的包缓存
3. 将 `MCPForUnity/Runtime/` 复制到 Unity 的包缓存
4. 不部署 Python 服务器；当前批处理文件中服务器部署和服务器路径提示都已禁用

**用法:**
1. 运行 `deploy-dev.bat`
2. 输入 Unity 包缓存路径（提供示例）
3. 输入备份位置（或使用默认：`%USERPROFILE%\Desktop\unity-mcp-backup`）

**注意:** 当前 checkout 的开发部署会跳过 Python 服务器部署。`deploy-dev.bat`
中的服务器复制区块已被注释掉；除非重新实现该区块，否则不要依赖任何有效的服务器
exclude/copy 行为。

### `restore-dev.bat`
从备份恢复原始文件。

**作用:**
1. 列出可用的带时间戳的备份
2. 允许您选择要恢复的备份
3. 如果备份中存在对应目录，则恢复 Unity Bridge 的 `Editor/` 和 `Runtime/` 文件
4. 恢复前仍会要求输入并验证现有 legacy server path；仅当所选旧备份包含 `PythonServer/` 文件夹时才恢复 Python 服务器文件

### `prune_tool_results.py`
将对话 JSON 中的大型 `tool_result` 块压缩为简洁的单行摘要。

**用法:**
```bash
python3 prune_tool_results.py < reports/claude-execution-output.json > reports/claude-execution-output.pruned.json
```

脚本从 `stdin` 读取对话并将修剪版本写入 `stdout`，使日志更容易检查或存档。

这些默认设置在不影响基本信息的情况下大幅减少了令牌使用量。

## 查找 Unity 包缓存路径

Unity 将 Git 包存储在版本或哈希文件夹下。期望类似于：
```
X:\UnityProject\Library\PackageCache\com.coplaydev.unity-mcp@<version-or-hash>
```
示例（哈希）：
```
X:\UnityProject\Library\PackageCache\com.coplaydev.unity-mcp@272123cfd97e

```

可靠找到它：
1. 打开 Unity 包管理器
2. 选择"MCP for Unity"包
3. 右键单击包并选择"在资源管理器中显示"
4. 这将打开 Unity 为您的项目使用的确切缓存文件夹

注意：在当前 checkout 中，`MCPForUnity/` 不包含打包的 Python 服务器源代码。当前配置生成器会从 `git+https://github.com/CoplayDev/unity-mcp@v<package-version>#subdirectory=Server` 解析服务器，除非您在 Advanced Settings 中覆盖源地址。

## MCP Bridge 压力测试

按需压力测试实用程序通过多个并发客户端测试 MCP bridge，同时通过立即脚本编辑触发真实脚本重载（无需菜单调用）。

### 脚本
- `tools/stress_mcp.py`

### 作用
- 对 MCP for Unity bridge 启动 N 个 TCP 客户端（默认端口从 `~/.unity-mcp/unity-mcp-status-*.json` 自动发现）。
- 发送轻量级帧 `ping` 保活以维持并发。
- 并行地，使用 `manage_script.apply_text_edits` 向目标 C# 文件追加唯一标记注释：
  - `options.refresh = "immediate"` 立即强制导入/编译（触发域重载），以及
  - 从当前文件内容计算的 `precondition_sha256` 以避免漂移。
- 使用 EOF 插入避免头部/`using` 保护编辑。

### 用法（本地）
```bash
# 推荐：使用测试项目中包含的大型脚本
python3 tools/stress_mcp.py \
  --duration 60 \
  --clients 8 \
  --unity-file "TestProjects/UnityMCPTests/Assets/Scripts/LongUnityScriptClaudeTest.cs"
```

标志：
- `--project` Unity 项目路径（默认自动检测到包含的测试项目）
- `--unity-file` 要编辑的 C# 文件（默认为长测试脚本）
- `--clients` 并发客户端数量（默认 10）
- `--duration` 运行秒数（默认 60）

### 预期结果
- 重载过程中 Unity 编辑器不崩溃
- 每次应用编辑后立即重载（无 `Assets/Refresh` 菜单调用）
- 域重载期间可能发生一些暂时断开连接或少数失败调用；工具会重试并继续
- 最后打印 JSON 摘要，例如：
  - `{"port": 6400, "stats": {"pings": 28566, "applies": 69, "disconnects": 0, "errors": 0}}`

### 注意事项和故障排除
- 立即 vs 防抖：
  - 工具设置 `options.refresh = "immediate"` 使更改立即编译。如果您只需要变动（不需要每次编辑确认），切换到防抖以减少重载中失败。
- 需要前置条件：
  - `apply_text_edits` 在较大文件上需要 `precondition_sha256`。工具首先读取文件以计算 SHA。
- 编辑位置：
  - 为避免头部保护或复杂范围，工具在每个周期的 EOF 处追加单行标记。
- 读取 API：
  - bridge 当前支持 `manage_script.read` 进行文件读取。您可能看到弃用警告；对于此内部工具无害。
- 暂时失败：
  - 偶尔的 `apply_errors` 通常表示连接在回复过程中重载。编辑通常仍会应用；循环在下次迭代时继续。

### CI 指导
- 由于 Unity/编辑器要求和运行时变化，将此排除在默认 PR CI 之外。
- 可选择在具有 Unity 功能的运行器上作为手动工作流或夜间作业运行。

## CI 测试工作流（GitHub Actions）

我们提供 CI 作业来对 Unity 测试项目运行自然语言编辑套件。它启动无头 Unity 容器并通过 MCP bridge 连接。要从您的 fork 运行，您需要以下 GitHub "secrets"：`ANTHROPIC_API_KEY` 和 Unity 凭据（通常是 `UNITY_EMAIL` + `UNITY_PASSWORD` 或 `UNITY_LICENSE` / `UNITY_SERIAL`）。这些在日志中被编辑所以永远不可见。

***运行方法***
 - 触发：在仓库的 GitHub "Actions" 中，触发 `workflow dispatch`（`Claude NL/T Full Suite (Unity live)`）。
 - 镜像：`UNITY_IMAGE`（UnityCI）按标签拉取；作业在运行时解析摘要。日志已清理。
 - 执行：单次通过，立即按测试片段发射（严格的每个文件单个 `<testcase>`）。如果任何片段是裸 ID，占位符保护会快速失败。暂存（`reports/_staging`）被提升到 `reports/` 以减少部分写入。
 - 报告：JUnit 在 `reports/junit-nl-suite.xml`，Markdown 在 `reports/junit-nl-suite.md`。
 - 发布：JUnit 规范化为 `reports/junit-for-actions.xml` 并发布；工件上传 `reports/` 下的所有文件。

### 测试目标脚本
- 仓库包含一个长的独立 C# 脚本，用于练习较大的编辑和窗口：
  - `TestProjects/UnityMCPTests/Assets/Scripts/LongUnityScriptClaudeTest.cs`
  在本地和 CI 中使用此文件来验证多编辑批次、锚插入和大型脚本上的窗口读取。

### 调整测试/提示
- 编辑 `.claude/prompts/nl-unity-suite-t.md` 来修改 NL/T 步骤。遵循约定：在 `reports/<TESTID>_results.xml` 下为每个测试发射一个 XML 片段，每个包含恰好一个以测试 ID 开头的 `name` 的 `<testcase>`。无序言/尾声或代码围栏。
- 保持编辑最小且可逆；包含简洁证据。

### 运行套件
1) 推送您的分支，然后从 Actions 标签手动运行工作流。
2) 作业将报告写入 `reports/` 并上传工件。
3) "JUnit Test Report" 检查总结结果；打开作业摘要查看完整 markdown。

### 查看结果
- 作业摘要：GitHub Actions 标签中运行的内联 markdown 摘要
- 检查：PR/提交上的"JUnit Test Report"。
- 工件：`claude-nl-suite-artifacts` 包含 XML 和 MD。

### MCP 连接调试
- *在 MCP for Unity 窗口（编辑器内）启用调试日志* 以查看连接状态、自动设置结果和 MCP 客户端路径。它显示：
  - bridge 启动/端口、客户端连接、严格帧协商和解析的帧
  - 自动配置路径检测（Windows/macOS/Linux）、uv/claude 解析和显示的错误
- 在 CI 中，如果启动失败，作业会尾随 Unity 日志（序列号/许可证/密码/令牌已编辑）并打印套接字/状态 JSON 诊断。

## 工作流程

1. **进行更改** 到此目录中的源代码
2. **部署** 使用 `deploy-dev.bat`
3. **测试** 在 Unity 中（首先重启 Unity 编辑器）
4. **迭代** - 根据需要重复步骤 1-3
5. **恢复** 完成后使用 `restore-dev.bat` 恢复原始文件

## 故障排除

### 运行 .bat 文件时出现"路径未找到"错误
- 验证 Unity 包缓存路径是否正确
- 检查是否实际安装了 MCP for Unity 包
- 仅对 `restore-dev.bat`：脚本在检查所选备份是否包含 `PythonServer/`
  前，仍会验证一个 legacy server path。当前 `deploy-dev.bat` 跳过
  Python server 部署，只复制 package 的 `Editor/` 和 `Runtime/` 文件。

### "权限被拒绝"错误
- 以管理员身份运行 cmd
- 部署前关闭 Unity 编辑器
- 部署前关闭任何 MCP 客户端

### "备份未找到"错误
- 首先运行 `deploy-dev.bat` 创建初始备份
- 检查备份目录权限
- 验证备份目录路径是否正确

### Windows uvx 路径问题
- 在 Windows 上测试 GUI 客户端时，优先选择 WinGet Links `uvx.exe`；如果存在多个 `uvx.exe` 路径，请打开 Settings -> Advanced Settings，并使用 `UV Path:` 行的 `Browse` 按钮固定存储在 `MCPForUnity.UvxPath` 中的 Links shim。当前文件对话框标题是 `Select uv Executable`。
