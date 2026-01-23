# Synth — AI Development Guide

This document provides context for AI assistants (like Claude) working on this codebase.

## Repository Overview

**Synth** is a creative coding project focused on audio synthesis, generative art, and real-time visualization synchronized to rhythm and MIDI input.

**Current modules:**
- **visuals/** — Generative art and visualization engine with rhythm and MIDI sync

**Experimental scripts:**
- **sine.py** — Simple sine wave audio generation example
- **AudioFun.ipynb** — Jupyter notebook for audio experimentation

## Project Structure

```
synth/
├── CLAUDE.md           # This file: AI development context (top-level)
├── README.md           # User-facing documentation (top-level)
├── Makefile            # Test runner (make unittest)
├── sine.py             # Sine wave generation example
├── AudioFun.ipynb      # Audio experimentation notebook
├── visuals/            # Main visualization module
│   ├── CLAUDE.md       # Module-specific AI context
│   ├── README.md       # Module documentation
│   ├── engine.py       # Pygame render loop
│   ├── rhythm.py       # Beat clock (BPM, phase, pulse)
│   ├── midi_input.py   # MIDI input handling
│   ├── requirements.txt
│   └── sketches/       # Visual sketches
│       ├── rings.py    # Beat-synced expanding rings
│       ├── blink.py    # Colored grid reacting to MIDI
│       ├── constellation.py  # Radial blinking lights from MIDI
│       └── run_*.py    # CLI entry points
└── tests/
    └── test_visuals/   # Unit tests for visuals module
```

## Development Workflow

### When Starting Any Task

**ALWAYS do this first:**
1. Check for `CLAUDE.md` files in:
   - Repository root (`/home/user/synth/CLAUDE.md`)
   - Relevant module directories (e.g., `visuals/CLAUDE.md`)
2. Check for `README.md` files in the same locations
3. Use this documentation as your initial context
4. Explore code when you need deeper understanding or when docs are unclear

### When Making Code Changes

**CRITICAL: Keep documentation synchronized with code changes**

After making any significant code change, update the relevant documentation:

1. **Architecture changes** (new files, modules, classes, major refactoring):
   - Update `CLAUDE.md` in the affected module
   - Update `README.md` with any user-facing changes
   - Update this top-level `CLAUDE.md` if project structure changes

2. **New features or functionality**:
   - Update module `README.md` with usage examples
   - Update `CLAUDE.md` if internal architecture changes

3. **API changes** (function signatures, module interfaces):
   - Update code examples in `README.md`
   - Update `CLAUDE.md` to reflect new patterns

4. **New dependencies or setup steps**:
   - Update `requirements.txt` or installation instructions
   - Document in relevant `README.md`

**Documentation update checklist:**
- [ ] Does this change affect how users interact with the code? → Update README.md
- [ ] Does this change affect project architecture? → Update CLAUDE.md
- [ ] Did I add/remove/rename files? → Update project structure diagrams
- [ ] Did I add new dependencies? → Update requirements.txt and installation docs
- [ ] Are code examples still accurate? → Verify and update examples

### Testing

Run tests before committing:
```bash
make unittest
```

Tests mock pygame and rtmidi — no hardware or display needed.

## Module-Specific Documentation

Each module has its own documentation:
- **visuals/** — See `visuals/CLAUDE.md` for architecture and `visuals/README.md` for usage

When working on a specific module, read that module's documentation first.

## Development Conventions

### Code Style
- Follow PEP 8 for Python code
- Use descriptive variable names
- Keep functions focused and single-purpose
- Add docstrings for complex logic

### Testing
- Write tests for new functionality
- Mock external dependencies (pygame, rtmidi)
- Place tests in `tests/test_{module}/`

### Git Commits
- Write clear, descriptive commit messages
- Focus on the "why" rather than the "what"
- Keep commits atomic and focused

## Current State

**Last updated:** 2026-01-23

**Recent work:**
- Created visuals module with rhythm and MIDI sync
- Implemented three sketches: rings, blink, constellation
- Added comprehensive test coverage
- Documented MIDI setup for Ableton Live integration

**Known limitations:**
- No top-level README yet (to be added)
- Only one module (visuals) currently implemented
- sine.py is a standalone example, not integrated

## Future Directions

Potential areas for expansion:
- Additional synthesis modules (FM, wavetable, etc.)
- Audio analysis and feature extraction
- More complex visual sketches
- Integration between audio synthesis and visualization
- Real-time audio processing pipeline

---

**Remember:** This file is a living document. Update it whenever you make significant changes to the codebase.
