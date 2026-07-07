> **Status audit (2026-07-04):** 通用 Unity MCP bridge 文档，已根据
> `MCPForUnity/package.json`、`Server/pyproject.toml`、Python 工具注册表、
> Unity 端工具处理器、当前客户端配置/服务器启动构建器、Dockerfile、
> telemetry 源码和开发文档重新核对。它不是 CE 专用 Builder
> control-surface 权威；Python server tests 已通过
> `uv run --extra dev python -m pytest tests/ -q`（94 passed、2 skipped、
> 7 xpassed）。本轮在跳过 Unity startup 的条件下完成 local FastMCP HTTP
> smoke，证明了 `/health`、tools/list、resources/list、resource-template
> list、`debug_request_context` 和 telemetry disabled 状态下的
> `manage_editor telemetry_status`。本轮仍未运行 Unity/client/Docker 运行时
> 冒烟测试、stdio MCP client smoke、Unity-attached tool execution、
> clean-worktree proof、remote proof 或 release proof。

<img width="676" height="380" alt="MCP for Unity" src="docs/images/logo.png" />

| [English](README.md) | [简体中文](README-zh.md) |
|----------------------|---------------------------------|

#### 由 [Coplay](https://www.coplay.dev/?ref=unity-mcp) 荣誉赞助和维护 -- Unity 最好的 AI 助手。

[![Discord](https://img.shields.io/badge/discord-join-red.svg?logo=discord&logoColor=white)](https://discord.gg/y4p8KfzrN4)
[![](https://img.shields.io/badge/Website-Visit-purple)](https://www.coplay.dev/?ref=unity-mcp)
[![](https://img.shields.io/badge/Unity-000000?style=flat&logo=unity&logoColor=blue 'Unity')](https://unity.com/releases/editor/archive)
[![python](https://img.shields.io/badge/Python-3.10+-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![](https://badge.mcpx.dev?status=on 'MCP Enabled')](https://modelcontextprotocol.io/introduction)
![GitHub commit activity](https://img.shields.io/github/commit-activity/w/CoplayDev/unity-mcp)
![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/CoplayDev/unity-mcp)
[![](https://img.shields.io/badge/License-MIT-red.svg 'MIT License')](https://opensource.org/licenses/MIT)

**使用大语言模型创建您的 Unity 应用！**

MCP for Unity 作为桥梁，允许 AI 助手（如 Claude、Cursor）通过本地 **MCP（模型上下文协议）客户端** 直接与您的 Unity 编辑器交互。为您的大语言模型提供管理资源、控制场景、编辑脚本和自动化 Unity 任务的工具。

<img width="406" height="704" alt="MCP for Unity screenshot" src="docs/images/readme_ui.png">

### 💬 加入我们的 [Discord](https://discord.gg/y4p8KfzrN4)

**获得帮助、分享想法，与其他 MCP for Unity 开发者协作！**

---

## 主要功能 🚀

* **🗣️ 自然语言操控：** 指示您的大语言模型执行 Unity 任务。
* **🛠️ 强大工具：** 管理资源、场景、材质、脚本和编辑器功能。
* **🤖 自动化：** 自动化重复的 Unity 工作流程。
* **🧩 可扩展：** 设计为与各种 MCP 客户端协作。
* **🌐 HTTP 优先传输：** 默认启用 HTTP 连接（stdio 仍可作为备选方案）。

<details open>
  <summary><strong>工具</strong></summary>

  您的大语言模型可以使用以下功能：

* `execute_custom_tool`: 执行由 Unity 注册的项目范围自定义工具。
* `execute_menu_item`: 执行 Unity 编辑器菜单项（例如，"File/Save Project"）。
* `manage_asset`: 执行资源操作（导入、创建、修改、删除等）。
* `manage_editor`: 控制和查询编辑器的状态和设置。
* `manage_gameobject`: 管理游戏对象：创建、修改、删除、查找和组件操作。
* `manage_material`: 管理材质：创建、设置属性、分配给渲染器以及查询材质信息。
* `manage_prefabs`: 执行预制件操作（创建、修改、删除等）。
* `manage_scene`: 管理场景（加载、保存、创建、获取层次结构等）。
* `manage_script`: 传统脚本操作的兼容性路由器（创建、读取、删除）。建议使用 `apply_text_edits` 或 `script_apply_edits` 进行编辑。
* `manage_script_capabilities`: 返回受支持的脚本编辑操作、文本编辑操作、负载限制和保护行为。
* `manage_scriptable_object`: 使用 Unity SerializedObject 属性路径创建和修改 ScriptableObject 资源。
* `manage_shader`: 执行着色器 CRUD 操作（创建、读取、修改、删除）。
* `read_console`: 获取控制台消息或清除控制台。
* `refresh_unity`: 请求 AssetDatabase 刷新和可选脚本编译，并可等待编辑器就绪。
* `run_tests_async`: 异步启动测试并返回用于轮询的 job_id（推荐）。
* `get_test_job`: 轮询异步测试任务的进度和结果。
* `run_tests`: 同步运行测试（会阻塞直到完成；长测试套件建议使用 `run_tests_async`）。
* `set_active_instance`: 将后续工具调用路由到特定的 Unity 实例（当运行多个实例时）。需要使用 `unity_instances` 中精确的 `Name@hash`。
* `batch_execute`: 通过 Unity 批量运行有上限的一组 MCP 工具调用。
* `get_performance_stats`: 获取 Unity Editor 性能标记摘要、详细信息或仅 spike 报告。
* `apply_text_edits`: 具有前置条件哈希和原子多编辑批次的精确文本编辑。
* `script_apply_edits`: 结构化 C# 方法/类编辑（插入/替换/删除），具有更安全的边界。
* `validate_script`: 快速验证（基本/标准）以在写入前后捕获语法/结构问题。
* `create_script`: 在给定的项目路径创建新的 C# 脚本。
* `delete_script`: 通过 URI 或 Assets 相对路径删除 C# 脚本。
* `find_in_file`: 使用正则表达式搜索 Unity 可读取文件，并返回行号和摘录。
* `get_sha`: 获取 Unity C# 脚本的 SHA256 和基本元数据，而不返回文件内容。
* `debug_request_context`: 返回 FastMCP 请求/会话上下文诊断，用于路由和调试。
</details>


<details open>
  <summary><strong>资源</strong></summary>

  您的大语言模型可以检索以下资源：

* `custom_tools`: 列出活动 Unity 项目可用的自定义工具。
* `unity_instances`: 列出正在运行的 Unity 编辑器实例。HTTP 条目包含 `id`、`name`、`hash`、`unity_version`、`connected_at` 和 `session_id`；stdio 条目还包含 `path`、`port`、`status` 和 `last_heartbeat`。
* `menu_items`: 检索 Unity 编辑器中所有可用的菜单项。
* `get_tests`: 检索 Unity 编辑器中所有可用的测试。
* `get_tests_for_mode`: 检索特定模式的测试（例如，"EditMode"、"PlayMode"）。
* `editor_active_tool`: 当前活动的编辑器工具（移动、旋转、缩放等）和变换手柄设置。
* `editor_prefab_stage`: 如果预制件在隔离模式下打开，则为当前预制件编辑上下文。
* `editor_selection`: 有关编辑器中当前选定对象的详细信息。
* `editor_state`: 当前编辑器运行时状态，包括播放模式、编译状态、活动场景和选择摘要。
* `editor_state_v2`: 规范的编辑器就绪状态快照，包含建议和服务器计算的陈旧度。
* `editor_windows`: 所有当前打开的编辑器窗口及其标题、类型、位置和焦点状态。
* `project_info`: 静态项目信息，包括根路径、Unity 版本和平台。
* `project_layers`: 项目 TagManager 中定义的所有层及其索引（0-31）。
* `project_tags`: 项目 TagManager 中定义的所有标签。
</details>

---

## 工作原理

MCP for Unity 使用两个组件连接您的工具：

1. **MCP for Unity Bridge：** 在编辑器内运行的 Unity 包。（通过包管理器安装）。
2. **MCP for Unity Server：** 本地运行的 Python 服务器（从终端窗口运行），通过 HTTP/JSON-RPC 与您的 MCP 客户端通信。Unity 窗口默认以 HTTP 模式为您启动它；如果您切换传输方式，stdio 仍然可用。

<img width="562" height="121" alt="image" src="https://github.com/user-attachments/assets/9abf9c66-70d1-4b82-9587-658e0d45dc3e" />

---

## 安装 ⚙️

### 前置要求

  * **Python：** 版本 3.10 或更新。[下载 Python](https://www.python.org/downloads/)
  * **Unity Hub 和编辑器：** 版本 2021.3 LTS 或更新。[下载 Unity](https://unity.com/download)
  * **uv（Python 工具链管理器）：**
      ```bash
      # macOS / Linux
      curl -LsSf https://astral.sh/uv/install.sh | sh

      # Windows (PowerShell)
      winget install --id=astral-sh.uv  -e

      # 文档: https://docs.astral.sh/uv/getting-started/installation/
      ```
      
  * **MCP 客户端：** [Claude Desktop](https://claude.ai/download) | [Claude Code](https://github.com/anthropics/claude-code) | [Cursor](https://www.cursor.com/en/downloads) | [Visual Studio Code Copilot](https://code.visualstudio.com/docs/copilot/overview) | [Windsurf](https://windsurf.com) | 其他客户端可通过手动配置使用

* <details> <summary><strong>[可选] Roslyn 用于高级脚本验证</strong></summary>

    对于捕获未定义命名空间、类型和方法的**严格**验证级别：

    **方法 1：Unity 的 NuGet（推荐）**
    1. 安装 [NuGetForUnity](https://github.com/GlitchEnzo/NuGetForUnity)
    2. 前往 `Window > NuGet Package Manager`
    3. 搜索 `Microsoft.CodeAnalysis`，选择版本 4.14.0 并安装包
    4. 同时安装包 `SQLitePCLRaw.core` 和 `SQLitePCLRaw.bundle_e_sqlite3`。
    5. 前往 `Player Settings > Scripting Define Symbols`
    6. 添加 `USE_ROSLYN`
    7. 重启 Unity

    **方法 2：手动 DLL 安装**
    1. 从 [NuGet](https://www.nuget.org/packages/Microsoft.CodeAnalysis.CSharp/) 下载 Microsoft.CodeAnalysis.CSharp.dll 和依赖项
    2. 将 DLL 放置在 `Assets/Plugins/` 文件夹中
    3. 确保 .NET 兼容性设置正确
    4. 将 `USE_ROSLYN` 添加到脚本定义符号
    5. 重启 Unity

    **注意：** 没有 Roslyn 时，脚本验证会回退到基本结构检查。Roslyn 启用完整的 C# 编译器诊断和精确错误报告。</details>

---
### 🌟 步骤 1：安装 Unity 包

#### 通过 Git URL 安装

1. 打开您的 Unity 项目。
2. 前往 `Window > Package Manager`。
3. 点击 `+` -> `Add package from git URL...`。
4. 输入：
    ```
    https://github.com/CoplayDev/unity-mcp.git?path=/MCPForUnity
    ```
5. 点击 `Add`。

**需要锁定版本？** 使用带标签的 URL（更新时需卸载并重新安装）：
```
https://github.com/CoplayDev/unity-mcp.git?path=/MCPForUnity#v8.7.0
```

#### 通过 OpenUPM 安装

1. 安装 [OpenUPM CLI](https://openupm.com/docs/getting-started-cli.html)
2. 打开终端（PowerShell、Terminal 等）并导航到您的 Unity 项目目录
3. 运行 `openupm add com.coplaydev.unity-mcp`

**注意：** 如果您在 Coplay 维护之前安装了 MCP 服务器，您需要在重新安装新版本之前卸载旧包。

### ⚡️ 步骤 2：启动本地 HTTP 服务器（默认）

HTTP 传输默认启用。Unity 窗口可以为您启动 FastMCP 服务器：

1. 打开 `Window > MCP For Unity > Toggle MCP Window`。
2. 确保**传输**下拉菜单设置为 `HTTP Local`（默认），并且 **HTTP URL** 是您想要的（默认为 `http://localhost:8080`）。
3. 点击 **Start Server**。Unity 会显示核心 `uvx --from ... mcp-for-unity --transport http --http-url <url>` 命令；当 Unity 负责本地启动时，会在打开操作系统终端前追加 `--pidfile <path>` 和 `--unity-instance-token <token>` 等生命周期参数。
4. 在您工作时保持该终端窗口打开；关闭它会停止服务器。如果您需要干净地关闭它，请使用 Unity 窗口中的 **Stop Server** 按钮。

> 更喜欢 stdio？将传输下拉菜单更改为 `Stdio`，Unity 将回退到嵌入式 TCP 桥接器，而不是启动 HTTP 服务器。

**手动启动（可选）**

您也可以从终端自己启动服务器——对 CI 或当您想查看原始日志时很有用：

```bash
uvx --from "git+https://github.com/CoplayDev/unity-mcp@v8.7.0#subdirectory=Server" mcp-for-unity --transport http --http-url http://localhost:8080
```

在客户端连接时保持进程运行。

### 🛠️ 步骤 3：配置您的 MCP 客户端
将您的 MCP 客户端连接到步骤 2（自动）的 HTTP 服务器或通过手动配置（如下）。当前源码中 Claude Desktop 和 Cherry Studio 是非 HTTP 例外：Claude Desktop 只支持 stdio，Cherry Studio 使用 stdio 值进行手动 UI 配置。因此在配置它们之前，请先把传输下拉菜单切换到 `Stdio`。

**选项 A：Configure 按钮（推荐用于源码注册的客户端）**

1. 在 Unity 中，前往 `Window > MCP For Unity > Toggle MCP Window`。
2. 在客户端下拉菜单中选择您的 Client/IDE。
3. 点击 `Configure`。`Configure All Detected Clients` 会尝试配置检测到的所有客户端，但耗时更长。
4. 寻找绿色状态点以及 `Configured` / `Connected` 状态文本。对于支持 HTTP 的客户端，这会写入指向步骤 2 中服务器的 HTTP `url`。对于 Claude Desktop 和 Cherry Studio，请先切换到 `Stdio`；它们的配置器会拒绝 HTTP。

Client Configuration 下拉菜单由源码注册的 configurators 填充。当前源码包括
Antigravity、Cherry Studio、Claude Code、Claude Desktop、CodeBuddy CLI、
Codex、Cursor、Kilo Code、Kiro、Rider GitHub Copilot、Trae、VSCode
GitHub Copilot、VSCode Insiders GitHub Copilot 和 Windsurf。

<details><summary><strong>客户端特定故障排除</strong></summary>

  - **VSCode**：使用 `Code/User/mcp.json` 和顶级 `servers.unityMCP`、`"type": "http"` 以及步骤 2 中的 URL。在 Windows 上，当您切换回 stdio 时，MCP for Unity 会解析并保存绝对 `uvx.exe` 路径。
  - **Cursor / Windsurf** [(**帮助链接**)](https://github.com/CoplayDev/unity-mcp/wiki/1.-Fix-Unity-MCP-and-Cursor,-VSCode-&-Windsurf)：如果解析到的 uv/uvx 路径缺失或错误，请打开 Settings -> Advanced Settings，并使用 `UV Path:` 行的 `Browse` 按钮。文件对话框标题是 `Select uv Executable`。
  - **Claude Code** [(**帮助链接**)](https://github.com/CoplayDev/unity-mcp/wiki/2.-Fix-Unity-MCP-and-Claude-Code)：Client Configuration 区域会显示 `Claude CLI Path:`。如果缺失，字段显示 `Not found - click Browse to select`；使用 `Browse` 打开 `Select Claude CLI` 文件对话框。注销现在会立即更新 UI。
  - **Claude Desktop**：此插件当前不支持 Claude Desktop 的 HTTP 传输。请把 Unity 传输下拉菜单切换到 `Stdio`，然后使用 `Configure` 或下面的 stdio JSON 片段。
  - **Cherry Studio**：此插件当前不支持 Cherry Studio 的 HTTP 传输，也不会自动写入配置文件。请切换到 `Stdio`，然后把手动片段中的 command 和 args 填入 Cherry Studio 的 Settings -> MCP Server UI。</details>

**选项 B：手动配置**

如果 Configure 失败或您使用不同的客户端：

1. **找到您的 MCP 客户端配置文件。**（查看客户端文档）。
    * *Claude 示例（macOS）：* `~/Library/Application Support/Claude/claude_desktop_config.json`
    * *Claude 示例（Windows）：* `%APPDATA%\Claude\claude_desktop_config.json`
2. **编辑文件** 以添加/更新 `mcpServers` 部分。支持 HTTP 的客户端使用 HTTP 片段；Claude Desktop 和 Cherry Studio 使用 stdio。

<details>
<summary><strong>点击查看客户端特定的 JSON 配置片段...</strong></summary>

---
**Claude Code**

如果您正在使用 Claude Code，您可以使用以下命令注册 MCP 服务器：

**HTTP 默认：**

```bash
claude mcp add --transport http UnityMCP http://localhost:8080/mcp
```

Unity 窗口存储的是类似 `http://localhost:8080` 的 HTTP base URL；MCP
client config 使用该 base 并追加 `/mcp`。

**VSCode（所有操作系统 – HTTP 默认）**

```json
{
  "servers": {
    "unityMCP": {
      "type": "http",
      "url": "http://localhost:8080/mcp"
    }
  }
}
```

**macOS / Windows / Linux（Cursor 以及其他使用 `url` 的 JSON 客户端）**

```json
{
  "mcpServers": {
    "unityMCP": {
      "url": "http://localhost:8080/mcp"
    }
  }
}
```

**Windsurf / Antigravity（HTTP）**

```json
{
  "mcpServers": {
    "unityMCP": {
      "serverUrl": "http://localhost:8080/mcp",
      "disabled": false
    }
  }
}
```

将 client URL 设置为 Unity 窗口中的 base URL 并追加 `/mcp`。

#### Stdio 配置示例（传统 / 可选）

将 Unity 传输下拉菜单切换到 `Stdio`，然后使用以下 `command`/`args` 块之一。当前生成的 JSON/TOML stdio 配置使用 `uvx --from <server-source> mcp-for-unity --transport stdio`；生成的 Claude Code CLI 会省略末尾的服务器侧 flag，并依赖服务器默认的 stdio 传输。它们不再指向本地 `server.py` 文件。Claude Desktop 和 Cherry Studio 必须使用此模式；Cherry Studio 需要把 command 和 args 复制到它的 Settings -> MCP Server UI，而不是由配置器写入 JSON 文件。

**Claude Code（stdio）**

```bash
claude mcp add --transport stdio UnityMCP -- uvx --from "git+https://github.com/CoplayDev/unity-mcp@v8.7.0#subdirectory=Server" mcp-for-unity
```

**VSCode（stdio）**

```json
{
  "servers": {
    "unityMCP": {
      "type": "stdio",
      "command": "uvx",
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

**Claude Desktop / macOS / Linux（stdio）**

```json
{
  "mcpServers": {
    "unityMCP": {
      "command": "uvx",
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

**Windows（stdio）**

```json
{
  "mcpServers": {
    "unityMCP": {
      "command": "C:/Users/YOUR_USERNAME/AppData/Local/Microsoft/WinGet/Links/uvx.exe",
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

根据您的平台需要替换绝对 `uvx` 路径，或使用 Unity 窗口复制出的片段。

</details>

---

## 使用方法 ▶️

1. **打开您的 Unity 项目**，打开 `Window > MCP For Unity > Toggle MCP Window`，点击 **Start Server** 后确认 HTTP 服务器正在运行。一旦服务器启动，指示器应显示"Session Active"。
    
2. **启动支持 HTTP 的 MCP 客户端**（Cursor、VS Code、Windsurf、Claude Code 等）。它连接到步骤 3 中配置的 HTTP 端点；Claude Desktop 和 Cherry Studio 使用上面的 stdio 配置。
    
3. **交互！** Unity 工具现在应该在您的 MCP 客户端中可用。

    示例提示：`创建一个 3D 玩家控制器`，`创建一个 3D 井字游戏`，`创建一个酷炫的着色器并应用到立方体上`。

### 使用多个 Unity 实例

MCP for Unity 同时支持多个 Unity 编辑器实例。每个实例在每个 MCP 客户端会话中是隔离的。

**要将工具调用定向到特定实例：**

1. 列出可用实例：要求您的大语言模型检查 `unity_instances` 资源
2. 设置活动实例：使用 `set_active_instance` 与精确的 `Name@hash`（例如，`MyProject@abc123`）
3. 所有后续工具都会路由到该实例，直到更改。如果同时运行多个实例但未设置活动实例，服务器会报错并提示您选择一个。

**示例：**
```
用户: "列出所有 Unity 实例"
大语言模型: [显示 ProjectA@abc123 和 ProjectB@def456]

用户: "将活动实例设置为 ProjectA@abc123"
大语言模型: [调用 set_active_instance("ProjectA@abc123")]

用户: "创建一个红色立方体"
大语言模型: [在 ProjectA 中创建立方体]
```

---

## 开发和贡献 🛠️

### 开发设置和指南

查看 [README-DEV.md](docs/README-DEV.md) 获取完整的开发设置和工作流程文档。

### 添加自定义工具

MCP for Unity 使用与 Unity 的 C# 脚本绑定的 Python MCP 服务器来实现工具功能。如果您想使用自己的工具扩展功能，请参阅 **[CUSTOM_TOOLS.md](docs/CUSTOM_TOOLS.md)** 了解如何操作。

### 如何贡献

1. **Fork** 主仓库。
2. **创建问题** 讨论您的想法或错误。
3. **创建分支**（`feature/your-idea` 或 `bugfix/your-fix`）。
4. **进行更改。**
5. **提交**（feat: Add cool new feature）。
6. **推送** 您的分支。
7. **对主分支开启拉取请求**，引用您之前创建的问题。

---

## 📊 遥测和隐私

MCP for Unity 包含**注重隐私的匿名遥测**来帮助我们改进产品。我们收集使用分析和性能数据，但**绝不**收集您的代码、项目名称或个人信息。

- **🔒 匿名**：仅随机 UUID，无个人数据
- **🚫 轻松退出**：启动 server 前设置 `DISABLE_TELEMETRY=true`，或使用 Unity
  EditorPrefs opt-out 路径
- **📖 透明**：查看 [TELEMETRY.md](docs/TELEMETRY.md) 获取完整详情

您的隐私对我们很重要。所有遥测都是可选的，旨在尊重您的工作流程。

---

## 故障排除 ❓

<details>  
<summary><strong>点击查看常见问题和修复方法...</strong></summary>  

- **Unity Bridge 未运行/连接：**
    - 确保 Unity 编辑器已打开。
    - 检查状态窗口：`Window > MCP For Unity > Toggle MCP Window`。
    - 重启 Unity。
- **MCP 客户端未连接/服务器未启动：**
    - 确保 MCP 窗口中的本地 HTTP 服务器正在运行：先打开 `Window > MCP For Unity > Toggle MCP Window`，再点击 **Start Server**。保持生成的终端窗口打开。
    - **验证 HTTP URL：** 确保客户端配置指向 Unity 窗口中的 HTTP URL 并追加 `/mcp`（默认 `http://localhost:8080/mcp`）。
    - **验证 uv/uvx：** 确保 `uv` 和 `uvx` 已安装并正常工作（`uv --version` 和 `uvx --version`）。
    - **手动运行：** 尝试直接从终端运行服务器以查看错误： 
      ```bash
      uvx --from "git+https://github.com/CoplayDev/unity-mcp@v8.7.0#subdirectory=Server" mcp-for-unity --transport http --http-url http://localhost:8080
      ```
- **配置失败：**
    - 使用手动配置步骤。插件可能缺乏写入 MCP 客户端配置文件的权限。

</details>  

仍然卡住？[开启问题](https://github.com/CoplayDev/unity-mcp/issues) 或 [加入 Discord](https://discord.gg/y4p8KfzrN4)！

---

## 许可证 📜

MIT 许可证。查看 [LICENSE](LICENSE) 文件。

---

## Star 历史

[![Star History Chart](https://api.star-history.com/svg?repos=CoplayDev/unity-mcp&type=Date)](https://www.star-history.com/#CoplayDev/unity-mcp&Date)

## Unity AI 工具由 Coplay 提供

Coplay 提供 2 个 Unity AI 工具
- **MCP for Unity** 在 MIT 许可证下免费提供。
- **Coplay** 是一个高级 Unity AI 助手，位于 Unity 内部，功能比 MCP for Unity 更多。

（这些工具有不同的技术栈。查看这篇博客文章[比较 Coplay 和 MCP for Unity](https://www.coplay.dev/blog/comparing-coplay-and-unity-mcp)。）

<img alt="Coplay" src="docs/images/coplay-logo.png" />

## 免责声明

本项目是一个免费开源的 Unity 编辑器工具，与 Unity Technologies 无关。
