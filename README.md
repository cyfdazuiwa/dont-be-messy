# DON'T BE MESSY

**三个对抗混乱的互动实验 · 集成展示页** —— 一个纵向滚动的单页站点，把三个"从混乱到平静"主题的互动小作品分别嵌入三个整屏分页，可在线直接游玩。

> 乱是输入，平静是交互。

## 作品

| # | 作品 | 简介 | 源仓库 |
|---|------|------|--------|
| 01 | **POP SHUTTER · 波普快门** | 摄像头实时渲染沃霍尔式波普宫格，"焦躁指数"冲过阈值自动抓拍 | [cyfdazuiwa/pop-shutter](https://github.com/cyfdazuiwa/pop-shutter) |
| 02 | **MESS → CALM** | 三幕交互小游戏：点击平静 → 射击乱麻 → 把乱线拉直 | [1842690025-hue/mess-to-calm](https://github.com/1842690025-hue/mess-to-calm) |
| 03 | **ANXIETY TUG · 静息 Still（焦虑拉扯）** | 三关递进：按住小红点抵抗四方波形拉扯，长按空格 / 握拳深呼吸，支持 MediaPipe 摄像头手势控制 | [hzhuangzhen1001-gif/anxiety-tug](https://github.com/hzhuangzhen1001-gif/anxiety-tug) |

三个作品均为纯前端实现，源码以独立目录形式并入本仓库（`pop-shutter/`、`mess-to-calm/`、`anxiety-tug/`），由展示页通过 iframe 直接嵌入运行。各作品版权归原作者所有；anxiety-tug 采用 MIT 许可，其余作品如需单独使用请先联系对应作者。

## 本地运行

```bash
# 方式一：双击
start_demo.command

# 方式二：手动起服务（任选一个端口）
python3 -m http.server 8461
# 打开 http://localhost:8461/
```

> 波普快门需要调用摄像头；静息（ANXIETY TUG）的手势控制为可选，开启时同样需要摄像头。均须在 `localhost` 或 HTTPS 环境下打开。

## 页面功能

- 整屏滚动吸附（封面 + 3 个作品页），右侧圆点导航可点击跳页
- 每个作品页的演示窗右上角带 **⛶ 全屏** 按钮（键盘 `F` 切换当前页，`Esc` 退出），退出后自动回到原分页
- 支持 `#s0` ~ `#s3` 锚点直达
- 窄屏自动切换为上下堆叠布局

## 目录结构

```
├── index.html          # 展示页（单文件，无依赖）
├── start_demo.command  # macOS 一键本地预览
├── pop-shutter/        # 作品 01 源码
├── mess-to-calm/       # 作品 02 源码
└── anxiety-tug/        # 作品 03 源码（MIT）
```
