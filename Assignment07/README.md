# Assignment 07 — oo-comparison

Comparing how Python and C++ implement objects.

**Author:** Adam Edwards
**Course:** CS 414 Programming Languages, Dr. Lewis
**Report:** [docs/report.pdf](docs/report.pdf)

This folder is the `oo-comparison` deliverable.

## Layout

```
Assignment07/
    README.md
    cpp/
        CMakeLists.txt
        nonvirtual_diamond.cpp    Part 1
        virtual_diamond.cpp       Parts 2 and 4 (C++)
    python/
        cooperative_diamond.py    Parts 3 and 4 (Python)
    docs/
        report.pdf
```

## Requirements

- Windows with Visual Studio (MSVC, C++20)
- CMake 3.16 or newer
- Python 3 (tested with Python 3.14 in Anaconda `base`; only the standard library is used)

## Build and run the C++ programs

Open **Developer PowerShell for VS**, then:

```powershell
cd cpp
cmake -S . -B build
cmake --build build
.\build\Debug\nonvirtual_diamond.exe
.\build\Debug\virtual_diamond.exe
```

## Run the Python program

Open **Anaconda PowerShell Prompt** (or any terminal with Python 3), then from `Assignment07`:

```powershell
python python\cooperative_diamond.py
```

## Reproducing the compiler diagnostics

The invalid code is kept in the source, commented out. To see each error,
remove the comment, rebuild with `cmake --build build`, then restore the comment.

| File | Code to uncomment | MSVC error |
|------|-------------------|------------|
| `nonvirtual_diamond.cpp` | `std::cout << ta.name << '\n';` | C2385: ambiguous access of 'name' |
| `nonvirtual_diamond.cpp` | `Person* person = &ta;` | C2594: ambiguous conversions from 'TeachingAssistant *' to 'Person *' |
| `virtual_diamond.cpp` | Comment out `TeachingAssistant::role()` | C2250: ambiguous inheritance of 'Person::role(void) const' |
| `virtual_diamond.cpp` | `announce_person(robot);` | C2664: cannot convert argument 1 from 'RobotAssistant' to 'const Person &' |

To see Python's `role()` lookup without an override, comment out
`TeachingAssistant.role()` in `cooperative_diamond.py` and rerun. `ta.role()`
then prints `Student`, the first `role()` found in the MRO.

## AI Help

Claude (Anthropic) helped draft the source files, `CMakeLists.txt`, this README,
and the report. Each source file's header has an `AI Help:` line.