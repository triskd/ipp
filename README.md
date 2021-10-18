# Syntaktický analyzátor a interpret jazyka IPPcode20
## Seznam souborů
```
.
├── input
│   └── empty
├── interpret
│   ├── interpret.py
│   └── lib_interpret
│       ├── Frame.py
│       ├── Instruction.py
│       ├── Interpret.py
│       ├── Killer.py
│       └── Variable.py
├── ipp20spec.pdf
├── parser
│   ├── lib
│   │   ├── Instr.php
│   │   ├── Killer.php
│   │   └── Prog.php
│   ├── parse.php
│   └── rozsireni
└── programs
    ├── fibonaci
    ├── fibonaci.ippcode20
    ├── helloworld10x
    ├── helloworld10x.ippcode20
    ├── read
    ├── read.ippcode20
    └── zadani
```
## Použití
- zdrojový kód jazyka IPPcode20 se nejprve musí zkontrolovat jeho syntaktická správnost použitím scriptu parser/parser.php, tento script načítá zrdojový program ze stdin, pokud je program syntaktický správný vrací na stdout xml reprezentaci zdrojového kódu, která je vstupem pro interpret - script interpret/interpret.py
- interpret musí mít vždy zadaný, alespoň jeden z argumentů --source="xml reprezentace zdrojového kódu" nebo --input="soubor obsahující vstupy, které bude zdrojový kód požadovat", pokud jeden z těchto armentů chybí bude načítán z stdin
- v adresáři programs jsou příklady jednoduchých programů napsaných v jazyce IPPcode20, soubory s příponou .ippcode20 obsahují xml reprezenataci programu určenou pro interpret
## Spustění
#### parser:
 -  $ php7.0 parser/parser.php < programs/fibonaci 
#### interpret:
  - $ python3 interpret/interpret.py --source="programs/fibonaci.ippcode20"

