# Citation Format Reference

## Standard Format

```
Author (Year) [ref:ZOTEROKEY]
```

The Zotero key is an 8-character identifier consisting of uppercase letters and numbers.

## Examples by Context

### In-Text Citations

**Narrative (author as subject)**:
```markdown
Harvey (2016) [ref:TVE8UM2C] showed that most reported factors fail to replicate.
```

**Parenthetical (supporting statement)**:
```markdown
Most reported factors fail to replicate under scrutiny (Harvey, 2016) [ref:TVE8UM2C].
```

### Multiple Authors

**Two authors**:
```markdown
Fama and French (1993) [ref:XYZ12345] introduced the three-factor model.
```

**Three or more authors**:
```markdown
Gu et al. (2020) [ref:ABCD1234] demonstrated deep learning's superiority.
```

### Multiple Citations

**Same statement**:
```markdown
Factor momentum has been extensively studied (Arnott et al., 2019) [ref:KEY1]
(Ehsani & Linnainmaa, 2022) [ref:KEY2].
```

**Comparing sources**:
```markdown
While Harvey (2016) [ref:KEY1] emphasizes statistical issues,
McLean and Pontiff (2016) [ref:KEY2] focus on post-publication decay.
```

## Finding Zotero Keys

1. **Search command**: `/ref-search "topic"`
2. **Database query**: Check `ml4t_refs.db`
3. **Papers index**: Look in `papers_index.json`
4. **Zotero app**: Visible in item details

## Validation

Grep for all citations in a chapter:
```bash
grep -oE '\[ref:[A-Z0-9]{8}\]' chapter/draft.md | sort -u
```

Verify all cited keys exist:
```bash
for key in $(grep -oE '\[ref:[A-Z0-9]{8}\]' draft.md | sed 's/\[ref://;s/\]//'); do
    [ -d "$REFS_DIR/papers/$key" ] || echo "Missing: $key"
done
```

## Anti-Patterns

**Don't use**:
- Footnote numbers: `[1]` - not stable
- URL only: `https://arxiv.org/...` - not grepable
- Informal: `(see Harvey's paper)` - not traceable

**Do use**:
- Full citation: `Harvey (2016) [ref:TVE8UM2C]`
- Key enables automation and validation
