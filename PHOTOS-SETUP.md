# Setting up the photo library

Decks can use Poetics' own photographs by name. They aren't in this repo (it's public, and the
photos show real people), so you get them as a zip, `Poetics Photos.zip`, and Claude Code puts
them in place.

**Before you start:** install the plugin (Path A in [INSTALL.md](INSTALL.md)). This only works
in Claude Code (the Code tab of the Claude desktop app, or the `claude` terminal app). It doesn't
work in claude.ai chat, which can't save files to your computer; there, attach the photos you want
to the conversation instead.

## Steps

1. Open Claude Code and start a new session.
2. Attach `Poetics Photos.zip` to the message.
3. Paste the prompt below and send it.
4. When it's done, quit and reopen Claude (or open a new terminal tab) so the setting takes effect.

When you get a newer zip, do the same again: it replaces the old photos.

## The prompt

```text
I've attached "Poetics Photos.zip", the Poetics photo library for the Poetics brand plugin (brand@poetics). Please set it up on this computer so decks can use these photos:

1. Find the attached zip. If you can't, ask me where it is; don't search my whole disk.
2. Unzip it into a temporary folder, then move the photo folder to ~/Poetics Photos. The right folder is the one that directly contains subfolders such as "about/" and "art-tech-technopolis/". If the zip has an extra wrapper folder (e.g. "images/"), use the folder inside it. If ~/Poetics Photos already exists, replace it with the new photos, but tell me first.
3. Make the setting permanent by adding this line to ~/.zshrc:
   export POETICS_PHOTO_ROOT="$HOME/Poetics Photos"
   If ~/.zshrc already has a POETICS_PHOTO_ROOT line, update it rather than adding a second one.
4. Check that it works. Find the installed plugin's photo index (a file at brand-kit/photos/index.json inside the brand@poetics plugin, usually under ~/.claude/plugins/). For every photo in it, check that "file" exists under ~/Poetics Photos. Tell me how many were found out of the total, and list any that are missing. If the plugin isn't installed, say so and skip this step.
5. Delete the temporary unzip folder. Keep the zip.
6. Finish with one short summary: where the photos are, how many matched, and a reminder that I need to quit and reopen Claude (or open a new terminal) for the setting to take effect.

Don't change anything else on my computer.
```

## If photos come out as empty frames

The path is wrong or the photos are out of date. Run the prompt again with the latest zip. If a
few are still missing, the plugin is newer than your zip: ask for a fresh one.

## Making the zip (for whoever sends it)

From the Poetics Website project, so the subfolders stay at the top level:

```bash
cd ~/Data/Projects/"Poetics Website"/src/assets && ditto -c -k --keepParent --norsrc images ~/Desktop/"Poetics Photos.zip"
```

Send a new zip whenever photos are added to the website and `photo-library.py index` is re-run.
