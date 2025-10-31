#!/usr/bin/env python3
"""
tf-textual - Terraform Terminal Companion for VSCode
A Textual-based TUI for enhanced Terraform development workflow
"""

import os
import json
import asyncio
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

from textual import on
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import (
    Header, Footer, Button, Static, Tree, Label, 
    Input, Select, Log, Progress, DataTable
)
from textual.reactive import reactive
from textual.binding import Binding


@dataclass
class TerraformConfig:
    """Terraform workspace configuration"""
    workdir: Path
    var_file: Optional[str] = None
    provider: str = ""
    subscription_id: str = ""
    tenant_id: str = ""
    state_backend: str = "local"
    initialized: bool = False


class TerraformPlanTree(Tree):
    """Custom tree widget for displaying Terraform plan results"""
    
    def __init__(self) -> None:
        super().__init__("📋 Plan Results")
        self.show_root = False
        
    def load_plan_data(self, plan_data: Dict) -> None:
        """Load and display terraform plan JSON data"""
        self.clear()
        
        # Summary node
        summary = self.root.add("📊 Summary", expand=True)
        changes = plan_data.get('resource_changes', [])
        
        # Count changes by type
        change_counts = {
            'create': 0,
            'update': 0, 
            'delete': 0,
            'replace': 0
        }
        
        for change in changes:
            actions = change.get('change', {}).get('actions', [])
            for action in actions:
                if action in change_counts:
                    change_counts[action] += 1
        
        # Add summary labels with emojis
        summary.add(f"🟢 Create: {change_counts['create']}")
        summary.add(f"🟡 Update: {change_counts['update']}")
        summary.add(f"🔴 Delete: {change_counts['delete']}")
        summary.add(f"🔵 Replace: {change_counts['replace']}")
        
        # Resources by module
        modules: Dict[str, Any] = {}
        for change in changes:
            address = change['address']
            module = "root"
            if address.startswith("module."):
                module_parts = address.split(".")
                module = ".".join(module_parts[:2])
            
            if module not in modules:
                modules[module] = []
            modules[module].append(change)
        
        # Add module nodes
        resources_node = self.root.add("📦 Resource Changes", expand=True)
        for module_name, changes in modules.items():
            module_node = resources_node.add(f"📁 {module_name}", expand=False)
            for change in changes:
                actions = change['change']['actions']
                emoji = "⚪"
                if 'create' in actions:
                    emoji = "🟢"
                elif 'delete' in actions:
                    emoji = "🔴"
                elif 'replace' in actions:
                    emoji = "🔵"
                elif 'update' in actions:
                    emoji = "🟡"
                
                module_node.add(f"{emoji} {change['address']}")


class TerraformStateTree(Tree):
    """Custom tree widget for displaying Terraform state"""
    
    def __init__(self) -> None:
        super().__init__("🌳 State")
        self.show_root = False
        
    def load_state_data(self, state_data: Dict) -> None:
        """Load and display terraform state JSON data"""
        self.clear()
        
        if 'resources' not in state_data:
            self.root.add("❌ No state data available")
            return
            
        resources = state_data['resources']
        
        # Group by type
        resource_types = {}
        for resource in resources:
            resource_type = resource['type']
            if resource_type not in resource_types:
                resource_types[resource_type] = []
            resource_types[resource_type].append(resource)
        
        # Build tree
        for resource_type, items in resource_types.items():
            type_node = self.root.add(f"📦 {resource_type} ({len(items)})", expand=False)
            for resource in items:
                name = resource.get('name', 'unknown')
                mode = resource.get('mode', 'managed')
                mode_icon = "🔧" if mode == "managed" else "📊"
                type_node.add(f"{mode_icon} {name}")


class StatusHeader(Static):
    """Custom header showing Terraform context"""
    
    config = reactive(TerraformConfig)
    
    def __init__(self, config: TerraformConfig) -> None:
        super().__init__()
        self.config = config
        
    def render(self) -> str:
        provider_info = f"{self.config.provider}: {self.config.subscription_id}" if self.config.provider else "Not detected"
        var_info = f"tfvars: {self.config.var_file}" if self.config.var_file else "No var file"
        state_info = f"State: {self.config.state_backend}"
        init_status = "✓" if self.config.initialized else "✗"
        
        return (
            f"┌─ tf-textual ─[{provider_info}]─[{var_info}]─[{state_info}]─[Init:{init_status}]─┐\n"
            f"│ [Init] [Plan] [Apply] [Refresh] [Config] [Auth]                               │\n"
            f"├──────────────── Current workdir: {self.config.workdir.name} ──────────────────┤"
        )


class TerraformOutput(Log):
    """Widget for displaying Terraform command output"""
    
    def __init__(self) -> None:
        super().__init__(classes="output-panel")
        self.border_title = "TERRAFORM OUTPUT"


class ControlButtons(Horizontal):
    """Main control buttons"""
    
    def compose(self) -> ComposeResult:
        yield Button("🚀 Init", id="init-btn", variant="primary")
        yield Button("📋 Plan", id="plan-btn", variant="success") 
        yield Button("✅ Apply", id="apply-btn", variant="warning")
        yield Button("🔄 Refresh State", id="refresh-btn")
        yield Button("⚙️ Config", id="config-btn")
        yield Button("🔐 Auth", id="auth-btn")


class TFTextualApp(App):
    """Main Terraform Textual Application"""
    
    CSS = """
    Screen {
        layout: vertical;
    }
    
    .header {
        height: 3;
        border: solid $accent;
        padding: 0 1;
    }
    
    .main-container {
        height: 1fr;
        layout: horizontal;
    }
    
    .left-panel {
        width: 60%;
        border: solid $accent;
        margin: 0 1 0 0;
    }
    
    .right-panel {
        width: 40%;
        border: solid $accent;
    }
    
    .output-panel {
        height: 12;
        border: solid $accent;
        margin: 1 0 0 0;
    }
    
    Button {
        margin: 0 1 0 0;
    }
    
    Tree:focus {
        border: double $accent;
    }
    
    .success {
        color: $success;
    }
    
    .warning {
        color: $warning;
    }
    
    .error {
        color: $error;
    }
    """
    
    BINDINGS = [
        Binding("ctrl+i", "init", "Init"),
        Binding("ctrl+p", "plan", "Plan"), 
        Binding("ctrl+a", "apply", "Apply"),
        Binding("ctrl+r", "refresh", "Refresh"),
        Binding("f1", "toggle_dark", "Toggle dark mode"),
    ]
    
    def __init__(self, workdir: Optional[Path] = None) -> None:
        super().__init__()
        self.workdir = workdir or Path.cwd()
        self.config = self.detect_environment()
        self.plan_tree = TerraformPlanTree()
        self.state_tree = TerraformStateTree()
        self.output = TerraformOutput()
        
    def detect_environment(self) -> TerraformConfig:
        """Auto-detect Terraform environment configuration"""
        config = TerraformConfig(workdir=self.workdir)
        
        # Detect .tfvars files
        tfvars_files = list(self.workdir.glob("*.tfvars"))
        if tfvars_files:
            config.var_file = tfvars_files[0].name
            
        # Detect provider
        for tf_file in self.workdir.glob("*.tf"):
            content = tf_file.read_text()
            if 'azurerm' in content:
                config.provider = "azure"
            elif 'google' in content:
                config.provider = "gcp"
            elif 'aws' in content:
                config.provider = "aws"
                
        # Check if initialized
        config.initialized = (self.workdir / ".terraform").exists()
        
        return config
        
    def compose(self) -> ComposeResult:
        yield StatusHeader(self.config)
        yield ControlButtons()
        
        with Horizontal(classes="main-container"):
            with Vertical(classes="left-panel"):
                yield Label("📋 Terraform Plan", classes="panel-title")
                yield self.plan_tree
                
            with Vertical(classes="right-panel"):
                yield Label("🌳 Current State", classes="panel-title")
                yield self.state_tree
                
        yield self.output
        yield Footer()
        
    async def on_mount(self) -> None:
        """Called when app starts"""
        self.output.write("🚀 tf-textual started - Ready for Terraform operations!")
        await self.load_current_state()
        
    async def load_current_state(self) -> None:
        """Load current Terraform state"""
        try:
            # Try to load state file
            state_file = self.workdir / "terraform.tfstate"
            if state_file.exists():
                state_data = json.loads(state_file.read_text())
                self.state_tree.load_state_data(state_data)
                self.output.write("✅ Loaded current state")
            else:
                self.output.write("⚠️ No state file found")
                
        except Exception as e:
            self.output.write(f"❌ Error loading state: {e}")
            
    @on(Button.Pressed, "#init-btn")
    async def on_init(self) -> None:
        """Handle init button press"""
        self.output.write("🚀 Initializing Terraform...")
        await self.run_terraform_command(["init"])
        self.config.initialized = True
        self.query_one(StatusHeader).refresh()
        
    @on(Button.Pressed, "#plan-btn") 
    async def on_plan(self) -> None:
        """Handle plan button press"""
        if not self.config.initialized:
            self.output.write("❌ Please run init first!")
            return
            
        self.output.write("📋 Running terraform plan...")
        plan_args = ["plan", "-out=tfplan.out"]
        if self.config.var_file:
            plan_args.extend(["-var-file", self.config.var_file])
            
        await self.run_terraform_command(plan_args)
        await self.load_plan_output()
        
    @on(Button.Pressed, "#apply-btn")
    async def on_apply(self) -> None:
        """Handle apply button press"""
        plan_file = self.workdir / "tfplan.out"
        if not plan_file.exists():
            self.output.write("❌ No plan file found. Run plan first!")
            return
            
        self.output.write("✅ Applying Terraform plan...")
        await self.run_terraform_command(["apply", "tfplan.out"])
        await self.load_current_state()
        
    @on(Button.Pressed, "#refresh-btn")
    async def on_refresh(self) -> None:
        """Handle refresh button press"""
        self.output.write("🔄 Refreshing...")
        await self.load_current_state()
        self.config = self.detect_environment()
        self.query_one(StatusHeader).refresh()
        
    async def run_terraform_command(self, args: List[str]) -> None:
        """Run terraform command and capture output"""
        try:
            process = await asyncio.create_subprocess_exec(
                "terraform", *args,
                cwd=self.workdir,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT
            )
            
            while True:
                output = await process.stdout.readline()
                if not output:
                    break
                line = output.decode().strip()
                self.output.write(line)
                
            await process.wait()
            
        except Exception as e:
            self.output.write(f"❌ Error running command: {e}")
            
    async def load_plan_output(self) -> None:
        """Load and parse plan output"""
        try:
            # Convert plan to JSON
            process = await asyncio.create_subprocess_exec(
                "terraform", "show", "-json", "tfplan.out",
                cwd=self.workdir,
                stdout=asyncio.subprocess.PIPE
            )
            
            output, _ = await process.communicate()
            plan_data = json.loads(output.decode())
            
            # Update plan tree
            self.plan_tree.load_plan_data(plan_data)
            self.output.write("✅ Plan loaded successfully")
            
        except Exception as e:
            self.output.write(f"❌ Error loading plan: {e}")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="tf-textual - Terraform Terminal Companion")
    parser.add_argument("--dir", type=str, help="Terraform working directory", default=".")
    
    args = parser.parse_args()
    workdir = Path(args.dir).resolve()
    
    if not workdir.exists():
        print(f"Error: Directory {workdir} does not exist")
        return
        
    app = TFTextualApp(workdir)
    app.run()


if __name__ == "__main__":
    main()