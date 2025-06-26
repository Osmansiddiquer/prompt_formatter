"""
The main script for customizing the command prompt in Windows.
"""
import os
import sys
import subprocess
import argparse


def is_powershell():
    """
    Checks if the current shell is PowerShell.
    """
    # PowerShell sessions always have PSModulePath defined
    return "PSModulePath" in os.environ


def set_cmd_prompt(fmt: str):
    """
    Sets the command prompt in cmd.exe.
    If fmt is empty, it resets to the default prompt ($P$G).
    the fmt format is according to cmd.exe's prompt syntax.
    """
    # In cmd.exe, the built-in `prompt` command sets the prompt for the session.
    # If fmt is empty, it resets to default ($P$G).
    cmd = ["cmd", "/c", "prompt"]
    if fmt:
        cmd.append(fmt)
    proc = subprocess.run(cmd, check=False)
    if proc.returncode != 0:
        raise RuntimeError(
            f"Failed to set cmd prompt with format '{fmt}'. "
            "Ensure the format is valid according to cmd.exe's syntax."
        )


def set_powershell_prompt(fmt: str):
    """
    Sets the PowerShell prompt.
    If fmt is empty, it resets to the default prompt.
    fmt is according to PowerShell's prompt function syntax.
    """
    # In PowerShell, you override the prompt() function.
    # To set a new format:
    if fmt:
        # We emit a function definition that returns the literal fmt
        ps_cmd = f"function global:prompt {{ '{fmt}' }};"
    else:
        # Removing the override causes PS to revert to its built-in prompt
        ps_cmd = "Remove-Item function:\\prompt -ErrorAction SilentlyContinue;"
    proc = subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], check=False)
    if proc.returncode != 0:
        raise RuntimeError(
            f"Failed to set PowerShell prompt with format '{fmt}'."
            "Ensure the format is valid according to PowerShell's syntax."
        )

def main():
    """
    Main function to handle command line arguments and set the prompt.
    """
    parser = argparse.ArgumentParser(
        prog="prompt", description="Customize your Windows shell prompt."
    )
    parser.add_argument(
        "format",
        nargs="?",
        help="Prompt format string (use shell’s placeholder syntax).",
    )
    parser.add_argument(
        "-r", "--reset", action="store_true", help="Reset prompt to default."
    )
    args = parser.parse_args()

    if args.reset:
        fmt = ""
    elif args.format:
        fmt = args.format
    else:
        parser.print_help()
        sys.exit(1)

    if is_powershell():
        set_powershell_prompt(fmt)
    else:
        set_cmd_prompt(fmt)


if __name__ == "__main__":
    main()
