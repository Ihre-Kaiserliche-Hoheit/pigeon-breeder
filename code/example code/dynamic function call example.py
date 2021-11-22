
# Dynamic function calls

def hello():
	print("Hello") # Prints hello
def world():
	print("World!") # Prints world

calls = {
	"hello":hello, # Links hello function to the dictionary key hello
	"world":world # Same as above but for world
}

calls["hello"]() # This calls the function as linked in calls
