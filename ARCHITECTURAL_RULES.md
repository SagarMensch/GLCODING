# 🏛️ Architecture & Coding Principles

These 50 principles mandate how all application code should be written, architected, and maintained.

## I. Architectural Supremacy
1. **Conquer Complexity First**: Treat managing complexity as software's primary technical imperative.
2. **Fire Tracer Bullets**: Build end-to-end, skeletal implementations immediately to hit moving targets and get real user feedback, rather than wasting time on disposable prototypes.
3. **Enforce Orthogonality**: Do not split one piece of knowledge across multiple system components; keep your modules strictly independent so changes do not ripple.
4. **DRY (Don't Repeat Yourself)**: Eradicate duplicated knowledge and logic throughout your entire system.
5. **Engineer for Reversibility**: Isolate third-party vendors and databases behind abstract services so you have the flexibility to change them in midstream.
6. **Use Blackboard Systems**: For complex, multi-actor workflows (like Palantir-style data fusion), use blackboard architectures where independent agents post and read from a shared space.
7. **Build Good-Enough Software**: Involve users in the trade-off of deciding when software is ready for the real world instead of chasing impossible perfection.
8. **Design by Contract**: Explicitly define the input domains, preconditions, and postconditions of your routines.
9. **Abstract Your Interfaces**: Ensure every routine in a class interface works toward a consistent, abstracted end, hiding the internal data structures.
10. **Buy vs. Build**: Do not build what you can buy; leverage existing GUI controls, databases, and open-source software to accelerate your development.

## II. The Craft of Code 
11. **Program Into the Language**: Do not just program in a language; bend the language's capabilities to serve your overarching design. 
12. **Establish Conventions Early**: Set programming conventions before you begin; it is nearly impossible to change code to match them later. 
13. **Call Things by Their Proper Name**: Name applications, modules, and variables precisely based on the specific domain vocabulary. 
14. **Document Abbreviations**: Maintain a project-level standard for abbreviations to prevent confusion among programmers reading the code. 
15. **Write Short Functions**: The programs that live best and longest are those built entirely of short, highly focused routines. 
16. **Slide Similar Statements**: Arrange related code items together so they can be easily extracted into new, isolated functions. 
17. **Replace Temps with Queries**: Eliminate local temporary variables by replacing them with declared functions to reduce complex, long routines. 
18. **Measure Complexity**: Count decision points (like if, and, or, while) to track and ruthlessly reduce the cyclomatic complexity of your logic. 
19. **Enter Loops from the Top**: Construct loops cleanly from the inside out, ensuring initialization code is directly before them and they are entered exclusively from the top. 
20. **Code is the Only Documentation**: Recognize that requirements and design docs go out of date, making your source code the only constantly accurate description of the software.

## III. Relentless Refactoring 
21. **Refactor to Understand**: Refactor code continually as an evolutionary process to move knowledge from your head into the system. 
22. **Obey the Rule of Three**: The first time you do something, do it. The second time, wince. The third time you duplicate logic, refactor it. 
23. **Extract Functions Ruthlessly**: Whenever there is a semantic distance between what the code does and how it does it, extract it. 
24. **Eliminate Code Smells**: If code stinks, change it immediately. 
25. **Refactor Duplication**: When the exact same expression exists in two methods of the same class, extract it and invoke the code from both places. 
26. **YAGNI (You Aren't Gonna Need It)**: Do not speculate on future flexibility; build what you need now and rely on refactoring when needs change. 
27. **Do Not Outrun Your Headlights**: Take remarkably small steps during refactoring, ensuring code compiles and passes tests after every minor change. 
28. **Treat Data as Flow**: View data as a continuous flow and think of your programs as pipelines that simply transform inputs into outputs. 
29. **Abstract Data Types**: Hide implementation details inside ADTs so data types can change in one place without breaking the rest of the application. 
30. **Continually Evolve**: Accept that all successful software gets changed, and initial coding consumes a massive portion of the project effort.

## IV. Defensive Engineering 
31. **Dead Programs Tell No Lies**: Catch errors early and crash the program immediately rather than allowing it to continue with corrupted data. 
32. **Assertive Programming**: Leave assertions active in your production code to catch "impossible" conditions (e.g., a month with fewer than 28 days). 
33. **Developer Testing**: Write your own automated tests; testing is the most popular and proven software quality-improvement activity. 
34. **Don't Program by Coincidence**: Never rely on undocumented behavior, accidents, or luck. 
35. **Read the Damn Error Message**: Do not just look at a crash and immediately guess at a code modification; read the actual output. 
36. **Trigger Bugs First**: Get into the debugger and use a failing test to trigger the exact problem before writing a fix. 
37. **Avoid Brute Force Fixing**: Ask yourself if you are guaranteed to fix the problem; avoid wasting hours when a quick, complete rewrite of the routine is better. 
38. **Rely on Compilers**: Use modern compilers and linters to eliminate syntax and typing errors instantly. 
39. **Self-Testing Code**: Realize that you cannot safely modify a legacy enterprise system without automated tests verifying the interfaces. 
40. **Capability Maturity**: Implement systematic, repeatable testing processes with measured feedback to reach the highest level of software quality.

## V. The Hacker's Workbench & Culture 
41. **The Power of Plain Text**: Store your knowledge persistently in plain text so it can be manipulated by any programmatic tool at your disposal. 
42. **Master the Command Shell**: Break free from the limitations of GUIs by building complex macro commands in the shell. 
43. **Automate Manual Procedures**: Do not rely on humans for builds or deployments. Put a shell script under version control so the computer executes it identically every time. 
44. **Use Version Control for Everything**: Track subtle differences and bugs across environments by putting your entire toolchain under version control. 
45. **Pair Program with Discipline**: Support pair programming with strict coding standards so developers focus on the design, not arguing over formatting styles. 
46. **Be an Inquisitive Pack Rat**: Constantly ask questions, explore new paradigms (like quantum computing), and stockpile technical facts. 
47. **Think Critically**: Never accept "because that's the way it's done" or blind vendor promises; always get the facts first. 
48. **Provide Options, Not Excuses**: If a risk materializes, provide alternative solutions. Saying "the cat ate my source code" is entirely unacceptable. 
49. **Take Responsibility**: You own your code. Have a contingency plan for disasters (like your mass storage melting). 
50. **No One Knows What They Want**: Recognize that requirements always drift; use your architecture and agility to survive the shifting landscape.
