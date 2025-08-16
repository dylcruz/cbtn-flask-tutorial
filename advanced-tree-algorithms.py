my_tree = {
    'value': 1,
    'children': [{
        'value': 2,
        'children': [{
            'value': 99
        }, {
            'value': 100
        }]
    }, {
        'value': 3,
        'children': [{
            'value': 4
        }, {
            'value': 5
        }]
    }]
}

def tree_contains(tree, predicate):
    if predicate(tree['value']):
        return True
    
    if 'children' not in tree:
        return False
    
    for child in tree['children']:
        if tree_contains(child, predicate):
            return True
        
    return False

def is_even(x):
    return x % 2 == 0

# print(tree_contains(my_tree, is_even))

def map_tree(tree, transform):
    new_tree = { **tree }
    new_tree['value'] = transform(new_tree['value'])

    if 'children' not in tree:
        return new_tree
    
    new_children = []
    for child in new_tree['children']:
        new_children.append(map_tree(child, transform))

    new_tree['children'] = new_children

    return new_tree

def fitler_tree(tree, predicate):
    new_tree = { **tree }
    matches = predicate(tree['value'])

    if 'children' not in tree:
        if matches:
            return tree
        else:
            return None
    
    if not matches:
        del new_tree['value']
    
    new_children = []

    for child in new_tree['children']:
        result = fitler_tree(child, predicate)
        if result:
            new_children.append(result)

    new_tree['children'] = new_children

    return new_tree

def reduce_tree(tree, accumulate, default_value):
    if 'children' not in tree:
        return tree['value']
    
    result = tree.get('value') or default_value

    for child in tree['children']:
        result = accumulate(
            result, 
            reduce_tree(child, accumulate, default_value)
        )
    
    return result

def print_tree(tree, level=0):
    if 'value' in tree:
        print(f"+{'-' * level}{tree['value']}")
    else: 
        print(f"+{'-' * level}(empty)")

    if 'children' not in tree:
        return
    
    for subtree in tree['children']:
        print_tree(subtree, level+1)

def double(x):
    return x * 2

# print_tree(
#     map_tree(my_tree, double)
# )

print_tree(
    fitler_tree(my_tree, is_even)
)

def add(acc, x):
    return acc + x

print(reduce_tree(my_tree, add, 0))
