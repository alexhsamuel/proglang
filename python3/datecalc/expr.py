import datetime
import re

from   . import parse_date

#-------------------------------------------------------------------------------

def tokenize(expr):
    expr = expr.strip()

    while len(expr) > 0:
        expr = expr.lstrip()

        for token in ("today", "<<", ">>", "-", "...", "..", ):
            if expr.startswith(token):
                yield token, token
                expr = expr[len(token) :]
                break
            
        else:
            match = re.match(r"\d{4}-\d{2}-\d{2}", expr)
            if match is not None:
                yield "date", match.group(0)
                expr = expr[match.end() :]
                continue

            match = re.match(r"[-+]?\d+", expr)
            if match is not None:
                yield "offset", match.group(0)
                expr = expr[match.end() :]
                continue

            raise RuntimeError("can't tokenize: from {!r}".format(expr))



#-------------------------------------------------------------------------------

def evaluate_date(tokens, context):
    token, text = tokens.pop(0)
    if token == "date":
        return evaluate_date(text)
    elif token == "today":
        return context["today"]
    else:
        raise RuntimeError("unepected token: {}".format(text))


def evaluate_date_expr(tokens, context):
    date = evaluate_date(tokens, context)
    if len(tokens) > 0 and tokens[0][0] in ("<<", ">>"):
        token, _ = tokens.pop(0)
        date = context["calendar"].to(date, token == ">>")
        if tokens[0][0] == "offset":
            _, offset = tokens.pop(0)
            offset = int(offset)
            offset = offset if token == ">>" else -offset
            return context["calendar"].add(date, offset)
        else:
            raise RuntimeError("unexpected token: {}".format(text))
    else:
        return date


def evaluate_date_diff(tokens, context):
    date0 = evaluate_date_expr(tokens, context)
    token, text = tokens.pop(0)
    if token != "-":
        raise RuntimeError("unexpected token: {}".format(text))
    date1 = evaluate_date_expr(tokens, context)
    
    return date_diff(context["calendar"], date0, date1)


def evaluate_date_range(tokens, context):
    date0 = evaluate_date_expr(tokens, context)
    token, text = tokens.pop(0)
    if token == "..":
        inclusive = False
    elif token == "...":
        inclusive = True
    else:
        raise RuntimeError("unexpected token: {}".format(text))
    date1 = evaluate_date_expr(tokens, context)

    return date_range(context["calendar"], date0, date1, inclusive)


def evaluate_expr(tokens, context):
    if any( t in ("..", "...") for t, _ in tokens ):
        return evaluate_date_range(tokens, context)
    elif any( t == "-" for t, _ in tokens ):
        return evaluate_date_diff(tokens, context)
    else:
        return evaluate_date_expr(tokens, context)


def evaluate(expr, calendar):
    context = dict(calendar=calendar, today=datetime.date.today())
    tokens = list(tokenize(expr))
    return evaluate_expr(tokens, context)


