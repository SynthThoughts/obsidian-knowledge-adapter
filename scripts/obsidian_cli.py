#!/usr/bin/env python3
import subprocess
import argparse
import sys
import shutil
import os

OBSIDIAN_BIN = "obsidian"
# User Configuration
DEFAULT_VAULT_PATH = "."

def check_cli():
    # Use global to modify the variable
    global OBSIDIAN_BIN
    
    # Check if currently set binary is valid
    if shutil.which(OBSIDIAN_BIN):
        return True
    
    # Check common locations
    locations = [
        "/Applications/Obsidian.app/Contents/MacOS/Obsidian",
        "/Applications/Obsidian.app/Contents/MacOS/obsidian",
    ]
    
    # Try to find via mdfind (macOS) or find
    try:
         locations.append(str(subprocess.run("mdfind kMDItemCFBundleIdentifier = 'md.obsidian' | head -n 1", shell=True, capture_output=True, text=True).stdout.strip()) + "/Contents/MacOS/Obsidian")
    except:
        pass

    for loc in locations:
        if loc and shutil.which(loc):
            OBSIDIAN_BIN = loc
            return True
    return False

def run_command(args, timeout=10, vault_path=None):
    if not check_cli():
        print("Error: Obsidian CLI not found.")
        return

    cmd = [OBSIDIAN_BIN] + args
    
    # Determine the working directory for the command
    cwd = vault_path if vault_path else os.getcwd()
    
    try:
        # Execute command in the context of the default vault if possible
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=cwd)
        if result.returncode == 0:
            print(result.stdout)
        else:
            print(f"Error executing command: {result.stderr}")
    except subprocess.TimeoutExpired:
        print("Error: Command timed out.")
    except Exception as e:
        print(f"Exception: {e}")

# Command Handlers

def read_file(file_path):
    run_command(["read", f"file={file_path}"])

def eval_js(code):
    run_command(["dev:eval", f"code={code}"])

def get_backlinks(file_path):
    # Use CLI native command instead of JS eval if possible, but keep JS for custom/raw data
    # Docs say: obsidian backlinks file=...
    run_command(["backlinks", f"file={file_path}"])

def get_links(file_path):
    run_command(["links", f"file={file_path}"])

def get_orphans():
    run_command(["orphans"])

def get_unresolved():
    run_command(["unresolved"])

def handle_daily(mode, content=None):
    if mode == "read":
        run_command(["daily:read"])
    elif mode == "append":
        if not content:
            print("Error: Content required for append.")
            return
        run_command(["daily:append", f"content={content}"])
    elif mode == "open":
        run_command(["daily"])
    else:
        print("Invalid daily mode. Use read, append, or open.")

def create_note(name, content=""):
    args = ["create", f"name={name}"]
    if content:
        args.append(f"content={content}")
    run_command(args)

def search_vault(query):
    run_command(["search", f"query={query}"])

def list_tags():
    run_command(["tags"])
    
def open_note(file_path):
    run_command(["open", f"file={file_path}"])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Obsidian CLI Wrapper")
    subparsers = parser.add_subparsers(dest="command")

    # READ
    read_parser = subparsers.add_parser("read")
    read_parser.add_argument("file", help="File path relative to vault root")

    # EVAL
    eval_parser = subparsers.add_parser("eval")
    eval_parser.add_argument("code", help="JS code to execute")

    # BACKLINKS
    backlinks_parser = subparsers.add_parser("backlinks")
    backlinks_parser.add_argument("file", help="File path relative to vault root")

    # LINKS (Outgoing)
    links_parser = subparsers.add_parser("links")
    links_parser.add_argument("file", help="File path relative to vault root")

    # ORPHANS
    orphans_parser = subparsers.add_parser("orphans")

    # UNRESOLVED
    unresolved_parser = subparsers.add_parser("unresolved")

    # DAILY
    daily_parser = subparsers.add_parser("daily")
    daily_parser.add_argument("mode", choices=["read", "append", "open"], help="Action regarding daily note")
    daily_parser.add_argument("--content", help="Content to append (only for append mode)")

    # CREATE
    create_parser = subparsers.add_parser("create")
    create_parser.add_argument("name", help="Name of the note")
    create_parser.add_argument("--content", default="", help="Initial content")

    # SEARCH
    search_parser = subparsers.add_parser("search")
    search_parser.add_argument("query", help="Query string")

    # TAGS
    tags_parser = subparsers.add_parser("tags")

    # OPEN
    open_parser = subparsers.add_parser("open")
    open_parser.add_argument("file", help="File path to open")

    args = parser.parse_args()

    if args.command == "read":
        read_file(args.file)
    elif args.command == "eval":
        eval_js(args.code)
    elif args.command == "backlinks":
        get_backlinks(args.file)
    elif args.command == "links":
        get_links(args.file)
    elif args.command == "orphans":
        get_orphans()
    elif args.command == "unresolved":
        get_unresolved()
    elif args.command == "daily":
        handle_daily(args.mode, args.content)
    elif args.command == "create":
        create_note(args.name, args.content)
    elif args.command == "search":
        search_vault(args.query)
    elif args.command == "tags":
        list_tags()
    elif args.command == "open":
        open_note(args.file)
    else:
        parser.print_help()
