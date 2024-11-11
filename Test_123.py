# tester.py
from TableMetod import SimplexTable

def get_test_case(case_number):
    match case_number:
        case 1:
            is_max = True
            coefficients = [14, 18]
            sz_aim = len(coefficients)
            sz_coeffs = 3
            table = [[10, 8], [5, 10], [6, 12]]
            signs = [True, True, True]
            free_members = [168, 180, 144]
            return is_max, sz_aim, coefficients, sz_coeffs, table, signs, free_members
        case 2:
            is_max = True
            coefficients = [3, 2]
            sz_aim = len(coefficients)
            sz_coeffs = 3
            table = [[1, 2], [2, -1], [1, 3]]
            signs = [True, False, False]
            free_members = [12, 7, 14]
            return is_max, sz_aim, coefficients, sz_coeffs, table, signs, free_members
        case 3:
            is_max = False
            coefficients = [4, 1]
            sz_aim = len(coefficients)
            sz_coeffs = 3
            table = [[1, 2], [2, -1], [1, 3]]
            signs = [False, False, True]
            free_members = [12, 12, 14]
            return is_max, sz_aim, coefficients, sz_coeffs, table, signs, free_members
        case 4:
            is_max = False
            coefficients = [4, 3, 6]
            sz_aim = len(coefficients)
            sz_coeffs = 2
            table = [[3, -4, 2], [5, 2, 3]]
            signs = [False, False]
            free_members = [11, 16]
            return is_max, sz_aim, coefficients, sz_coeffs, table, signs, free_members
        case 5:
            is_max = True
            coefficients = [1, 10, 100, 1000, 10000]
            sz_aim = len(coefficients)
            sz_coeffs = 5
            table = [[1, 2, 3, 4, 5], [5, 6, 7, 8, 9], [9, 10, 11, 12, 13], [13, 14, 15, 16, 17], [17, 18, 19, 20, 21]]
            signs = [True, True, True, True, True]
            free_members = [2, 4, 8, 16, 32]
            return is_max, sz_aim, coefficients, sz_coeffs, table, signs, free_members
        case 6:
            is_max = False
            coefficients = [1, 10, 100, 1000, 10000]
            sz_aim = len(coefficients)
            sz_coeffs = 5
            table = [[1, 2, 3, 4, 5], [5, 6, 7, 8, 9], [9, 10, 11, 12, 13], [13, 14, 15, 16, 17], [17, 18, 19, 20, 21]]
            signs = [True, True, False, False, True]
            free_members = [2, 4, 8, 16, 32]
            return is_max, sz_aim, coefficients, sz_coeffs, table, signs, free_members
            

def run_test(case_number):
    is_max, sz_aim, coefficients, sz_coeffs, table, signs, free_members = get_test_case(case_number)
    table_method_instance = SimplexTable(
        max_min_bool=is_max,
        list_x=sz_aim,
        target_function_variables=coefficients,
        list_ogran=sz_coeffs,
        matrix_table=table,
        marks=signs,
        right_hand_side_values=free_members
    )

    print(f"\nRunning Test Case {case_number}:")
    table_method_instance.basic_solution()

if __name__ == "__main__":
    print("Testing SimplexTable with predefined cases.\n")
    i = int(input())
    run_test(i)
