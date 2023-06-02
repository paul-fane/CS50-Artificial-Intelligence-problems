import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # The list of people example
    #{'Harry': {'name': 'Harry', 'mother':'Lily','father':'James',  'trait': None}, 
    # 'James': {'name': 'James', 'mother': None, 'father': None,    'trait': True}, 
    # 'Lily':  {'name': 'Lily',  'mother': None, 'father': None,    'trait': False}
    # }

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Probabilities dictionary
    #{'Harry': {'gene': {2: 0, 1: 0, 0: 0}, 'trait': {True: 0, False: 0}}, 
    # 'James': {'gene': {2: 0, 1: 0, 0: 0}, 'trait': {True: 0, False: 0}}, 
    #  'Lily': {'gene': {2: 0, 1: 0, 0: 0}, 'trait': {True: 0, False: 0}}}


    # Loop over all sets of people who might have the trait
    names = set(people)
    # names = the set of people name {'Harry', 'James', 'Lily'}

    # print(powerset(names))
    # [set(), {'Harry'}, {'James'}, {'Lily'}, {'Harry', 'James'}, {'Harry', 'Lily'}, {'Lily', 'James'}, {'Harry', 'James', 'Lily'}]

    for have_trait in powerset(names):
        
        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue
        
        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            # [{'Harry'}, {'James'}, {'Lily'}, {'Harry', 'James'}, {'Harry', 'Lily'}, {'Lily', 'James'}, {'Harry', 'James', 'Lily'}]
            # one_gene = Herry
            for two_genes in powerset(names - one_gene):
                # [ {'James'}, {'Lily'}, {'Harry', 'James'}, {'Harry', 'Lily'}, {'Lily', 'James'}, {'Harry', 'James', 'Lily'}]
                # two_genes = James => Lily =>'Harry', 'James' =>'Harry', 'Lily' =>'Lily', 'James'=>'Harry', 'James', 'Lily

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    
    joint_probability = 1
    # {'Harry', 'James', 'Lily'}
    for person in people:

        if person in one_gene:
            copiesOfGenes = 1
        elif person in two_genes:
            copiesOfGenes = 2
        else:
            copiesOfGenes = 0

        if person in have_trait:
            hasTrait = True
        else:
            hasTrait = False

        mother = people[person]['mother']
        father = people[person]['father']

        # If the person does not have one or both parents we need to take the probabilities from the PROBS dictionary
        if mother == None or father == None:
            joint_probability *= PROBS['gene'][copiesOfGenes] * PROBS["trait"][copiesOfGenes][hasTrait]

        # Else for any child, the probability of them having a certain number of genes is conditional on what genes their parents have.
        else:
            # Calculate the probability of mother and father to pass the gene based on how many genes they have
            if mother in one_gene:
                # If the mother has 1 gene, there is a 50% chance of passing on the gene
                probOfMother = 0.5
            elif mother in two_genes:
                # If the mother has 2 genes, she will not pass the gene only if the gene mutate => (1 - 0.01)
                probOfMother = 1 - PROBS['mutation']
            else:
                # If the mother has 0 genes, she can pass the gene only if the gene mutate (0.01)
                probOfMother = PROBS['mutation']

            if father in one_gene:
                probOfFather = 0.5
            elif father in two_genes:
                probOfFather = 1 - PROBS['mutation']
            else:
                probOfFather = PROBS['mutation']
                

            if copiesOfGenes == 1:
                # What’s the probability that the person has 1 copy of the gene? 
                # There are two ways this can happen.
                # Either (he gets the gene from his mother and not his father), or (he gets the gene from his father and not his mother)
                joint_probability *= probOfMother * (1-probOfFather) + probOfFather * (1-probOfMother)
            elif copiesOfGenes == 2:
                # 2 copy of the gene => one from his mother and one from his father
                joint_probability *= probOfMother * probOfFather
            else:
                # Both parents do not transmit the gene
                joint_probability *= (1-probOfMother) * (1-probOfFather)

            # Find the probability that the parson has a specific treat
            joint_probability *= PROBS["trait"][copiesOfGenes][hasTrait]
            

    return joint_probability

        


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:

        if person in one_gene:
            copiesOfGenes = 1
        elif person in two_genes:
            copiesOfGenes = 2
        else:
            copiesOfGenes = 0

        if person in have_trait:
            hasTrait = True
        else:
            hasTrait = False

        probabilities[person]['gene'][copiesOfGenes] += p
        probabilities[person]['trait'][hasTrait] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    # 1/sum = x/trait
    # x=1/sum * trait

    for person in probabilities:
        for field in probabilities[person]:
            sumValue = sum(probabilities[person][field].values())
            for value in probabilities[person][field]:
                probabilities[person][field][value] *= 1/sumValue


if __name__ == "__main__":
    main()
