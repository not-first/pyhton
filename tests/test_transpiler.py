from src.transpiler import PyhtonTranspiler


def test_transpiler_all_typo_types():
    transpiler = PyhtonTranspiler()

    pyhton_code = """deff test_function():
    doubled_var = "test"
    missing_var = "test"
    swapped_var = "test"
    prrint(f"Testing: {doubled_var}, {missing_var}, {swapped_var}")
    retrn Treu"""

    result = transpiler.transpile_code(pyhton_code)

    expected = """def test_function():
    doubled_var = "test"
    missing_var = "test"
    swapped_var = "test"
    print(f"Testing: {doubled_var}, {missing_var}, {swapped_var}")
    return True"""

    assert result == expected


def test_transpiler_custom_variables():
    transpiler = PyhtonTranspiler()

    pyhton_code = """my_variable = 5
custom_name = "test"
prrint(my_variable)"""

    result = transpiler.transpile_code(pyhton_code)

    expected = """my_variable = 5
custom_name = "test"
print(my_variable)"""

    assert result == expected


def test_transpiler_user_defined_names():
    transpiler = PyhtonTranspiler()

    pyhton_code = """deff prrint():
    deff = "this is a variable named deff"
    prrint(deff)"""

    result = transpiler.transpile_code(pyhton_code)

    expected = """def prrint():
    deff = "this is a variable named deff"
    print(deff)"""

    assert result == expected
