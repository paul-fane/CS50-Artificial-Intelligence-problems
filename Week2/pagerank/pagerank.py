import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    pagesProbability = {}

    # If page has no outgoing links
    if len(corpus[page]) == 0:
        # Then give equal probability to each page in corpus 
        # The keys method will return the keys(page), not the valus of each key(link)
        for item in corpus.keys():
            # Divide the total of 1(100%) to all the pages to have the probability of a single page
            pagesProbability[item] = 1/len(corpus)

    # Else => the page has links(to other pages) => Calculate probability of each page
    else:

        # To each link in the current page add his (damping_factor) probability + (1-damping_factor) probability 
        for link in corpus[page]:
            # The (damping_factor) probability is equal to (damping_factor) divided to all the links in the page
            # The (1-damping_factor) probability is equal to (1-damping_factor) divided to all the existing pages
            pagesProbability[link] = (damping_factor/len(corpus[page])) + ((1-damping_factor)/len(corpus))

        # To all the others pages remaining in the corpus add only the (1-damping_factor) probability 
        for item in corpus.keys():
            # If the item is not in pagesProbability it means that the item was not a link in the current page
            if item not in pagesProbability:
                pagesProbability[item] = (1-damping_factor)/len(corpus)

    return pagesProbability
            


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # How many times each page was visited
    pageCount = {}

    # Initialize the count for any page to 0
    for page in corpus.keys():
        pageCount[page] = 0

    # Select a random first page to start
    firstChoice = random.choice(list(corpus.keys()))

    # Count also the first page
    pageCount[firstChoice] += 1

    # Calculate transition_model of firstChoice
    transitionProbability = transition_model(corpus, firstChoice, damping_factor)

    for i in range(n-1):
        # Randomly a page will be choosen based on the weights of the transition_model
        page = random.choices(population=list(transitionProbability.keys()), weights=list(transitionProbability.values()), k=1)[0]
        # Add 1 to the choosen page to increment the count of haw many times the page was visited
        pageCount[page] += 1

        # Calculate transition_model of current page
        transitionProbability = transition_model(corpus, page, damping_factor)

    # Pagename : Rank
    pageRank = {}

    # Iterate dictionary key-value pairs: items()
    # Key => page , Value => countNumber
    for (key, value) in pageCount.items():
        # For each page calculate his value between 0-1 => divide the totalCount of the page to the total number of counts(samples)
        pageRank[key] = value/n

    return pageRank

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pageRank = {}
    # The convergence will be set to true if the difference between the old probability and the new one is <= 0.0001
    convergencePage = {}

    # Set equal rank to each page and initialize the convergence to false
    startRank = 1/len(corpus)
    for page in corpus.keys():
        pageRank[page] = startRank
        convergencePage[page] = False

    # with probability 1-d
    #(1-damping_factor)/len(corpus)

    # Repeatedly calculate new rank values based on all of the current rank values (pageRank)
    # The formula => (1-damping_factor)/len(corpus) + damping_factor * pageRank(i)/NumLinks(i)
    # NumLinks(i)=> the number of links on page (i)


    # While convergence == false => Continue calculate new more precise probability for each page
    while not all(convergencePage.values()):

        # For each page calc the probability
        for page1 in corpus.keys():

            # Save the current rank, to calculate later the convergence with the new rank
            currentRank = pageRank[page1]

            # Calc the sum of each page(i)/NumLinks(i) => Only if the page(i) links to page1
            sum = 0
            for (keyPage2, valuePage2) in corpus.items():
                # A page that has no links at all should be interpreted as having one link for every page in the corpus (including itself).
                if len(valuePage2) == 0:
                    sum += pageRank[keyPage2]/len(corpus)
                    
                # Add to the sum only if the other page(keyPage2) links to page1
                elif page1 in valuePage2:
                    sum += pageRank[keyPage2]/len(valuePage2)

            # PR(p) = (1-d)/N + d* sum
            pageRank[page1] = (1-damping_factor)/len(corpus) + damping_factor * sum

            # Calc the convergence between the currentRank and the newRank (pageRank[page1])
            if abs(currentRank - pageRank[page1]) <= 0.0001:
                convergencePage[page1] = True

    return pageRank


if __name__ == "__main__":
    main()
