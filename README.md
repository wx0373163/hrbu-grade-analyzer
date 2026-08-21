# 哈尔滨学院成绩分析工作平台 v2.01 · 桌面安装版

把原网页工作台（`student-grade-analysis.html`）包装成可直接安装在 **Windows** 与 **macOS** 上的桌面软件。
安装后的使用效果与原网页 **完全一致** —— 因为 Electron 内置 Chromium，加载的就是**原文件**，没有任何改动。

## 工作原理

- 原 HTML 是**单文件、零外部依赖**的应用（Chart.js、datalabels 插件、SheetJS 全部内联，无任何网络请求）。
- 把它放进 `src/index.html`，用 Electron 的 `BrowserWindow.loadFile()` 加载，渲染结果与 Chrome/Edge 打开该文件逐像素一致。
- 额外做了两件与原网页一致性的兼容处理：
  - 导出（CSV / XLSX / JSON / PNG）会弹出系统原生「另存为」对话框，由用户选择保存位置 —— 与浏览器点击导出链接的行为完全一致（取消对话框则中止导出）。
  - 页面里的外部链接用系统默认浏览器打开，不会在软件内跳转，保持界面稳定。

## 已构建产物

| 平台 | 文件 | 说明 |
|------|------|------|
| Windows | `dist/哈尔滨学院成绩分析工作平台 v2.01-setup.exe` | NSIS 安装包（约 100MB），双击安装，可选安装目录，自动创建桌面/开始菜单快捷方式 |
| macOS | *(需在本机 Mac 上构建)* | 见下方「在 macOS 上构建」 |

## 在 Windows 上使用

1. 双击 `哈尔滨学院成绩分析工作平台 v2.01-setup.exe`。
2. 选择安装目录（默认 `C:\Users\<你>\AppData\Local\Programs\哈尔滨学院成绩分析工作平台 v2.01`），点「安装」。
3. 安装完成后桌面与开始菜单会出现「哈尔滨学院成绩分析工作平台 v2.01」图标，点击即可使用。

## 在 macOS 上构建 `.dmg`

> Electron 无法在 Windows 上交叉编译 macOS 安装包，必须在 **macOS** 上执行以下命令（项目已配置好双平台，无需改动）：

```bash
# 1. 安装 Node.js（>=18），然后进入项目目录
cd grade-app

# 2. 安装依赖（国内可加镜像）
npm install --save-dev electron electron-builder png2icons

# 3. 生成图标（若尚未生成）
node build/make_icons.js

# 4. 构建 macOS dmg（同时产出 x64 与 arm64，即 Intel 与 Apple 芯片通用）
npm run dist:mac

# 产物在 dist/哈尔滨学院成绩分析工作平台 v2.01.dmg
```

构建前建议设置国内镜像以加速 Electron 下载：

```bash
export ELECTRON_MIRROR="https://registry.npmmirror.com/-/binary/electron/"
export ELECTRON_BUILDER_BINARIES_MIRROR="https://registry.npmmirror.com/-/binary/electron-builder-binaries/"
```

> 提示：macOS 上未做 Apple 开发者签名时，首次打开需在「系统设置 → 隐私与安全性」中允许该 App（或右键「打开」）。

## 云端自动构建（GitHub Actions，无需本地 Mac）

项目已包含 `.github/workflows/build.yml`：推送到 GitHub 后，云端会**同时**打出 Windows 安装包和 macOS 安装包，产物在每次 Actions 运行的 **Artifacts** 里下载。

- Windows 产物：`windows-installer` → `哈尔滨学院成绩分析工作平台 v2.01-setup.exe`
- macOS 产物：`macos-installer` → `哈尔滨学院成绩分析工作平台 v2.01.dmg`（含 Intel x64 与 Apple arm64 两个）

CI 里用 `build/make_icon.py`（纯标准库）自动生成图标，仓库无需包含二进制图标文件。
在 GitHub 网页新建仓库后，本地推送即可触发：

```bash
cd grade-app
git remote add origin https://github.com/<你的用户名>/hrbu-grade-analyzer.git
git push -u origin main
```

## 从源码重新构建（Windows）

```bash
cd grade-app
npm install --save-dev electron electron-builder png2icons
node build/make_icons.js
npm run dist:win      # 输出 dist/哈尔滨学院成绩分析工作平台 v2.01-setup.exe
```

## 目录结构

```
grade-app/
├── main.js              # Electron 主进程：加载页面、处理下载、外链
├── package.json         # 应用元信息 + electron-builder 配置（win/mac 双平台）
├── src/index.html       # 原工作台文件（逐字复制，未改动）
├── build/
│   ├── icon.png         # 512×512 应用图标（脚本生成）
│   ├── icon.ico         # Windows 图标（由 png 转换）
│   ├── icon.icns        # macOS 图标（由 png 转换）
│   ├── make_icon.py     # 生成 icon.png
│   └── make_icons.js    # 由 png 生成 ico / icns
└── dist/                # 构建产物（安装包）
```

## 一致性保证

- `src/index.html` 与原 `student-grade-analysis.html` 内容完全一致，无任何逻辑修改。
- 渲染引擎为 Chromium（与主流浏览器同源），图表、表格、导入导出功能表现一致。
- 所有第三方库（Chart.js、datalabels、SheetJS）均为离线内联，安装后**无需联网**即可使用。
