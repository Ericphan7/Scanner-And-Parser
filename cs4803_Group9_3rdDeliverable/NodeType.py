

from enum import Enum


class NodeType(Enum):

	PROGRAM = "<program>"
	IMPORT = "<import_stmnt>"
	SYMBOL = "<symbol_stmnt>"
	GLOBALS = "<globals>"
	IMPLEMENT = "<implement>"
	CONST_DEC = "<const_dec>"
	CONST_LIST = "<const_list>"
	VAR_DEC = "<var_dec>"
	VAR_LIST = "<var_list>"
	COMP_DECLARE = "<comp_declare>"
	RET_TYPE = "<ret_type>"
	FUNCT_LIST = "<funct_list>"
	FUNCT_BODY = "<funct_body>"
	PACTIONS = "<pactions>"
	ACTION_DEF = "<action_def>"
	EXP = "<exp>"
	PVAR_VALUE_LIST = "<p_var_value_list>"