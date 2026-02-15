#!/usr/bin/env python3
import os
import sys
import json
import glob

def get_frontmatter(file_path):
    fm = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if not lines or not lines[0].strip() == '---':
                return {}
            # Start parsing from line 1
            for line in lines[1:]:
                line = line.strip()
                if line == '---':
                    break
                if ':' in line:
                    key, val = line.split(':', 1)
                    key = key.strip()
                    val = val.strip().strip('"').strip("'")
                    fm[key] = val
    except Exception as e:
        sys.stderr.write(f"Error reading {file_path}: {e}\n")
    return fm

def scan_dir(directory):
    agents = []
    if not os.path.exists(directory):
        return agents
        
    for file_path in glob.glob(os.path.join(directory, "*.md")):
        fm = get_frontmatter(file_path)
        agent_name = fm.get('name', os.path.basename(file_path).replace('.md', ''))
        agent_desc = fm.get('description', '')
        
        # If built-in agent, prepend (Built-in) to name for clarity
        if "obsidian-knowledge-adapter/agents" in file_path:
             agent_name = f"{agent_name} (Built-in)"

        agent_info = {
            "name": agent_name,
            "description": agent_desc,
            "path": file_path
        }
        agents.append(agent_info)
    return agents

def list_agents(vault_root):
    all_agents = []

    # 1. Scan Vault Agents (.claude/agents)
    # 1. Scan Vault Agents (.antigravity/agents or .claude/agents)
    # Check Antigravity first
    antigravity_agents_dir = os.path.join(vault_root, '.antigravity', 'agents')
    if os.path.exists(antigravity_agents_dir):
        all_agents.extend(scan_dir(antigravity_agents_dir))
    
    # Check Legacy Claudian path
    legacy_agents_dir = os.path.join(vault_root, '.claude', 'agents')
    if os.path.exists(legacy_agents_dir):
        all_agents.extend(scan_dir(legacy_agents_dir))

    # 2. Scan Built-in Agents (relative to script location)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    builtin_agents_dir = os.path.join(script_dir, '../agents')
    all_agents.extend(scan_dir(builtin_agents_dir))

    if not all_agents:
        print(json.dumps({"agents": [], "message": f"No agents found in {antigravity_agents_dir} or {legacy_agents_dir} or built-in directory."}))
        return

    print(json.dumps({"agents": all_agents}, indent=2))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        vault_root = sys.argv[1]
    else:
        vault_root = os.getcwd()
    
    list_agents(vault_root)
