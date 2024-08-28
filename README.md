# FizzBuzz Implementations

This repository contains the implementation of the FizzBuzz problem in various programming languages.

## Problem Statement
Print the numbers from 1 to 100, but:
- For multiples of three, print "Fizz" instead of the number.
- For multiples of five, print "Buzz".
- For multiples of both three and five, print "FizzBuzz".

## Implementations
Ensure you have necessary interpreters and or libraries for each language installed and pathed correctly to the proper environments

### Python
- **Explanation**: Uses a simple `for` loop with `if-elif-else` statements.
- **Run**: No compilation is needed. Just place the text into a file called fizzbuzz.py and execute the Python script using a python interpreter. I used python 3.9.0 `python fizzbuzz.py`.

### JavaScript
- **Explanation**: The function `fizzBuzz` is defined and called on page load. Outputs are logged to the console.
- **Run**: Include the script in an HTML file, using Node.js or other interpreters/text editors may require additional libraries, since window may not be defined in such environments and will not understand the call to **window.onload**. If using Node.js, save the code in a `.js` file called fizzbuzz.js and run using `node fizzbuzz.js`. 
### Java
- **Explanation**: Implementation is within the `Main` class inside the `main` method.
- **Run**: Compile the Java file using `javac Main.java` and run with `java Main`.

### C#
- **Explanation**: The logic is inside the `Main` method of the `Program` class.
- **Run**: Compile and run using a C# compiler, like `csc Program.cs` followed by `Program.exe`.

### Racket
- **Explanation**: A `for` loop with `cond` statements decides the output for each iteration.
- **Run**: Save the code in a `.rkt` file and run using `racket fizzbuzz.rkt`.

### C
- **Explanation**: The logic resides in the `main` function with `printf` used for output.
- **Run**: Compile the C code using `gcc fizzbuzz.c -o fizzbuzz` and run the output binary using `./fizzbuzz`.

## Challenges Faced
- **Racket**: Handling iteration and formatted output in a functional language required careful usage of `for` and `cond` which I have never done before.
- **C**: Managing the simplicity of C with basic loops and conditionals was straightforward, but careful attention to syntax and formatting was needed.
- **JavaScript**: JavaScript unlike most of the languages I am used to where you need to download a specific interpreter for that one particular language, is unique in that it is interpreted with also html and css kept in mind
