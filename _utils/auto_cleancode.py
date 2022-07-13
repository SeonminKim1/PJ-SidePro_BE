import os

os.system("black ./")
print("=== black : Code Clean-up Finished ~!")
os.system("isort ./")
print("=== isort : Code Alignment Done ~!")
