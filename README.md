# ⚡ Velox-Lang
Velox-Lang is a simple, educational programming language interpreter written from scratch in Python. It includes its own lexer, parser, and evaluator (AST-based) layers. It uses Turkish keywords and runs through an interactive REPL (live terminal).
This project is designed for anyone who wants to learn/understand from scratch how a programming language works (tokenization → parsing → AST → evaluation).

## ✨ Features
- 🔢 Working with numbers (integers)
- 🔤 String support and concatenation with `+`
- 📦 Variable definition and access (`deger`)
- 🖨️ Printing to screen (`yaz`)
- 🔀 Conditional statements (`eger` / `yoksa`)
- ➕ Arithmetic operators: `+ - * /`
- 🔍 Comparison operators: `== != < >`
- 💬 Interactive REPL (live terminal) interface

## 📥 Installation
Only Python 3 is required to run the project (no external dependencies).
```bash
git clone https://github.com/your-username/velox-lang.git
cd velox-lang
python3 main.py
```

## 🚀 Usage
When you run the program, you'll be greeted with the `velox >` prompt:
```
=============================================
 ⚡ VELOX-LANG v1.2 (String & Text Support) ⚡
 Type 'cikis' to exit.
=============================================
velox >
```
You can type `cikis` to exit.

### Defining variables
```
velox > deger x = 10
velox > yaz(x)
10
```

### Using and concatenating strings
```
velox > deger isim = "World"
velox > yaz("Hello, " + isim)
Hello, World
```

### Arithmetic operations
```
velox > yaz(5 + 3 * 2)
11
```

### Comparison operations
```
velox > yaz(5 > 3)
1
velox > yaz(5 == 3)
0
```

### Conditional statements (`eger` / `yoksa`)
```
velox > eger (5 > 3) { yaz("big") } yoksa { yaz("small") }
big
```

## 🧠 Language Syntax Summary
| Keyword / Operator | Meaning |
|---|---|
| `deger` | Variable definition |
| `yaz(...)` | Print to screen |
| `eger (...) { ... }` | If condition |
| `yoksa { ... }` | Else block |
| `+ - * /` | Arithmetic operators |
| `== != < >` | Comparison operators |
| `"..."` | String literal |

## 🏗️ Project Architecture
The interpreter consists of 4 classic layers:
1. **Lexer** – Splits source code into tokens (regex-based).
2. **Parser** – Converts the token sequence into an AST (Abstract Syntax Tree) structure.
3. **AST Nodes** – `NumberNode`, `StringNode`, `BinOpNode`, `VarAssignNode`, `IfNode`, etc.
4. **Interpreter (Evaluator)** – Traverses the AST (visitor pattern) to compute/execute the result.
```
main.py
├── lexer()          # Source code -> Token list
├── Parser            # Token list -> AST
├── AST Node classes
└── Interpreter        # AST -> Result
```

## 🗺️ Roadmap (Ideas)
- [ ] Loops (`iken`, `tekrar`, etc.)
- [ ] Function definition support
- [ ] Lists / arrays
- [ ] Comment lines (`//` or `#`)
- [ ] Running code from files (`.vlx` extension files)
- [ ] Line/column info in error messages

## 🤝 Contributing
Contributions are welcome! You can open an issue or submit a pull request directly.

## 📄 License
This project is licensed under the [MIT License](LICENSE).
