Contributing
------------
We welcome contributions from anyone, even if you are new to open source we will be happy to help you to get started.

### Code contribution
This project follows PH-Tools contributing guideline. See [contributing to PH-Tools projects](https://github.com/PH-Tools/contributing).

---

## A few things specific to this repository

`honeybee_ph` is the **data model** — the Passive House objects that get attached to a
Honeybee model and saved into HBJSON. It sits in the middle of the stack, which has two
consequences worth knowing before you start.

**It must run under IronPython 2.7.** This package is imported inside Grasshopper, so no
f-strings, no `dataclasses`, no `pathlib`, guarded `typing` imports, and comment-style type
hints. See [the one big rule](https://github.com/PH-Tools/contributing#the-one-big-rule-ironpython-27)
and `context/CODING_STANDARDS.md`.

**Changes here usually ripple.** Validation and allowed values live in this repo, but the
user sees them in `honeybee_grasshopper_ph` and they only reach a PHPP or WUFI file through
`PHX`. Before you start, check
[Changes that span repositories](https://github.com/PH-Tools/contributing#changes-that-span-repositories).

### Selector inputs and the `EnumProperty` tables

A large share of the PHI certification settings are drop-down selectors, and they are
validated by the `allowed_inputs` tables in `honeybee_ph/phi.py`. These tables have a
non-obvious design that is easy to get wrong, so:

**The list index encodes the PHPP number.** `CustomEnum` resolves an integer input to
`allowed[n - 1]`. That means the *position* of an entry in the list is meaningful, not just
its text. Where PHPP skips a number, the list carries a `"_"` placeholder to keep everything
lined up:

```python
"ihg_type": {
    10: [
        "1-USER-DEFINED",                            # index 0  -> input "1"
        "2-STANDARD",                                # index 1  -> input "2"
        "3-PHPP-CALCULATION ('IHG' WORKSHEET)",      # index 2  -> input "3"
        "4-PHPP-CALCULATION ('IHG NON-RES' WORKSHEET)",
    ],
},
```

So:

- **Never reorder or delete entries** — you will silently remap every existing model.
- **To add a value, replace the `"_"` placeholder at its position**; do not append it.
- **Entries are UPPERCASE.** Lookups are case-insensitive, so mixed case works by accident,
  but please match the surrounding style.
- A `"_"` that survives into a set value raises — that is the deliberate "this number is not
  valid for this PHPP version" signal.

**Check the real PHPP before changing an allowed-values list.** These lists mirror the
drop-downs on the `Verification` worksheet, and some of those drop-downs are *dynamic* —
the options change depending on another selection. Getting the list right matters more than
getting it long. If you do not have the workbook handy, say so in the issue and we will
confirm the values for you.

### Tests

Run `python3 -m pytest` before opening a PR. Two things this repo has been bitten by, so
please cover them for anything you touch:

- **Both PHPP versions.** `PHPPSettings9` and `PHPPSettings10` are separate classes with
  separate tables. A test that only builds the default version leaves the other one
  untested while coverage still looks fine.
- **The rejection path.** If a value should be refused, assert that it raises. Also assert
  the `.number` round-trip (`.number` is what `PHX` reads to decide what to write into the
  PHPP cell), not just `.value`.
