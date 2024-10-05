# MerC
My first EsoLang that uses france memes


hello everyone i coded this early build in 8 hours

NOTICE EARLY BUILD MIGHT GET SOME CHANGES

here are the list of all commands if you are interested

List of Commands



bonjour
Description: Marks the beginning of the program. It must be the first line of the code.
Example:
bonjour
au revoir

Description: Marks the end of the program. It must be the last line of the code.
Example:
au revoir
talktoseniour>

Description: Outputs text to the console. Text can include variables and lists, which will be replaced with their values.
Example:
talktoseniour>Hello, World!<
the eiffel tower <list_name> = [...]

Description: Declares a list with the specified name and initializes it with elements provided inside square brackets.
Example:
the eiffel tower myList = [1, 2, 3]
<var_type> <var_name>

Description: Declares a variable of the specified type (baguette, tea liters, clever joke, or vrai).
baguette: Initializes an integer variable (default is 0).
tea liters: Initializes a float variable (default is 0.0).
clever joke: Initializes a string variable (default is an empty string).
vrai: Initializes a boolean variable (default is False).
Example:
tea liters myTea = 5
<var_name> = <expression>

Description: Assigns a value to a previously declared variable. The expression can be a number, string, list, or an arithmetic operation.
Example:
myTea = myTea + 2
imagine(<condition>)

Description: Evaluates a condition. If true, it executes the subsequent block of code until it encounters meanwhile or au revoir. Supports logical operators AND and OR.
Example:
imagine(myTea > 0 AND baguette count == 0)
meanwhile

Description: Acts as an else statement for an imagine condition. Code following this line is executed if the imagine condition is false.
Example:
meanwhile
make tea until (<condition>)

Description: Begins a loop that continues until the specified condition is true. The loop allows for additional commands to be executed.
Example:
make tea until (myTea == 0 OR baguette count < 5)
wakebacktoreality

Description: Acts as a placeholder to indicate the end of any ongoing commands or loops.
Example:
wakebacktoreality
AmericaWin

Description: Triggers a runtime error, signifying a failure condition (for example, a joke or unexpected state).
Example:
AmericaWin
Examples of Commands in Context
Here’s a small example of how these commands can work together in a program:

bonjour
tea liters = 10
baguette count = 0
the eiffel tower jokes = ["Why did the chicken cross the road?", "Knock Knock!"]

make tea until (tea liters == 0 AND baguette count < 5)
    imagine(baguette count == 0)
        talktoseniour>We need more baguettes!<
    meanwhile
        talktoseniour>We have enough baguettes!<
    baguette count = baguette count + 1
    tea liters = tea liters - 1

wakebacktoreality
au revoir
Logical Operations
The imagine command supports the following logical conditions:

AND: Both conditions must be true for the overall condition to be true.
OR: At least one of the conditions must be true for the overall condition to be true.
Variable Types
Integer: Declared with baguette (e.g., baguette count = 5).
Float: Declared with tea liters (e.g., tea liters = 3.5).
String: Declared with clever joke (e.g., clever joke myJoke = "Hello!").
Boolean: Declared with vrai (e.g., vrai isTrue).
