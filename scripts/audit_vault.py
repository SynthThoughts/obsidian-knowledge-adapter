#!/usr/bin/env python3
import os
import re
import argparse
from pathlib import Path
from collections import defaultdict
from datetime import datetime

class VaultAuditor:
    def __init__(self, vault_path):
        self.vault_path = Path(vault_path).resolve()
        self.all_files = set()
        self.all_links = defaultdict(list)  # target -> [sources]
        self.broken_links = defaultdict(list) # source -> [missing_targets]
        self.orphans = []
        self.empty_files = []
        
    def scan_vault(self):
        """Walk strictly through the vault to inventory files."""
        print(f"Scanning vault: {self.vault_path}")
        for root, dirs, files in os.walk(self.vault_path):
            # Skip hidden directories (like .git, .obsidian, .trash)
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                if file.startswith('.'): continue
                
                file_path = Path(root) / file
                rel_path = file_path.relative_to(self.vault_path)
                
                self.all_files.add(str(rel_path))
                
                if file.endswith('.md'):
                    self._analyze_markdown(file_path, str(rel_path))
                    if file_path.stat().st_size == 0:
                        self.empty_files.append(str(rel_path))

    def _analyze_markdown(self, file_path, rel_path):
        """Parse markdown for wikilinks and check validity."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Regex for [[link]] or [[link|alias]]
            # We capture the content inside [[...]]
            links = re.findall(r'\[\[([^\]]+)\]\]', content)
            
            for link in links:
                # Extract actual link target (remove alias)
                target = link.split('|')[0].strip()
                # Remove anchor links (e.g. [[Note#Heading]])
                target_file_base = target.split('#')[0].strip()
                
                if not target_file_base:
                    continue
                    
                self.all_links[target_file_base].append(rel_path)
                
        except Exception as e:
            print(f"Error reading {rel_path}: {e}")

    def verify_links(self):
        """Check if captured links exist in the file inventory."""
        # Create a set of "normalized" file paths/names for easier matching
        # Obsidian allows linking by filename alone if unique
        file_inventory_names = {os.path.basename(f): f for f in self.all_files}
        file_inventory_paths = set(self.all_files)
        
        for target, sources in self.all_links.items():
            # 1. Exact path match
            if target in file_inventory_paths:
                continue
            
            # 2. Filename match (with or without extension)
            target_name = os.path.basename(target)
            
            # Try matching with .md extension if not present
            if not os.path.splitext(target_name)[1]:
                 candidate_md = target_name + ".md"
                 if candidate_md in file_inventory_names:
                     continue
            
            # Try exact name match against inventory files
            if target_name in file_inventory_names:
                continue
               
            # If we get here, the link is likely broken
            for source in sources:
                self.broken_links[source].append(target)

    def identify_orphans(self):
        """Find markdown files with no incoming links (excluding index files)."""
        # Build set of all targets that have at least one valid link
        linked_targets = set()
        
        # We need to map the "targets" back to actual files
        file_inventory_names = {os.path.basename(f): f for f in self.all_files}
        
        for target in self.all_links.keys():
             # Resolve target to actual file
             if target in self.all_files:
                 linked_targets.add(target)
             else:
                 # Try to resolve by filename
                 target_name = os.path.basename(target)
                 if not os.path.splitext(target_name)[1]:
                     target_name += ".md"
                 
                 if target_name in file_inventory_names:
                     linked_targets.add(file_inventory_names[target_name])
        
        for f in self.all_files:
            if not f.endswith('.md'): continue
            
            # Skip obvious index files
            if f in ['index.md', 'README.md', 'Home.md', '首页.md']: continue
            
            # If not in linked_targets, it's an orphan
            if f not in linked_targets:
                self.orphans.append(f)

    def generate_report(self, output_file):
        """Write the audit results to a markdown file."""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# Vault Audit Report\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Vault: `{self.vault_path}`\n\n")
            
            f.write(f"## Summary\n")
            f.write(f"- Total Files: {len(self.all_files)}\n")
            f.write(f"- Broken Links (Source Files): {len(self.broken_links)}\n")
            f.write(f"- Orphan Files: {len(self.orphans)}\n")
            f.write(f"- Empty Files: {len(self.empty_files)}\n\n")
            
            f.write(f"## Broken Links\n")
            if not self.broken_links:
                f.write("_No broken links found._\n")
            else:
                for source, targets in sorted(self.broken_links.items()):
                    f.write(f"### [[{source}]]\n")
                    for t in set(targets):
                        f.write(f"- ❌ [[{t}]]\n")
                    f.write("\n")
            
            f.write(f"## Orphan Files\n")
            if not self.orphans:
                f.write("_No orphans found._\n")
            else:
                for orphan in sorted(self.orphans):
                    f.write(f"- [[{orphan}]]\n")
            
            f.write(f"\n## Empty Files\n")
            if not self.empty_files:
                f.write("_No empty files found._\n")
            else:
                for ef in sorted(self.empty_files):
                    f.write(f"- `{ef}`\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit Obsidian Vault for issues.")
    parser.add_argument("--vault", required=True, help="Path to the Obsidian vault root")
    parser.add_argument("--output", default="vault_audit_report.md", help="Output report file path")
    
    args = parser.parse_args()
    
    auditor = VaultAuditor(args.vault)
    auditor.scan_vault()
    auditor.verify_links()
    auditor.identify_orphans()
    auditor.generate_report(args.output)
    
    print(f"Audit complete. Report written to {args.output}")
