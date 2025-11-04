from actions.db.connector import restaurant_db, inventory_db, inventory_catalog
from sentence_transformers import SentenceTransformer, util
import random

inventory = inventory_db('./actions/db/inventory.json')
reco_catalog = inventory_catalog('./actions/db/inventory_catalog.json', inventory)

def lookup_item(item_name):
    # Check if the item exists in the inventory and returns it if it does
    #print(f'Looking up item: {item_name}')
    item_id = inventory.get_item_id_by_name(item_name)
    #print(f'Item id: {item_id}')
    if item_id in inventory.inventory_db:
        return True, inventory.inventory_db[item_id]
    else:
        return False, None
    
def compute_cosine_similarity(query, corpus):
    model = SentenceTransformer('all-mpnet-base-v2')
    # Compute the cosine similarity between the query and all items in the corpus
    #print(query, corpus)
    query_embedding = model.encode(query, convert_to_tensor=True)
    corpus_embeddings = model.encode(corpus, convert_to_tensor=True)
    cos_scores = util.pytorch_cos_sim(query_embedding, corpus_embeddings)
    return cos_scores

def get_most_similar_items(user_message):
    # Setup corpus with inventory item names
    corpus = [item['product_name'] for item in inventory.inventory_db.values()]
    query = user_message
    print(f'Corpus: {corpus}, Query: {query}')
    
    # Get the most similar item to the query from the corpus
    cos_scores = compute_cosine_similarity(query, corpus)
    cos_scores = cos_scores.cpu()
    score_list = cos_scores.tolist()[0]
    print(["%.3f" %score for score in score_list])
    top_results = sorted(range(len(score_list)), key=lambda i: score_list[i], reverse=True)[:3]
    return [corpus[i] for i in top_results]

def cosine_explore(user_message):
    # Get the top 3 items to recommend to the user
    top3 = get_most_similar_items(user_message)
    item_keys = [inventory.get_item_id_by_name(item) for item in top3]
    # Update the proposed count for the items
    for item in item_keys:
        reco_catalog.add_item_proposed(item, 1)
    # Write the new catalog
    reco_catalog.write_catalog('./actions/db/inventory_catalog_new.json')
    items_list = [inventory.get_item_by_name(item) for item in top3]
    return top3

def random_explore():
    top3 = random.sample(inventory.inventory_db.keys(), 3)
    names = []
    for item in top3: # update the proposed count and get names of items
        print(item)
        reco_catalog.add_item_proposed(item, 1)
        names.append(inventory.inventory_db[item]['product_name'])
    reco_catalog.write_catalog('./actions/db/inventory_catalog_new.json') # write new catalog
    return [reco_catalog.get_item_by_id(item) for item in top3], names # return the items with their values and their names

def exploit():
    # process item scores
    score = []
    for item in reco_catalog.inventory_catalog:
        if reco_catalog.get_item_proposed(item) != 0:
            score.append(reco_catalog.get_item_clicks(item) / reco_catalog.get_item_proposed(item))
        else :
            score.append(0)
    print(score)
    # order the items by score
    score, items = zip(*sorted(zip(score, reco_catalog.inventory_catalog), reverse=True))
    top3 = items[:3]
    print(score)
    return top3, [inventory.get_item_by_id(item)['product_name'] for item in top3] # return top 3 items and their names



""" for i in range(40): # just to simulate click values for the items and 40 iterations of explore
    reco_catalog.add_item_clicks(str(random.randint(1, 10)),1)
    print(explore())
print(exploit())

print(compute_cosine_similarity('I want a burger', ['I want a burger', 'I want a pizza', 'I want Pasta', 'I want Sushi', 'I want a hot dog'])) # just to test the similarity function
names = []
for item in inventory.inventory_db:
    names.append(inventory.inventory_db[item]['product_name'])
print(compute_cosine_similarity(exploit()[1][0], names)) # just to test the similarity function """

#print(get_most_similar_items('I want Lasagna', ['I want a burger', 'I want a pizza', 'I want Pasta', 'I want a hot dog'])) # just to test the similarity function

#print(get_most_similar_items('I want to eat Pasta')) # just to test the similarity function
#print(cosine_explore('Pasta')) # just to test the similarity function
#print(explore())
#print(f'Recommanded items: {get_most_similar_items("I want to eat Pasta")}')