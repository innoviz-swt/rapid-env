import sys
from pathlib import Path

def mainwin32():
    if len(sys.argv) < 2:
        print(f'to use run: python set_activate_alias.py $profile')
        return

    profile = sys.argv[1]
    profile = Path(profile)
    
    # makr parent directory if not exist
    if not profile.parent.exists():
        profile.parent.mkdir(parents=True)
    
    # make file if not exist
    if not profile.exists():
        with open(profile, "a") as f:
            f.write("")

    with open(profile, 'r') as f:
        txt = f.read()

    insert = r"Set-Alias -Name activate -Value .\venv\Scripts\activate"
    if txt.find(insert) != -1:
        print(f'alias already set in "{profile}".')
        return
    
    # write to file
    with open(profile, "a") as f:
        f.write(insert + "\n")

def main():
    if sys.platform == "win32":
        mainwin32()
    else:
        print("plafrom not supported")


if __name__ == "__main__":
    main()