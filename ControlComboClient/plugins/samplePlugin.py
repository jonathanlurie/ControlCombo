

# shows the simplest plugin possible
def helloWorld():
	print(">> From the Sample plugin:  Hello world!")
	

# shows a simple plugin that takes arguments.
# just performs a sum and display it.
def methodWithArguments(number1, number2):
	result = int(number1) + int(number2)
	print(">> what about that: " + str(number1) +  " + " + str(number2) + " = " + str(result))
	
	
	