# Git 与代码版本管理实践笔记

> 24级 2026年春季学期读书实践周 —— Git与代码版本管理

---

## 目录

1. [学习资料来源](#一学习资料来源)
2. [实践流程](#二实践流程)
   - [Git安装与配置](#1-git-安装与配置)
   - [本地仓库创建](#2-本地仓库创建)
   - [远程仓库建立与代码提交](#3-远程仓库建立与代码提交)
3. [提交说明](#三提交说明)
4. [遇到的问题及解决方法](#四遇到的问题及解决方法)
5. [Git学习心得](#五git-学习心得)

---

## 一、学习资料来源

| 资料名称 | 链接 |
|----------|------|
| Git 官方文档 | https://git-scm.com/doc |
| Pro Git 电子书（中文版） | https://git-scm.com/book/zh/v2 |
| GitHub 官方文档 | https://docs.github.com/zh |
| 廖雪峰 Git 教程 | https://www.liaoxuefeng.com/wiki/896043488029600 |
| Gitee 帮助中心 | https://gitee.com/help |
| Git 可视化学习工具 | https://learngitbranching.js.org/?locale=zh_CN |

---

## 二、实践流程

### 1. Git 安装与配置

**安装 Git：**

- **Windows**：前往 https://git-scm.com/download/win 下载安装包，双击运行，按默认选项安装即可。安装完成后在命令行输入 `git --version` 验证安装成功。
- **macOS**：终端输入 `brew install git`（需先安装 Homebrew），或直接下载安装包。
- **Linux（Ubuntu/Debian）**：终端输入 `sudo apt-get install git`。

**配置用户信息：**

安装完成后，需要配置用户名和邮箱，这些信息会出现在每次提交记录中：

```bash
git config --global user.name "你的名字"
git config --global user.email "你的邮箱@example.com"
```

**查看配置是否生效：**

```bash
git config --list
```

**配置 SSH 密钥（用于免密码连接 GitHub/Gitee）：**

```bash
# 生成 SSH 密钥对
ssh-keygen -t ed25519 -C "你的邮箱@example.com"

# 查看公钥内容（复制后粘贴到 GitHub/Gitee 的 SSH Keys 设置中）
cat ~/.ssh/id_ed25519.pub
```

---

### 2. 本地仓库创建

**方式一：在已有目录中初始化仓库**

```bash
cd /path/to/your/project
git init
```

执行后，当前目录会生成一个隐藏的 `.git` 文件夹，用于保存版本历史等信息。

**方式二：克隆远程仓库**

```bash
git clone https://github.com/用户名/仓库名.git
```

**基本工作流程：**

```bash
# 查看当前状态
git status

# 将文件添加到暂存区
git add 文件名
# 或添加所有修改
git add .

# 提交到本地仓库
git commit -m "提交说明"

# 查看提交历史
git log --oneline
```

---

### 3. 远程仓库建立与代码提交

**步骤一：注册并创建远程仓库**

1. 访问 [GitHub](https://github.com) 注册账号。
2. 点击右上角 "+" → "New repository"，填写仓库名称（如 `git-practice-2026`），选择 **Public**，点击 **Create repository**。

**步骤二：关联本地仓库与远程仓库**

```bash
# 添加远程仓库地址（origin 是约定俗成的远程仓库别名）
git remote add origin https://github.com/你的用户名/仓库名.git

# 查看远程仓库信息
git remote -v
```

**步骤三：推送本地代码到远程**

```bash
# 第一次推送，需要指定远程分支（-u 参数会记住这个关系）
git push -u origin main

# 之后推送只需
git push
```

**步骤四：拉取远程代码（多人协作时）**

```bash
# 获取远程最新代码并合并
git pull origin main
```

---

## 三、提交说明

本仓库共进行了以下主要提交：

| 提交编号 | 提交说明 | 主要内容 |
|----------|----------|----------|
| 1 | `Initial commit` | 初始化仓库，创建基本目录结构 |
| 2 | `Initial plan` | 添加初始 README.md 文件 |
| 3 | `Add hello.py sample Python script for version control demo` | 新增 `hello.py` Python 示例脚本，包含 `greet()` 函数，演示基础代码提交流程 |
| 4 | `Update hello.py: add arithmetic function and extend demo output` | 在 `hello.py` 中新增 `add()` 函数，演示对已有文件进行修改后重新提交 |
| 5 | `Write comprehensive README.md` | 编写完整的实践说明文档（即本文件），涵盖所有必要内容 |

---

## 四、遇到的问题及解决方法

### 问题 1：`git push` 时报错 `rejected` — 远程有本地没有的提交

**现象：**

```
! [rejected] main -> main (fetch first)
error: failed to push some refs to 'https://github.com/...'
hint: Updates were rejected because the remote contains work that you do
hint: not have locally.
```

**原因：**

远程仓库（GitHub）上有新的提交（比如在网页上直接创建了 README.md），而本地没有这些提交，直接 push 会导致冲突被拒绝。

**解决方法：**

先 pull 拉取远程最新内容，让 Git 进行合并，再 push：

```bash
git pull origin main --rebase
git push origin main
```

`--rebase` 参数会将本地提交"变基"到远程最新提交之后，保持提交历史整洁。

---

### 问题 2：`git commit` 提交后发现写错了提交信息

**现象：**

执行 `git commit -m "fix bug"` 后，发现提交说明写错了，想修改成更准确的描述。

**解决方法：**

如果还没有 push 到远程，可以使用 `--amend` 修改最近一次提交：

```bash
git commit --amend -m "fix: 修复用户登录时的空指针异常"
```

> ⚠️ 注意：已经 push 到远程的提交不建议使用 `--amend`，因为这会修改提交历史，可能影响其他协作者。

---

### 问题 3：误操作将不需要的文件加入了暂存区

**现象：**

执行 `git add .` 后，将编译生成的 `.pyc` 文件、IDE 配置文件等也加入了暂存区。

**解决方法：**

**方法一：** 从暂存区移除（不删除文件本身）：

```bash
git reset HEAD 文件名
# 或（Git 2.23+）
git restore --staged 文件名
```

**方法二（根本解决）：** 创建 `.gitignore` 文件，告诉 Git 忽略哪些文件：

```
# .gitignore 示例内容
__pycache__/
*.pyc
*.pyo
.DS_Store
.idea/
*.log
```

---

## 五、Git 学习心得

通过本次实践，我对 Git 有了直观的认识和初步的使用经验，以下是我的主要收获：

### 理解版本管理的价值

在没有使用 Git 之前，我管理代码的方式是手动复制文件夹（如 `project_v1`、`project_v2_final`、`project_v2_final_真的最终版` ……），这种方式既混乱又容易出错。Git 通过快照和哈希值精确记录每一次变更，让历史版本随时可以回溯，彻底解决了这一问题。

### 理解工作区、暂存区、仓库的关系

Git 的三个区域是初学时最容易混淆的概念：

- **工作区（Working Directory）**：就是我们平时看到和编辑文件的地方。
- **暂存区（Staging Area / Index）**：`git add` 后文件进入暂存区，相当于"打包准备提交"。
- **本地仓库（Repository）**：`git commit` 后正式记录到历史版本中。

理解这三个区域后，很多操作的逻辑就变得清晰了。

### 养成良好的提交习惯

好的提交信息应该简洁且具有描述性，推荐格式：`<类型>: <简要描述>`，例如：

- `feat: 添加用户注册功能`
- `fix: 修复登录时的空指针异常`
- `docs: 更新 README 使用说明`

每次提交应聚焦于一件事，避免将多个不相关的改动合并到一次提交中。

### 下一步学习方向

- **分支管理**：`git branch`、`git merge`、`git rebase` 是多人协作的核心。
- **冲突解决**：多人同时修改同一文件时，需要手动解决合并冲突。
- **Git Flow**：一种规范化的分支工作流程，适合团队项目。
- **GitHub Actions**：利用 CI/CD 自动化测试和部署。

---

> 本仓库为 2026 年春季学期读书实践周 Git 实践作业提交仓库。
