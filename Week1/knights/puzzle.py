from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")


# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # The caracter can be a knight or a knave, not both 
    Or(AKnight, AKnave), 
    Not(And(AKnight, AKnave)),

    # The caracter is a Knight if the sentence that he is both a knight and a knave is true
    Implication(AKnight, And(AKnight, AKnave)),
    # Else, if the sentence is not true, the character is a lier.
    Implication(AKnave, Not(And(AKnight, AKnave)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # A caracter can be a knight or a knave, not both 
    Or(AKnight, AKnave), 
    Or(BKnight, BKnave),
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),

    # The caracter A is a knight if the sentence that they are both knaves is true
    Implication(AKnight, And(AKnave, BKnave)),
    # Else the caractere A is a Knave if they are not both knaves
    Implication(AKnave, Not(And(AKnave, BKnave)))
    # B says nothing
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # A caracter can be a knight or a knave, not both 
    Or(AKnight, AKnave), 
    Or(BKnight, BKnave),
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),

    # Character A: A is a knight if his sentence is true. The same kind it means both caracters Knaves or both Knights
    Biconditional(AKnight, Or(And(AKnave, BKnave), And(AKnight, BKnight)) ),
    # Character B: B is a knight if his sentence is true. One of them knave, another knight
    Biconditional(BKnight, Or(And(AKnave, BKnight), And(AKnight, BKnave)) ),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # A caracter can be a knight or a knave, not both
    Or(AKnight, AKnave), 
    Or(BKnight, BKnave),
    Or(CKnight, CKnave),
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),
    Not(And(CKnight, CKnave)),

    # Character A: A is a knight if his sentence that "he is a knight or knave" is true
    Biconditional(AKnight, Or(AKnave, AKnight)),
    # Character B: A knight said that B is a knave. Only if A is knight B will be knave
    Biconditional(AKnight, BKnave),
    # Character B: B is a knight if his sentence that "C is a knave" is true
    Biconditional(BKnight, CKnave),
    # Character C: C is a Knight if his sentence that "A is a knight" is true
    Biconditional(CKnight, AKnight)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
