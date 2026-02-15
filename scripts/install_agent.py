#!/usr/bin/env python3
import os
import sys
import shutil
import argparse
import glob

def get_builtin_agents_dir():
    # Helper to find the agents directory relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Assuming standard structure: skills/obsidian-knowledge-adapter/scripts/install_agent.py
    # Agents should be at: skills/obsidian-knowledge-adapter/agents/
    return os.path.abspath(os.path.join(script_dir, '../agents'))

def list_builtin_agents():
    agents_dir = get_builtin_agents_dir()
    if not os.path.exists(agents_dir):
        print(f"Error: Built-in agents directory not found at {agents_dir}")
        return []
    
    agents = []
    print(f"Available built-in agents in {agents_dir}:")
    for file_path in glob.glob(os.path.join(agents_dir, "*.md")):
        agent_name = os.path.basename(file_path).replace('.md', '')
        print(f"- {agent_name}")
        agents.append(agent_name)
    return agents

def install_agent(agent_name, target_vault_root=None):
    if not target_vault_root:
        target_vault_root = os.getcwd()
    
    agents_dir = get_builtin_agents_dir()
    source_path = os.path.join(agents_dir, f"{agent_name}.md")
    
    if not os.path.exists(source_path):
        print(f"Error: Agent '{agent_name}' not found.")
        list_builtin_agents()
        return False

    # Define target directory
    target_dir = os.path.join(target_vault_root, ".antigravity", "agents")
    os.makedirs(target_dir, exist_ok=True)
    
    target_path = os.path.join(target_dir, f"{agent_name}.md")
    
    try:
        shutil.copy2(source_path, target_path)
        print(f"Successfully installed '{agent_name}' to {target_path}")
        return True
    except Exception as e:
        print(f"Error installing agent: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Install built-in Antigravity agents to your Obsidian Vault.")
    parser.add_argument("agent_name", nargs="?", help="Name of the agent to install (without .md extension)")
    parser.add_argument("--list", action="store_true", help="List available built-in agents")
    parser.add_argument("--vault", help="Path to the Vault root (default: current directory)")

    args = parser.parse_args()

    if args.list or not args.agent_name:
        list_builtin_agents()
    else:
        install_agent(args.agent_name, args.vault)
