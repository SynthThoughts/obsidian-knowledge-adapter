#!/usr/bin/env python3
import argparse
import os
import sys

def secure_path(vault_root, file_path):
    """Ensures the file path is within the vault root."""
    abs_vault = os.path.abspath(vault_root)
    abs_file = os.path.abspath(os.path.join(abs_vault, file_path))
    if not abs_file.startswith(abs_vault):
        raise ValueError(f"Security Error: Path '{file_path}' attempts to access outside vault '{vault_root}'")
    return abs_file

def read_file(vault_root, file_path):
    full_path = secure_path(vault_root, file_path)
    if not os.path.exists(full_path):
        print(f"Error: File not found: {file_path}")
        sys.exit(1)
    with open(full_path, 'r', encoding='utf-8') as f:
        print(f.read())

def write_file(vault_root, file_path, content, mode='w'):
    full_path = secure_path(vault_root, file_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, mode, encoding='utf-8') as f:
        f.write(content)
    print(f"Successfully wrote to {file_path}")

def list_files(vault_root, path="."):
    full_path = secure_path(vault_root, path)
    if not os.path.exists(full_path):
        print(f"Error: Path not found: {path}")
        sys.exit(1)
    
    for root, dirs, files in os.walk(full_path):
        # Calculate relative path for display
        rel_root = os.path.relpath(root, full_path)
        if rel_root == ".":
            rel_root = ""
        
        for d in dirs:
             if not d.startswith('.'):
                print(f"[DIR]  {os.path.join(rel_root, d)}")
        for f in files:
            if not f.startswith('.'):
                print(f"[FILE] {os.path.join(rel_root, f)}")
        # Only list top level if path is specified, unless recursive flag meant (simplified for now)
        if path != ".":
             break 

def search_files(vault_root, query):
    abs_vault = os.path.abspath(vault_root)
    print(f"Searching for '{query}' in {abs_vault}...")
    for root, _, files in os.walk(abs_vault):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if query in content:
                            rel_path = os.path.relpath(file_path, abs_vault)
                            print(f"[MATCH] {rel_path}")
                except Exception as e:
                    pass # Ignore read errors

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Obsidian File System Tool")
    parser.add_argument("--vault", required=True, help="Absolute path to the Obsidian Vault root")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Read
    read_parser = subparsers.add_parser("read")
    read_parser.add_argument("file", help="File path relative to vault root")

    # Write
    write_parser = subparsers.add_parser("write")
    write_parser.add_argument("file", help="File path relative to vault root")
    write_parser.add_argument("--content", required=True, help="Content to write")

    # Append
    append_parser = subparsers.add_parser("append")
    append_parser.add_argument("file", help="File path relative to vault root")
    append_parser.add_argument("--content", required=True, help="Content to append")

    # List
    list_parser = subparsers.add_parser("list")
    list_parser.add_argument("path", nargs="?", default=".", help="Directory to list (relative to vault)")

    # Search
    search_parser = subparsers.add_parser("search")
    search_parser.add_argument("query", help="String to search for")

    args = parser.parse_args()

    try:
        if args.command == "read":
            read_file(args.vault, args.file)
        elif args.command == "write":
            write_file(args.vault, args.file, args.content, mode='w')
        elif args.command == "append":
            write_file(args.vault, args.file, "\n" + args.content, mode='a')
        elif args.command == "list":
            list_files(args.vault, args.path)
        elif args.command == "search":
            search_files(args.vault, args.query)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
