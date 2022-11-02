import wikipedia

result = wikipedia.search("what is brazil?", results = 1)
page_object = wikipedia.page(result[0])
print(dir(page_object)
print(page_object.content)