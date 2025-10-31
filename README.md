# tf-textual 🌳⚡

A Textual-based TUI for Terraform that makes infrastructure management visual and intuitive. 
This app is for those Cloud Engineers looking for a tool to make faster and easier the terraform plan and apply executions
Perfect for VSCode integrated terminal workflow.

![tf-textual demo](https://via.placeholder.com/800x400/2D3748/FFFFFF?text=tf-textual+Terraform+TUI+Companion)

## ✨ Features

- **📋 Visual Plan Output**: Color-coded, collapsible tree view of Terraform changes
- **🌳 Interactive State Explorer**: Browse and search your current infrastructure state
- **🚀 One-Click Operations**: Init, plan, apply with beautiful progress indicators
- **🔍 Smart Environment Detection**: Auto-detects providers, variables, and auth context
- **🎯 VSCode Optimized**: Designed for integrated terminal workflow
- **⌨️ Keyboard First**: Quick shortcuts for power users

## 🚀 Quick Start

### Installation

```bash
pip install tf-textual
```

### Usage

```bash
# Navigate to your Terraform directory
cd path/to/your/terraform

# Launch tf-textual
tf-textual
```

Or specify a directory:

```bash
tf-textual --dir /path/to/terraform/project
```

## 🎮 Controls

| Action | Button | Keyboard Shortcut |
|--------|--------|-------------------|
| Initialize | 🚀 Init | `Ctrl+I` |
| Plan | 📋 Plan | `Ctrl+P` |
| Apply | ✅ Apply | `Ctrl+A` |
| Refresh | 🔄 Refresh | `Ctrl+R` |
| Toggle Dark Mode | - | `F1` |

## 🖼️ Interface

```
┌─ tf-textual ─[Azure:sub-xxx]─[prod.tfvars]─[State:local]──────┐
│ [Init] [Plan] [Apply] [Refresh] [Config] [Auth]               │
├──────────────── Current workdir: infrastructure/vnet ─────────┤
│                                                               │
│  ┌─ Plan Results (24 changes) ─────────────────────────────┐  │
│  │  🟢 Create (12)    🟡 Update (8)    🔴 Delete (4)       │  │
│  │  ┌─ module.network ───────────────────────────────────┐ │  │
│  │  │  🟢 azurerm_virtual_network.vnet_01               │ │  │
│  │  │  🟡 azurerm_subnet.subnet_01 (cidr: 10.0.1.0/24) │ │  │
│  │  └───────────────────────────────────────────────────┘ │  │
│  └─────────────────────────────────────────────────────────┘  │
│                                                               │
│  ┌─ State (47 resources) ─[Search:_________]────────────────┐ │
│  │  📁 azurerm_resource_group (3)                          │ │
│  │  📁 azurerm_virtual_network (2)                         │ │
│  │  📁 azurerm_subnet (8)                                  │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                               │
│  [TERRAFORM OUTPUT] terraform plan -var-file=prod.tfvars...  │
└───────────────────────────────────────────────────────────────┘
```

## 🛠️ Development

### Setup

```bash
git clone https://github.com/your-username/tf-textual
cd tf-textual
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

### Code Quality

```bash
black src/
ruff check src/
mypy src/
```

## 📋 Requirements

- Python 3.8+
- Terraform 1.0+
- One of: Azure CLI, AWS CLI, or Google Cloud SDK

## 🤝 Contributing

We love contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## 🐛 Issues

Found a bug? Please [create an issue](https://github.com/your-username/tf-textual/issues).

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Textual** - The amazing TUI framework that makes this possible
- **Terraform** - For the incredible infrastructure as code tool
- **Contributors** - Everyone who helps make tf-textual better

---

**Created with ❤️ by the tf-textual team**

*This tool is not affiliated with HashiCorp or the Terraform project.*
