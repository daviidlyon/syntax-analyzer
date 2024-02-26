import sys

from constants import GRAMMAR
from lexer import lexical

## FIRST
def get_productions_first_set(grammar, productions):
    prod_first_set = set()
    if productions == ["eps"]:
        prod_first_set.add("eps")
        return prod_first_set

    if productions[0] not in grammar:
        prod_first_set.add(productions[0])
        return prod_first_set

    first_a1 = get_rule_first_set(grammar, grammar[productions[0]])
    if "eps" in first_a1:
        if len(productions) > 1:
            first_a1.discard("eps")
            first_a2_an = get_productions_first_set(grammar, productions[1:])
            prod_first_set.update(first_a1)
            prod_first_set.update(first_a2_an)
            return prod_first_set
    return first_a1


def get_rule_first_set(grammar, rule):
    rule_first_set = set()
    for subrule in rule:
        prod_first_set = get_productions_first_set(grammar, subrule)
        rule_first_set.update(prod_first_set)
    return rule_first_set


def get_grammar_first(grammar):
    grammar_first = {}
    for rule in grammar:
        grammar_first[rule] = get_rule_first_set(grammar, grammar[rule])
    return grammar_first


## NEXT
def get_last_occurence_index(item, li):
    return len(li) - 1 - li[::-1].index(item)


def get_grammar_rule_occurrences(grammar):
    # Check for appearences in the grammar
    def search_in_grammar(key):
        matches = []
        for rule, productions in grammar.items():
            for production in productions:
                if key in production:
                    matches.append((rule, production))
        return matches

    grammar_rule_occurrences = {}
    # For every key fetch for appearences in all grammar
    for rule_key in grammar:
        grammar_rule_occurrences[rule_key] = search_in_grammar(rule_key)
    return grammar_rule_occurrences


def get_grammar_next_set(grammar, initial_rule_key):
    grammar_first = get_grammar_first(grammar)
    grammar_rule_occurrence = get_grammar_rule_occurrences(grammar)

    calculated_next = {}

    def get_next_set(rule_key):
        # If it already exists, then return it
        if rule_key in calculated_next:
            return calculated_next[rule_key]

        # Get places where it appears
        rule_occurrences = grammar_rule_occurrence[rule_key]

        # Create a new set
        next_set = set()

        # If it is the initial key, then add $
        if rule_key == initial_rule_key:
            next_set.add("$")

        # Now go for each occurrence
        for occ_key, occ_production in rule_occurrences:
            key_index = get_last_occurence_index(rule_key, occ_production)
            if key_index + 1 == len(occ_production):  # Is the last one
                if occ_key != rule_key:
                    s_A = get_next_set(occ_key)
                    next_set.update(s_A)
            else:
                beta = occ_production[key_index + 1]
                if beta not in grammar:
                    next_set.add(beta)
                else:
                    f_beta = grammar_first[beta]
                    if "eps" in f_beta:
                        f_beta.discard("eps")
                        next_set.update(f_beta)
                        s_A = get_next_set(occ_key) if occ_key != rule_key else set()
                        next_set.update(s_A)
                    else:
                        next_set.update(f_beta)

        # At the end, return the set obviously,
        # But first, add it to the calculated ones
        calculated_next[rule_key] = next_set
        return next_set

    grammar_next = {}
    for key in grammar:
        key_next_set = get_next_set(key)
        grammar_next[key] = key_next_set

    return grammar_next


## PREDICTION SET


def get_grammar_pred_set(grammar, initial_rule_key):
    grammar_next = get_grammar_next_set(grammar, initial_rule_key)

    def get_pred_set(A, a):
        pred_set = set()
        f_a = get_productions_first_set(grammar, a)
        if "eps" in f_a:
            f_a.discard("eps")
            pred_set.update(f_a)

            s_A = grammar_next[A]
            pred_set.update(s_A)
        else:
            pred_set.update(f_a)
        return pred_set

    pred_set_dict = {}
    for rule, productions in grammar.items():
        pred_set_dict[rule] = []
        for prod in productions:
            pred_set = get_pred_set(rule, prod)
            pred_set_dict[rule].append(pred_set)
    return pred_set_dict


## PARSER
def format_expected(expected_tokens):
    formatted_tokens = []
    for token in expected_tokens:
        if token == "id":
            formatted_tokens.append("Identifier")
        elif token == "num":
            formatted_tokens.append("Number")
        elif token == "str":
            formatted_tokens.append("Text")
        elif token == "True":
            formatted_tokens.append("True")
        elif token == "False":
            formatted_tokens.append("False")
        elif token == "$":
            formatted_tokens.append("EOF")
        else:
            formatted_tokens.append(token)
    formatted_tokens.sort()
    return formatted_tokens


def parse(user_input, grammar, initial_symbol):
    def raise_error(row, column, found, expected_tokens):
        formatted = format_expected(expected_tokens)
        expected = ", ".join(f"'{token}'" for token in formatted)
        if found.token == "$":
            print(f"[{row}:{column}] Syntax Error: EOF found, expected: {expected}.")
        else:
            print(
                f"[{row}:{column}] Syntax Error: Found: '{found.lex}'; expected: {expected}."
            )

    tokens = lexical(user_input)
    grammar_pred_sets = get_grammar_pred_set(grammar, initial_symbol)

    derivation = [initial_symbol]
    syntactic_error = False
    while len(derivation) > 0:
        a1 = derivation.pop(0)
        current_token = tokens[0]
        if a1 not in grammar:  # Not in grammar, pair...
            if a1 == "eps":
                if current_token.token == "$" and len(derivation) == 0:
                    tokens.pop(0)
                continue
            else:
                terminalMatch = current_token.token == a1
                if terminalMatch:
                    tokens.pop(0)
                else:
                    syntactic_error = True
                    raise_error(
                        current_token.row, current_token.column, current_token, [a1]
                    )
                    break
        else:  # It is a non-terminal, lets derivate...
            rule_pred_sets = grammar_pred_sets[a1]
            for index, pred_set in enumerate(rule_pred_sets):
                matched = False
                if (
                    current_token.token in pred_set
                ):  # With the selected one, then replace
                    matched = True
                    for prod in reversed(grammar[a1][index]):
                        derivation.insert(0, prod)
                    break

            if not matched:
                syntactic_error = True
                f_a1 = get_productions_first_set(grammar, [a1])
                f_a2n = {}
                if len(derivation) > 0:
                    f_a2n = get_productions_first_set(grammar, [*derivation])
                combined_preds = set().union(*rule_pred_sets)
                expected = set()
                if "eps" in f_a1:
                    if "$" in combined_preds:
                        next_is_terminal = False
                        for derivation_i in derivation:
                            if derivation_i not in grammar:
                                next_is_terminal = True
                                break
                        if not next_is_terminal:
                            expected.add("$")
                    expected.update(f_a1)
                    expected.update(f_a2n)
                    expected.discard("eps")
                else:
                    expected = combined_preds
                the_expected = list(expected)
                raise_error(
                    current_token.row, current_token.column, current_token, the_expected
                )
                break

    if not syntactic_error:
        print("Syntax analysis finished succesfully.")


test_code = sys.stdin.read()

parse(test_code, GRAMMAR, "P")
