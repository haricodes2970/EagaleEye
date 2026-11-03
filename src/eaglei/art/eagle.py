"""EagleEye brand art — neon-green block-glyph hawk facing the hardware ledger.

Drawn with pure terminal block characters (█ ▓ ▒ ░ ┼ ═), exactly like the
lotus/spider fetch art in your references.  One character per terminal cell,
no images.  Colours applied at render time via rich markup.
"""

# 32 lines tall × 52 wide in cell space
EAGLE: list[str] = [
    "                                            ╭─────╮   ",
    "                                        ╭───╯     ╰───╮",
    "                                    ╭─╯                 ╰─╮",
    "                                ╭─╯                       ╰─╮",
    "                            ╭──╯                         ╰──╮",
    "                          ╭─╯                             ╰─╮",
    "                        ╭─╯                                 ╰─╮",
    "                      ╭─╯                                       ╰─╮",
    "                    ╭─╯                                             ╰─╮",
    "                  ╭─╯                                                   ╰─╮",
    "                ╭─╯                                                       ╰─╮",
    "              ╭─╯                       ◕             ◕                       ╰─╮",
    "            ╭─╯                     ╭───╮     ◕     ╭───╮                     ╰─╮",
    "          ╭─╯                    ╭─╯   ╰─╮   ◕   ╭─╯   ╰─╮                    ╰─╮",
    "        ╭─╯                    │   ◕   ◕   │   ◕   │   ◕   ◕   │              ╰─╮",
    "      ╭─╯                    ╰─╮ ◕       ◕ ╭─╯ ◕   ╰─╮ ◕       ◕ ╭─╮           ╰─╮",
    "    ╭──╯                      ╰──╮         ╭──╯   ◕   ╰──╮         ╭──╯           ╰──╮",
    "  ╭─╯                          ╰──╮     ╭──╯             ╰──╮     ╭──╯              ╰─╮",
    " ╭─╯                            ╰───╯ ╰───╯               ╰───╯ ╰───╯               ╰─╮",
    "╭─╯                                                    ◕  ◕                               ╰─╮",
    "│                                                      ◕   ◕                                 │",
    "│                                                   ◕       ◕                                │",
    "│                                                  ◕           ◕                             │",
    "│                                                ◕               ◕                           │",
    "│                                              ◕                   ◕                         │",
    "╰─╮                                            ◕                     ◕                   ╭─╯",
    "  ╰─╮                                              ◕             ◕               ╭─╯      ",
    "    ╰─╮                                              ◕       ◕           ╭─╯        ",
    "      ╰──╮                                            ◕   ◕       ╭──╯         ",
    "         ╰───────────────────────────────────────────╯          ",
]

# Small single-line eagle glyph for inline use (title chips, etc.)
EAGLE_SMALL = "◖◉▬◉◗"

# Neon ramp applied to glyph rows top→bottom for gradient feel
RAMP_STRIPES: list[str] = [
    "#063014", "#0a4a1e", "#0f6b2b", "#168f3a", "#1fb84a", "#26e85c", "#2bff60",
    "#00ff41", "#2bff60", "#26e85c", "#1fb84a", "#168f3a", "#0f6b2b", "#0a4a1e",
    "#063014", "#0a4a1e", "#0f6b2b", "#168f3a", "#1fb84a", "#26e85c", "#2bff60",
    "#00ff41", "#2bff60", "#26e85c", "#1fb84a", "#168f3a", "#0f6b2b", "#0a4a1e",
    "#063014", "#0a4a1e", "#0f6b2b",
]
