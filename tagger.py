import os
import tkinter as tk
from tkinter import filedialog, scrolledtext
from mutagen.flac import FLAC
from mutagen.id3 import ID3, TPE2, TALB


def get_album_artist(folder_path):
    return "Compilation: " + os.path.basename(folder_path)


def get_album_name():
    return album_name_var.get().strip()


def browse_folder():
    path = filedialog.askdirectory()
    if path:
        folder_var.set(path)
        # Auto-suggest album name from folder
        folder_name = os.path.basename(path)
        album_name_var.set(folder_name)


def log(msg):
    output.config(state="normal")
    output.insert(tk.END, msg + "\n")
    output.see(tk.END)
    output.config(state="disabled")


def run_tagger():
    folder = folder_var.get().strip()
    album_name = get_album_name()

    if not folder or not os.path.isdir(folder):
        log("ERROR: Select a valid folder first.")
        return

    if not album_name:
        log("ERROR: Album name cannot be empty.")
        return

    album_artist = get_album_artist(folder)

    output.config(state="normal")
    output.delete("1.0", tk.END)
    output.config(state="disabled")

    log("Folder      : " + folder)
    log("Album Artist: " + album_artist)
    log("Album Name  : " + album_name)
    log("")

    tagged = 0
    failed = 0

    for f in sorted(os.listdir(folder)):
        path = os.path.join(folder, f)
        ext = f.lower().split(".")[-1]

        try:
            if ext == "flac":
                audio = FLAC(path)
                audio["albumartist"] = [album_artist]
                audio["album"] = [album_name]
                audio.save()
                log("  [OK] " + f)
                tagged += 1

            elif ext == "mp3":
                audio = ID3(path)
                audio.setall("TPE2", [TPE2(encoding=3, text=album_artist)])
                audio.setall("TALB", [TALB(encoding=3, text=album_name)])
                audio.save()
                log("  [OK] " + f)
                tagged += 1

        except Exception as e:
            log("  [FAIL] " + f + " - " + str(e))
            failed += 1

    log("")
    log("Done. " + str(tagged) + " tagged, " + str(failed) + " failed.")
    log("Rescan MusicBee to apply changes.")


# --- GUI setup ---
root = tk.Tk()
root.title("MusicBee Compilation Tagger")
root.resizable(False, False)
root.configure(bg="#1e1e1e")

FONT = ("Consolas", 10)
FONT_LABEL = ("Consolas", 10, "bold")
BG = "#1e1e1e"
FG = "#d4d4d4"
ACCENT = "#569cd6"
ENTRY_BG = "#2d2d2d"
BTN_BG = "#3a3a3a"
BTN_FG = "#d4d4d4"
BTN_ACTIVE = "#4a4a4a"

pad = {"padx": 10, "pady": 5}

folder_var = tk.StringVar()
album_name_var = tk.StringVar()

# Folder row
tk.Label(root, text="Album Folder", font=FONT_LABEL, bg=BG, fg=ACCENT).grid(
    row=0, column=0, sticky="w", **pad
)
tk.Entry(root, textvariable=folder_var, width=55, font=FONT, bg=ENTRY_BG, fg=FG,
         insertbackground=FG, relief="flat").grid(row=0, column=1, **pad)
tk.Button(root, text="Browse", font=FONT, bg=BTN_BG, fg=BTN_FG,
          activebackground=BTN_ACTIVE, relief="flat", command=browse_folder).grid(
    row=0, column=2, **pad
)

# Album name row
tk.Label(root, text="Album Name", font=FONT_LABEL, bg=BG, fg=ACCENT).grid(
    row=1, column=0, sticky="w", **pad
)
tk.Entry(root, textvariable=album_name_var, width=55, font=FONT, bg=ENTRY_BG, fg=FG,
         insertbackground=FG, relief="flat").grid(row=1, column=1, **pad)

# Info label
tk.Label(root,
         text="Album Artist will be set to: Compilation: <folder name>",
         font=("Consolas", 9), bg=BG, fg="#6a9955").grid(
    row=2, column=0, columnspan=3, sticky="w", padx=10
)

# Run button
tk.Button(root, text="Run Tagger", font=FONT_LABEL, bg=ACCENT, fg="#1e1e1e",
          activebackground="#4fc1ff", relief="flat", cursor="hand2",
          command=run_tagger).grid(row=3, column=0, columnspan=3, pady=10)

# Output box
output = scrolledtext.ScrolledText(root, width=80, height=20, font=FONT,
                                   bg=ENTRY_BG, fg=FG, state="disabled",
                                   relief="flat", wrap="word")
output.grid(row=4, column=0, columnspan=3, padx=10, pady=(0, 10))

root.mainloop()
