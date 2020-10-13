from lark import Lark

lark_grammer = r"""
start: (_item? _NL)* _item?

_item: rule
     | token
     | statement

rule: RULE rule_params priority? ":" expansions
token: TOKEN token_params priority? ":" expansions

rule_params: ["{" RULE ("," RULE)* "}"]
token_params: ["{" TOKEN ("," TOKEN)* "}"]

priority: "." NUMBER


statement: "%ignore" expansions                    -> ignore
         | "%import" import_path ["->" name]       -> import
         | "%import" import_path name_list         -> multi_import
         | "%declare" name+                        -> declare

!import_path: "."? name ("." name)*
name_list: "(" name ("," name)* ")"

?expansions: alias (_VBAR alias)*

?alias: expansion ["->" RULE]

?expansion: expr*

?expr: atom [OP | "~" NUMBER [".." NUMBER]]

?atom: "(" expansions ")"
     | "[" expansions "]" -> maybe
     | value

?value: STRING ".." STRING -> literal_range
      | name
      | (REGEXP | STRING) -> literal
      | name "{" value ("," value)* "}" -> template_usage

name: RULE
    | TOKEN

_VBAR: _NL? "|"
OP: /[+*]|[?](?![a-z])/
RULE: /!?[_?]?[a-z][_a-z0-9]*/
TOKEN: /_?[A-Z][_A-Z0-9]*/
STRING: _STRING "i"?
REGEXP: /\/(?!\/)(\\\/|\\\\|[^\/\n])*?\/[imslux]*/
_NL: /(\r?\n)+\s*/

ARROW : "->"
IGNORE_STATEMENT : "%ignore"
IMPORT_STATEMENT : "%import"
DECLARE_STATEMENT : "%declare"


%import common.ESCAPED_STRING -> _STRING
%import common.SIGNED_INT -> NUMBER
%import common.WS_INLINE

COMMENT: /\s*/ "//" /[^\n]/*

%ignore WS_INLINE
%ignore COMMENT
"""

lark_grammar_parser = Lark(lark_grammer, parser="lalr")
