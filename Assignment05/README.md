# Assignment 05: Transactional Key-Value Store

CS 414 - Adam Edwards

A small key-value store with string keys and string values, written twice:
once in C++ (`cpp`) and once in OCaml (`ocaml`). Both programs accept the
same commands, print the same output, and read and write the same file format.

AI Help: Claude helped design and write the code, the tests, and this README.
Each source file notes this in its header comment.

## Requirements

- C++: Visual Studio with the C++ tools and CMake (built with MSVC 19.51, C++20)
- OCaml: opam, dune, and Alcotest (built with OCaml 5.4.1, dune 3.24)

## C++

Run these from a Developer PowerShell for VS, starting in the `cpp` folder.

Build:

```powershell
cmake -S . -B build
cmake --build build
```

Run the program:

```powershell
.\build\Debug\kvstore.exe
```

Run the tests:

```powershell
.\build\Debug\store_tests.exe
```

The tests print one PASS or FAIL line per check and end with `All tests passed`.

## OCaml

Run these from PowerShell, starting in the `ocaml` folder.

Load the opam environment (once per PowerShell window):

```powershell
(& opam env) -split '\r?\n' | ForEach-Object { Invoke-Expression $_ }
```

Install Alcotest if it is not already installed:

```powershell
opam install alcotest
```

Build:

```powershell
dune build
```

Run the program:

```powershell
dune exec kvstore
```

Run the tests:

```powershell
dune test
```

## Commands

Both programs show a `> ` prompt and accept these commands:

| Command | What it does |
|---|---|
| `SET key value` | Stores the value under the key. The value may contain spaces. |
| `GET key` | Prints the value, or `key not found`. |
| `DELETE key` | Removes the key, or prints `key not found`. |
| `LIST` | Prints every pair as `key = value`, sorted by key. |
| `SAVE filename` | Writes the store to a file. |
| `LOAD filename` | Replaces the store with the contents of a file. |
| `QUIT` | Exits. |

If a file cannot be opened, `SAVE` and `LOAD` print `could not open file`
and the store is left as it was.

## Sample data file

`data.txt` is a sample file written by `SAVE`. Each line is one pair: the key,
a space, then the value.

```
course CS 414
language OCaml
name Ada
```

To load it in the C++ program, start the program from the `Assignment05` folder:

```powershell
.\cpp\build\Debug\kvstore.exe
```

then enter `LOAD data.txt` and `LIST`.

To load it in the OCaml program, start the program from the `ocaml` folder with
`dune exec kvstore`, then enter `LOAD ..\data.txt` and `LIST`.

## Written comparison

The comparison of the two implementations is in the `docs` folder.
