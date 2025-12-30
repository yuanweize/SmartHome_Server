# CTU FEE Bachelor Thesis Compliance Checklist

Based on `Bachelor_project_Rules.md` requirements.

## ✅ Fixed Issues

| # | Requirement | Status | Action Taken |
|---|-------------|--------|--------------|
| 1 | **Declaration** with exact CTU wording | ✅ Fixed | Created `chapters/declaration.tex` with Methodological Instruction No. 1/2009 text |
| 2 | **Czech Abstract** (Abstrakt) | ✅ Fixed | Added Czech translation in `chapters/abstract.tex` |
| 3 | **Year 2026** | ✅ Fixed | Updated `thesis-final.tex` and `literature.bib` |
| 4 | **Font size 11pt** | ✅ Fixed | Changed `phdthesis.cls` from 12pt to 11pt |
| 5 | **Two-sided printing** | ✅ Fixed | Changed `phdthesis.cls` to `twoside` |
| 6 | **No Wikipedia references** | ✅ Verified | All references are from proper academic/technical sources |
| 7 | **Contents order** | ✅ Fixed | Reordered: Declaration → Abstract → Contents → Acronyms → Figures/Tables |

## 📋 Structure Compliance

### Required Sections (from Rules)

| Section | File | Status |
|---------|------|--------|
| Topic registration form | (Insert original in bound copy) | ⚠️ User must include |
| Declaration | `chapters/declaration.tex` | ✅ |
| Abstract (EN + CZ) | `chapters/abstract.tex` | ✅ |
| Contents | Auto-generated | ✅ |
| List of Acronyms | `acronyms.tex` | ✅ |
| Introduction | `chapters/introduction.tex` | ✅ |
| Body (Research + Implementation) | `chapters/background.tex` - `chapters/comparison.tex` | ✅ |
| Conclusion | `chapters/conclusion.tex` | ✅ |
| Bibliography | `literature.bib` | ✅ |
| Appendices | `chapters/appendix.tex` | ✅ |

### Page Count Target

- **Requirement:** 20-50 double-sided A4 pages + appendices
- **Estimated:** ~40-50 pages ✅

## ⚠️ User Actions Required

### Before Submission to KOS

1. **Topic Registration Form**
   - Insert the original undamaged form in the bound copy
   - Prepare a working copy during writing

2. **Assignment Fulfillment**
   - Ensure all 4 parts of the assignment are covered
   - If any part cannot be fully covered, explain in the thesis

3. **Remove Signatures for PDF Upload**
   - The PDF uploaded to KOS must have NO SIGNATURES
   - Erase signatures from Topic registration form scan

4. **Thermal Binding**
   - Use thermal binding, NOT spiral binding

### During Defense

- Prepare 10-minute presentation
- Minimum font size 24pt for slides
- Be ready for questions from:
  - Supervisor
  - Opponent
  - Commission

## 📚 Bibliography Reminders

### DO NOT Use
- ❌ Wikipedia
- ❌ Other unreliable resources

### Acceptable Sources (used in this thesis)
- ✅ OASIS Standards (MQTT)
- ✅ IEEE papers
- ✅ ACM publications
- ✅ Official documentation (ESP32, Home Assistant)
- ✅ Technical specifications

### Citation Format
Following ISO 690 (simplified version as per rules).

## 🔧 Compilation Commands

```bash
# In Overleaf
Main File: thesis-final.tex
Compiler: LuaLaTeX
Bibliography: Biber

# Local compilation
lualatex thesis-final
biber thesis-final
lualatex thesis-final
lualatex thesis-final
```

## 📅 Important Deadlines

Check Academic Calendar on FEE CTU website for:
1. Upload complete BT as PDF to KOS (first deadline)
2. Upload final version to KOS (second deadline)
3. Register/enroll for Defense in KOS
