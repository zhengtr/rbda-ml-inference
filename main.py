from detoxify import Detoxify

results = Detoxify('original', device='cuda').predict('example text')
print(results)