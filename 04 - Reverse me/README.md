# lancer le container 
docker run -it ubuntu

# debboguer avec gdb:
gdb ./level1

# desassembler avec objdump:
objdump -d ./level1 > level1.asm

# tracer les appels système avec strace:
strace ./level1

# ----------------Marche à suivre---------------

1) regarder comment faire du reverse en reverse engineering:
- gdb
- strace
- strings

# ----------------------------------------------

# faire tourner gdb:

gdb ./level1

lay next

# breakpoint pour faire stopper gdb

break main

# start the program
run

# go to the next line 
next
ou nexti ("next instruction")

# go to the next step (not the next line)
step

# clean the screen (?)
ref

# examiner l'instruction
x/i $pc (why pc ?)