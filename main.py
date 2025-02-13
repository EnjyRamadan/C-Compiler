from GUI import CompilerApp
import tkinter as tk
import math


class Scanner:
    def __init__(self, app) -> None:
        self.arr_dict = {}
        self.app = app
        self.loop_parts = []
        self.varValues = {}
        self.symbols = {
            "+": "Operator",
            "-": "Operator",
            "*": "Operator",
            "%": "Operator",
            "(": "Open Bracket",
            ")": "Close Bracket",
            "{": "Open Curly Bracket",
            "}": "Close Curly Bracket",
            ",": "Comma",
            ";": "Semicolon",
            "&&": "And",
            "||": "Or",
            "<": "Less than",
            ">": "Greater than",
            "=": "Equal",
            "!": "Not",
            "[": "Open Square Brackets",
            "]": "Closed Square Brackets",
        }
        self.reserved_words = [
            "for",
            "while",
            "if",
            "do",
            "return",
            "break",
            "continue",
            "end",
            "else",
            "switch",
            "case",
        ]
        self.identifiers = ["int", "float", "string", "double", "bool", "char"]
        self.defined_variables = []
        self.found_reserved = []
        self.values = []
        self.errors = []
        self.lineIdentify = []

    def scan(self):
        self.lineIdentify = []
        self.defined_variables = []
        self.found_reserved = []
        self.values = []
        self.errors = []
        self.arr_dict = {}
        self.app = app
        self.loop_parts = []
        self.varValues = {}
        num_lines = int(self.app.text_editor.index("end-1c").split(".")[0])
        for line_num in range(1, num_lines + 1):
            line_content = self.app.text_editor.get(f"{line_num}.0", f"{line_num}.end")
            words = line_content.split(" ")
            self.analyze_sentence(words, line_num)
        self.validate_syntax()
        if len(self.errors) == 0:
            self.compileMemory()

    def analyze_sentence(self, line_content, line_num):
        f_Identifier = 0
        start_index = 0
        num = ""
        for word in line_content:
            f = 0
            number = []
            s = ""
            for index, letter in enumerate(word):
                s += letter
                if s in self.symbols.keys() or letter in self.symbols.keys():
                    if letter in self.symbols.keys():
                        if letter == "]" and f == 1:
                            if temp not in self.varValues:
                                self.varValues[temp] = []
                            self.varValues[temp].append(number)
                            self.arr_dict[temp] = number
                            f = 0
                            if len(number) == 1:
                                app.output_console.insert(
                                    f"{line_num}.end",
                                    f" array {temp} of size {number[0]} \n",
                                )
                            else:
                                app.output_console.insert(
                                    f"{line_num}.end",
                                    f" array {temp} of size {len(number)} \n",
                                )
                                for index, element in enumerate(number):
                                    app.output_console.insert(
                                        f"{line_num}.end",
                                        f" array {temp} elemnt number {index + 1} has value {element} \n",
                                    )
                    f_Identifier = 0
                    s = ""
                elif s in self.reserved_words:
                    word_index = line_content.index(word, start_index)
                    word_length = len(s)
                    self.found_reserved.append(
                        (line_num, s, word_index, word_index + word_length)
                    )
                    s = ""
                elif s in self.identifiers:
                    f_Identifier = 1
                    self.lineIdentify.append(line_num)
                    s = ""
                elif (
                    index == len(word) - 1
                    or (
                        word[index + 1] == "&"
                        or word[index + 1] == "|"
                        or word[index + 1] in self.symbols.keys()
                    )
                    and s != ""
                ):
                    if s.isnumeric():
                        if f == 1:
                            number.append(int(s))
                    else:
                        if f_Identifier == 1:
                            self.defined_variables.append(s)
                            if s not in self.varValues:
                                self.varValues[s] = []
                            if word[index + 1] == "=":
                                if s not in self.varValues:
                                    self.varValues[s] = []
                            i = index + 2
                            while i < len(word) and word[i] != ";":
                                num += word[i]
                                i += 1
                            if num.isnumeric():
                                self.varValues[s].append(int(num))
                            f_Identifier = 0
                        if index + 1 < len(word):
                            temp = s if word[index + 1] == "[" else ""
                            if not (temp == ""):
                                f = 1
                    s = ""

    def validateCondition(self, cond, Line):
        words = cond.split(" ")
        if cond == "":
            self.errors.append(f"There is No Condition in line: {Line}")
        i = 0
        while i < len(words):
            if i > 0:
                token = words[i]
                if token in ["==", "!=", "&&", "||", "<", ">", "<=", ">="]:
                    # Compound conditions and comparison operators
                    if (
                        words[i - 1] not in self.defined_variables
                        and not words[i - 1].isnumeric()
                    ) or (
                        words[i + 1] not in self.defined_variables
                        and not words[i + 1].isnumeric()
                    ):
                        self.errors.append(
                            f"There is an error in Line {Line}: Invalid operands in condition"
                        )
                elif token in ["!", "&", "|"]:
                    # Single logical operators
                    if token == "&":
                        expected = "&&"
                    elif token == "|":
                        expected = "||"
                    elif token == "!":
                        expected = "!="
                    if words[i + 1] != expected:
                        self.errors.append(
                            f"There is an error in Line {Line}: Missing or incorrect logical operator"
                        )
                elif token == "=":
                    # Check if it's a legitimate comparison or an assignment statement
                    if (
                        words[i - 1] not in self.defined_variables
                        or words[i + 1] != "="
                    ):
                        self.errors.append(
                            f"There is an error in Line {Line}: Assignment statement found within condition"
                        )
                i += 1
            else:
                i += 1

    def checkBrackets(self):
        num_lines = int(self.app.text_editor.index("end-1c").split(".")[0])
        openBracketFlag = False
        ctOpenBrackets = 0
        ctClosedBrackets = 0
        ctCloseCurlyBrackets = 0
        ctOpenCurlyBrackets = 0
        for line_num in range(0, num_lines + 1):
            line_content = self.app.text_editor.get(f"{line_num}.0", f"{line_num}.end")
            words = line_content.split(" ")
            for word in words:
                if word == "(":
                    ctOpenBrackets += 1
                elif word == ")" and openBracketFlag:
                    ctClosedBrackets += 1
                elif openBracketFlag:
                    cond += word + " "
                if word == "{":
                    ctOpenCurlyBrackets += 1
                    continue
                elif word == "}":
                    ctCloseCurlyBrackets += 1
        if ctOpenBrackets < ctClosedBrackets:
            self.errors.append(f"in Line {line_num}: there is Missing Open Brakets")
        if ctOpenCurlyBrackets < ctCloseCurlyBrackets:
            self.errors.append(
                f"in Line {line_num}: there is Missing Open Curly Brakets"
            )
        elif ctCloseCurlyBrackets < ctOpenCurlyBrackets:
            self.errors.append(
                f"in Line {line_num}: there is Missing Closed Curly Brakets"
            )

    def validateIf(self, info):
        cond = ""
        elseflag = False
        openCurlyBracketCt = 0
        openBracketFlag = False
        openCurlyBracketFlag = False
        elseOpenCurlyBracketsflag = False
        num_lines = int(self.app.text_editor.index("end-1c").split(".")[0])
        for lineNum in range(info[0], num_lines + 1):
            line_content = self.app.text_editor.get(f"{lineNum}.0", f"{lineNum}.end")
            words = line_content.split(" ")
            for index, word in enumerate(words):
                if word == "(":
                    openBracketFlag = True
                elif word == ")" and openBracketFlag:
                    openBracketFlag = False
                elif word == "{":
                    openCurlyBracketFlag = True
                    openCurlyBracketCt += 1
                elif word == "}" and openCurlyBracketFlag:
                    openCurlyBracketFlag = False
                    openCurlyBracketCt -= 1
                elif openBracketFlag:
                    cond += word + " "
                if openCurlyBracketFlag and openCurlyBracketCt > 0 and word == "else":
                    self.errors.append(
                        f"There is an else inside the if condition while it should be outside in line {lineNum}"
                    )
                if not openCurlyBracketFlag and openCurlyBracketCt > 0:
                    if word == "else":
                        elseflag = True
                if elseflag:
                    if words[index - 1] == "else" and word == "{":
                        elseOpenCurlyBracketsflag = True
                    if elseOpenCurlyBracketsflag and word == "}":
                        elseOpenCurlyBracketsflag = False
                        elseflag = False
            if elseflag and elseOpenCurlyBracketsflag:
                self.errors.append(
                    f"There is no closing curly brackets for the else in line {lineNum}"
                )
            if openBracketFlag:
                self.errors.append(
                    f"Unclosed parenthesis in the if statement in line {lineNum}"
                )
            elif elseflag and not elseOpenCurlyBracketsflag:
                self.errors.append(f"Else without an Curly Brackets in line {lineNum}")
            elif elseflag:
                self.errors.append(
                    f"Else without an accompanying if statement in line {lineNum}"
                )
        if cond.strip() != "":
            self.validateCondition(cond, info[0])

    def showError(self):
        self.checkBrackets()
        line_number = 1
        if len(self.errors) > 0:
            for error in self.errors:
                app.output_console.insert(tk.END, f"{line_number}. {error}\n")
                line_number += 1
        else:
            app.output_console.insert(
                tk.END, f"The Memory is at Start and at the End\n"
            )
            for var in self.varValues:
                firstValue = (
                    self.varValues[var][0] if len(self.varValues[var]) > 0 else None
                )
                lastValue = (
                    self.varValues[var][-1] if len(self.varValues[var]) > 0 else None
                )
                app.output_console.insert(
                    tk.END,
                    f"{line_number}. {var}: {firstValue} -> {lastValue} \n",
                )
                line_number += 1

    def validateSwitch(self, info):
        num_lines = int(self.app.text_editor.index("end-1c").split(".")[0])
        openBracketFlag = False
        ctOpenBrackets = 0
        openCurlyBracketFlag = False
        ctOpenCurlyBrackets = 0
        caseFlag = False
        cond = ""
        for lineNum in range(info[0], num_lines + 1):
            line_content = self.app.text_editor.get(f"{lineNum}.0", f"{lineNum}.end")
            words = line_content.split(" ")
            for index, word in enumerate(words):
                if index == 0:
                    for letter in word:
                        if letter == "(":
                            ctOpenBrackets += 1
                            openBracketFlag = True
                            continue
                        elif letter == ")" and openBracketFlag:
                            ctOpenBrackets -= 1
                            if ctOpenBrackets == 0:
                                openBracketFlag = False
                        elif openBracketFlag and not openCurlyBracketFlag:
                            cond += letter
                if word == "{":
                    ctOpenCurlyBrackets += 1
                    openCurlyBracketFlag = True
                    continue
                if word == "case":
                    if caseFlag:
                        cond += " || "
                    word = words[index + 1]
                    word = word[:-1]
                    cond += " == " + word
                    caseFlag = True
                elif word == "}" and openCurlyBracketFlag:
                    ctOpenCurlyBrackets -= 1
        if not caseFlag:
            self.errors.append(
                f"in Line {lineNum}: there is wrong structure of switch operation"
            )
        if ctOpenBrackets > 0:
            self.errors.append(f"in Line {lineNum}: there is Missing Open Brakets")

    def validateWhile(self, line_num, word, flag):
        if word == "while" and flag == 0:
            line_content = self.app.text_editor.get(f"{line_num}.0", f"{line_num}.end")
            cond = line_content.split("while")[1].strip()
            self.loop_parts.append([line_num, cond[1:-4]])
            curly_bracket_found = False
            closing_bracket_found = False
            open_bracket_found = False
            closed_bracket_found = False
            if "(" in line_content:
                open_bracket_found = True
            if ")" in line_content:
                closed_bracket_found = True
            for i in range(
                line_num, len(self.app.text_editor.get("1.0", "end").split("\n"))
            ):
                next_line_content = self.app.text_editor.get(f"{i}.0", f"{i}.end")
                if "{" in next_line_content:
                    curly_bracket_found = True
                if "}" in next_line_content:
                    closing_bracket_found = True
            if not (curly_bracket_found):
                self.errors.append(
                    f"Missing opening Curly brackets in 'while' loop at or after line {line_num}"
                )
            if not (closing_bracket_found):
                self.errors.append(
                    f"Missing closed Curly brackets in 'while' loop at or after line {line_num}"
                )
            if not (open_bracket_found):
                self.errors.append(
                    f"Missing opening parentheses in 'while' loop at or after line {line_num}"
                )
            if not (closed_bracket_found):
                self.errors.append(
                    f"Missing closed parentheses in 'while' loop at or after line {line_num}"
                )
        elif word == "do":
            line_content = self.app.text_editor.get(f"{line_num}.0", f"{line_num}.end")
            do_index = line_content.find("do")
            while_index = line_content.find("while")
            open_bracket_index = line_content.find("{")
            close_bracket_index = line_content.find("}")
            open_line = -1
            close_line = -1
            while_line = ""
            i = line_num + 1
            while i <= len(self.app.text_editor.get("1.0", "end").split("\n")):
                next_line_content = self.app.text_editor.get(f"{i}.0", f"{i}.end")
                if "{" in next_line_content and open_bracket_index == -1:
                    open_bracket_index = next_line_content.find("{")
                    open_line = i
                if "}" in next_line_content and close_bracket_index == -1:
                    close_bracket_index = next_line_content.find("}")
                    close_line = i
                if "while" in next_line_content and while_line == "":
                    while_index = next_line_content.find("while")
                    while_line = next_line_content
                i += 1
            print(while_index, " ", open_bracket_index, " ", close_bracket_index)
            if (
                do_index != -1
                and while_index != -1
                and open_bracket_index != -1
                and close_bracket_index != -1
                and do_index < open_bracket_index
                and open_line < close_line
                and while_index > close_bracket_index
                and while_line[close_bracket_index + 1 : while_index].strip() == ""
                and while_line[while_index + 5 :].strip().startswith("(")
                and while_line[while_index + +5 : -1].strip().endswith(")")
                and while_line.endswith(";")
            ):
                cond = while_line[while_index + 5 : -1].strip()[1:-1]
                self.validateCondition(cond, line_num)
            else:
                # Invalid do...while loop structure
                self.errors.append(f"Invalid 'do...while' loop at line {line_num}")
                if open_line == -1:
                    self.errors.append(
                        f"Missing opening curly bracket in 'do' loop at line {line_num}"
                    )
                if close_line == -1:
                    self.errors.append(
                        f"Missing closing curly bracket in 'do' loop at line {line_num}"
                    )
                if while_index == -1:
                    self.errors.append(
                        f"Missing 'while' keyword in 'do' loop at line {line_num}"
                    )
                if "(" not in line_content or ")" not in line_content:
                    self.errors.append(
                        f"Missing parentheses after 'while' keyword in 'do' loop at line {line_num}"
                    )

    def validateCase(self, reserved, index):
        if self.found_reserved[index - 1][1] != "switch":
            self.errors.append(
                f"In Line {reserved[0]} There is Case that isn't inside Switch Operation"
            )
        else:
            if index + 1 < len(self.found_reserved):
                if self.found_reserved[index + 1][1] != "break":
                    self.errors.append(
                        f"In Line {reserved[0]} There is Case that doesn't have break after it"
                    )
            else:
                self.errors.append(
                    f"In Line {reserved[0]} There is Case that doesn't have break after it"
                )

    def validateElse(self, reserved, i):
        if self.found_reserved[i - 1][1] != "if":
            self.errors.append(
                f"In Line {reserved[0]} There is else that isn't after if Operation"
            )

    def group_words(self, word_list):
        words = []
        current_word = ""
        for sublist in word_list:
            for char in sublist:
                if char.isalpha():
                    current_word += char
                elif current_word:
                    words.append(current_word)
                    current_word = ""
            if current_word:
                words.append(current_word)
                current_word = ""
        return words

    def validate_syntax(self):
        skip = 0
        num_lines = int(self.app.text_editor.index("end-1c").split(".")[0])
        for i, reserved in enumerate(self.found_reserved):
            line_num, word, index, end_index = reserved
            if word == "while" or word == "do":
                if skip == 0 and word == "do":
                    skip = 1
                if skip != 1 or word != "while":
                    self.validateWhile(line_num, word, skip)
            elif word == "if":
                self.validateIf(reserved)
            elif word == "switch":
                self.validateSwitch(reserved)
            elif word == "case":
                self.validateCase(reserved, i)
            elif word == "else":
                self.validateElse(reserved, i)
            elif word == "for":
                self.validateFor(line_num, end_index)
        s = ""
        for line_num in range(1, num_lines + 1):
            line_content = self.app.text_editor.get(f"{line_num}.0", f"{line_num}.end")
            operators = ["+", "-", "*", "/", ";", " "]
            words = [line_content]
            # Split the line_content for each operator and store the results in words
            for op in operators:
                temp = []
                for word in words:
                    temp.extend(word.split(op))
                words = temp
            # Filter out any empty strings
            words = [word for word in words if word]
            words = self.group_words(words)
            flag = 0
            s = ""
            if line_num in self.found_reserved:
                pass
            for word in words:
                f = 0
                for l, _, _, _ in self.found_reserved:
                    if line_num == l:
                        f = 1
                if word in self.identifiers:
                    s = ""
                elif word in self.reserved_words:
                    pass
                elif not (word in self.defined_variables):
                    self.errors.append(
                        f"Undeclared variable '{word}' used in line {line_num}"
                    )
                elif word in self.defined_variables and f == 0:
                    self.validate_semicolon(line_num)

    def validateFor(self, line_num, end_index):
        line_content = self.app.text_editor.get(f"{line_num}.0", f"{line_num}.end")
        s = ""
        f = 0
        ct = 0
        flag = 0
        temp = ""
        loop = ""
        condition = ""
        stringF = 0
        if line_content[end_index] == "(":
            end_index += 1
            loop += line_content[end_index + 1]
            for i in range(end_index, len(line_content)):
                for letter in line_content[i]:
                    loop += letter
                    temp = s
                    s += letter
                    if s.strip() in self.identifiers and f == 0:
                        f = 1
                        s = ""
                    elif f != 2 and s.strip() in self.defined_variables and ct == 0:
                        s = ""
                        f = 2
                    if ct == 1:
                        if letter == ";":
                            ct += 1
                            condition = s[:-1]
                            s = ""
                    elif ct == 2:
                        if not (letter.isalpha()):
                            if stringF == 0:
                                if not (s[:-1].strip() in self.defined_variables):
                                    self.errors.append(
                                        f"Undeclared variable in third part in line {line_num}."
                                    )
                            stringF = 1
                            if flag == 0:
                                flag = 1
                            elif flag == 1:
                                if len(s.strip()) < 4:
                                    continue
                                if (
                                    s[1:-1] != "++"
                                    and s[1:-1] != "--"
                                    and s[1:-1] != "+="
                                    and s[1:-1] != "-="
                                    and s[1:-1] != "*="
                                    and s[1:-1] != "/="
                                    and s != ""
                                ):
                                    print("Wrong: ", s[1:-1])
                                    self.errors.append(
                                        f"Wrong operators in third part in line {line_num}."
                                    )
                                flag = 2
                                if (
                                    s[1:-1] == "+="
                                    or s[1:-1] == "-="
                                    or s[1:-1] == "*="
                                    or s[1:-1] == "/="
                                ):
                                    flag = 3
                                s = ""
                            elif flag == 2 or flag == 3:
                                if (
                                    flag == 2
                                    and line_content[len(line_content) - 1] != ")"
                                ):
                                    self.errors.append(
                                        f"Missing closed brackets in third part in line {line_num}."
                                    )
                                flag = 4
                    if ct == 0:
                        if letter == ";" and f == 0:
                            ct += 1
                            self.errors.append(
                                f"Wrong for loop syntax in declaration in line {line_num}."
                            )
                        if letter == ";" and f == 1:
                            ct += 1
                            self.errors.append(
                                f"Missing variable in declaration in line {line_num}."
                            )
                        elif letter == ";" and f == 2:
                            ct += 1
                        s = ""
            self.loop_parts.append([line_num, loop])
        else:
            self.errors.append(f"There is a missing ( in Line {line_num}:")
        self.validateCondition(condition, line_num)

    def validate_semicolon(self, line_num):
        line_content = self.app.text_editor.get(f"{line_num}.0", f"{line_num}.end")
        if not line_content.endswith(";"):
            self.errors.append(f"Missing semicolon at the end of Line {line_num}")

    def checkWord(self, var):
        if var in self.defined_variables:
            return True
        else:
            return False

    def calculateIterator(self, reserved, lineIndex, numOfSteps):
        loopInc = -1
        if reserved == "for":
            for loopPart in self.loop_parts:
                if loopPart[0] == lineIndex:
                    loopPart[1] = loopPart[1][1:-1]
                    sections = loopPart[1].split(";")
                    section = sections[0].split(" ")
                    if section[0] not in self.identifiers:
                        var = section[0][0]
                        intialVal = section[0][-1:]
                    else:
                        var = section[1][0]
                        intialVal = section[1][-1:]
                    section = sections[1].split(" ")
                    limit = section[-1:]
                    if isinstance(limit, list):
                        limit = int(limit[0])
                    section = sections[2]
                    if section[-1:].isnumeric():
                        loopInc = section[-1:]
                        inc = section[-3:]
                        if inc[0] == "-":
                            loopInc *= -1
                    else:
                        if section[-2:] == "++":
                            loopInc = 1
                        elif section[-2:] == "--":
                            loopInc = -1
                    limit = int(limit)
                    loopInc = int(loopInc)
                    for x in range(0, limit, loopInc):
                        finalVal = x
                    finalVal += loopInc
                    numOfSteps = math.ceil(
                        (int(finalVal) - int(intialVal)) / int(loopInc)
                    )
                    self.values.append([var, intialVal, finalVal])
                    self.varValues[var].append(finalVal)
        else:
            for loopPart in self.loop_parts:
                if loopPart[0] == lineIndex:
                    loopPart[1] = loopPart[1]
                    finalVal = int(loopPart[1][-1:]) + 1
                    var = loopPart[1][1]
                    loopInc = 1
                    self.varValues[var].append(finalVal)
        return numOfSteps

    def updateVariabels(self, lineContent, numOfLoops):
        if lineContent == "{" or lineContent == "}":
            return
        LHS = True
        varLHS = ""
        before = -1
        var1 = None
        op = ""
        var2 = None
        s = ""
        if lineContent[-3:] == "++;":
            var = lineContent[:-3]
            if var[-1:] == "]":
                pass
            valVar = self.varValues[var][-1]
            for i in range(numOfLoops):
                valVar += 1
            self.varValues[var].append(valVar)
        elif lineContent[-3:] == "--;":
            var = lineContent[:-3]
            valVar = self.varValues[var][-1]
            for i in range(numOfLoops):
                valVar -= 1
            self.varValues[var].append(valVar)
        else:
            for index, letter in enumerate(lineContent):
                if s in ["+", "*", "/", "-", "="]:
                    s = ""
                if s in self.defined_variables and LHS:
                    varLHS = s
                    before = self.varValues[varLHS][-1]
                    if lineContent[index] == "+" and lineContent[index + 1] == "=":
                        num = lineContent[index + 2 : -1]
                        if num.isnumeric():
                            num = int(num)
                            for i in range(numOfLoops):
                                before += num
                            self.varValues[varLHS].append(before)
                            return
                    if lineContent[index] == "-" and lineContent[index + 1] == "=":
                        num = lineContent[index + 2 : -1]
                        if num.isnumeric():
                            num = int(num)
                            for i in range(numOfLoops):
                                before -= num
                            self.varValues[varLHS].append(before)
                            return
                    if lineContent[index] == "*" and lineContent[index + 1] == "=":
                        num = lineContent[index + 2 : -1]
                        if num.isnumeric():
                            num = int(num)
                            for i in range(numOfLoops):
                                before *= num
                            self.varValues[varLHS].append(before)
                            return
                    if lineContent[index] == "/" and lineContent[index + 1] == "=":
                        num = lineContent[index + 2 : -1]
                        if num.isnumeric():
                            num = int(num)
                            for i in range(numOfLoops):
                                before /= num
                            self.varValues[varLHS].append(before)
                            return
                    elif lineContent[index] == "=":
                        LHS = False
                    s = ""
                elif not LHS:
                    if letter == "+" or letter == "-" or letter == "*" or letter == "/":
                        if s.isnumeric():
                            var1 = int(s)
                        else:
                            var1 = self.varValues[s][-1]
                        s = ""
                        op = letter
                    if letter == ";":
                        if s.isnumeric():
                            var2 = int(s)
                        else:
                            var2 = self.varValues[s][-1]
                s += letter
            if var1 != None and var2 != None:
                for i in range(numOfLoops):
                    if op == "+":
                        before = var1 + var2
                    elif op == "-":
                        before = var1 - var2
                    elif op == "*":
                        before = var1 * var2
                    elif op == "/":
                        before = var1 // var2
                self.varValues[varLHS].append(before)

    def compileMemory(self):
        numOfLoops = -1
        num_lines = int(self.app.text_editor.index("end-1c").split(".")[0])
        for line_num in range(1, num_lines + 1):
            fReseved = False
            lineContent = self.app.text_editor.get(f"{line_num}.0", f"{line_num}.end")
            for reserved in self.found_reserved:
                if line_num == reserved[0] and (
                    reserved[1] == "for" or reserved[1] == "while"
                ):
                    fReseved = True
                    numOfLoops = self.calculateIterator(
                        reserved[1], reserved[0], numOfLoops
                    )
            if not fReseved:
                if line_num not in self.lineIdentify:
                    self.updateVariabels(lineContent, numOfLoops)


if __name__ == "__main__":
    root = tk.Tk()
    app = CompilerApp(root)
    scanner = Scanner(app)
    app.set_compile_command(scanner.scan)
    app.set_run_command(scanner.showError)
    root.mainloop()
