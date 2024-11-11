from TableMetod import SimplexTable

def main():
    print("Добро пожаловать в программу решения задач линейного программирования методом симплекс-таблицы.")
    
    # Запрашиваем количество переменных и ограничений
    while True:
        try:
            list_x = int(input("Введите количество видов продукции: "))
            list_ogran = int(input("Введите количество ограничений: "))
            break
        except ValueError:
            print("Пожалуйста, введите целое число.")
    
    matrix = []
    marks = []
    right_hand_side_values = []
    print("\nВведите ограничения в формате: 'a1 a2 ... an <= b'")
    for i in range(list_ogran):
        while True:
            try:
                parts = input(f"Ограничение {i + 1}: ").split()
                constraint = [float(part) for part in parts[:-2]]
                if len(constraint) != list_x:
                    print(f"Ошибка: должно быть {list_x} коэффициентов.")
                    continue
                matrix.append(constraint)
                marks.append(parts[-2] == "<=")
                right_hand_side_values.append(float(parts[-1]))
                break
            except ValueError:
                print("Некорректный ввод. Попробуйте снова.")
    while True:
        try:
            target_function_variables = list(map(float, input("\nВведите коэффициенты целевой функции: ").split()))
            if len(target_function_variables) != list_x:
                print(f"Ошибка: должно быть {list_x} коэффициентов.")
                continue
            break
        except ValueError:
            print("Некорректный ввод. Попробуйте снова.")
    while True:
        max_min_vibor = input("Введите задачу (max/min): ").strip().lower()
        if max_min_vibor in ["max", "min"]:
            max_min_bool = (max_min_vibor == "max")
            break
        else:
            print("Ошибка: введите 'max' для максимизации или 'min' для минимизации.")
    table_method_instance = SimplexTable(
        max_min_bool=max_min_bool,
        list_x=list_x,
        target_function_variables=target_function_variables,
        list_ogran=list_ogran,
        matrix_table=matrix,
        marks=marks,
        right_hand_side_values=right_hand_side_values
    )
    
    table_method_instance.basic_solution()

if __name__ == "__main__":
    main()
