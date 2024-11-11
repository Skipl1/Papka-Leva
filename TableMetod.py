

class SimplexTable:
    # Определяем очень большое значение для представления бесконечности
    infty = 10**8

    def __init__(self, max_min_bool, list_x, target_function_variables, list_ogran, matrix_table, marks, right_hand_side_values):
        """
        Инициализация класса:
        - max_min_bool: флаг для максимизации (True) или минимизации (False)
        - list_x: количество переменных
        - target_function_variables: коэффициенты целевой функции
        - list_ogran: количество ограничений
        - matrix_table: матрица коэффициентов ограничений
        - marks: знаки ограничений (True - >=, False - <=)
        - right_hand_side_values: значения правой части ограничений
        """
        self.max_min_bool = max_min_bool
        self.list_x = list_x
        self.target_function_variables = target_function_variables
        self.list_ogran = list_ogran
        self.matrix_table = matrix_table
        self.marks = [True if mark else False for mark in marks]
        self.right_hand_side_values = right_hand_side_values
        # Количество искусственных переменных, которые понадобятся для ограничений с ">="
        self.limitation_calculation = sum(1 for mark in self.marks if not mark)

    @staticmethod
    def line_output(value):
        """
        Форматирование значений для отображения (три знака после запятой).
        """
        if isinstance(value, (int, float)):
            return f"{value:.3f}"
        return str(value)

    @staticmethod
    def line_output_2(value, max_negative=None, min_teta=None, max_min_bool=None):
        """
        Специальное форматирование для отображения значений, отмечая минимальные и максимальные значения.
        """
        if isinstance(value, (int, float)):
            if min_teta is not None and value == min_teta:
                return f"{value:.3f} (MIN)"
            if max_negative is not None and value == max_negative:
                # Добавляем вывод "MAX" или "MIN" в зависимости от задачи на максимизацию или минимизацию
                if max_min_bool:
                    return f"{value:.3f} (MIN)"
                else:
                    return f"{value:.3f} (MAX)"
            elif value <= -10000000:
                return "-"
            elif value >= 10000000:
                return "+"
            return f"{value:.3f}"
        return str(value)

    @staticmethod
    def scalar_product(list1, list2):
        """
        Вычисление скалярного произведения двух списков.
        """
        return sum(x * y for x, y in zip(list1, list2))

    def basic_solution(self):
        """
        Метод для нахождения базового решения и начальной инициализации таблицы.
        """
        # Размер задачи — количество переменных и ограничений
        self.size = self.list_x + self.list_ogran

        # Добавление единичной матрицы для учета знаков ограничений
        for i in range(self.list_ogran):
            for j in range(self.list_ogran):
                if i == j:
                    self.matrix_table[i].append(1 if self.marks[i] else -1)
                else:
                    self.matrix_table[i].append(0)

        # Добавление нулевых столбцов для искусственных переменных
        for i in range(self.list_ogran):
            self.matrix_table[i].extend([0] * self.limitation_calculation)
        
        # Индекс для отслеживания искусственных переменных
        dop_peremen = 0
        for i in range(len(self.marks)):
            if not self.marks[i]:
                self.matrix_table[i][self.list_ogran + self.list_x + dop_peremen] = 1
                dop_peremen += 1

        # Расширяем целевую функцию, чтобы учесть базисные и искусственные переменные
        self.size += self.limitation_calculation
        self.target_function_variables = [0] + self.target_function_variables + [0] * self.list_ogran
        self.target_function_variables += [-self.infty] * self.limitation_calculation if self.max_min_bool else [self.infty] * self.limitation_calculation

        # Определение начального базиса
        self.elementary_basis = [
            j + 1 for i in range(self.list_ogran)
            for j in range(self.list_x, self.size)
            if self.matrix_table[i][j] == 1
        ]

        # Вычисление начальных значений дельта и тета
        self.delt = self.delta_calculation()
        self.teta = self.teta_calculation()
        self.number = 0
        self.initial_table()
        self.table_output()

        # Итерационный процесс поиска решения
        while True:
            # Вычисление значений таблицы для новой итерации
            self.matrix_table = self.tabular_value_calculation()
            self.delt = self.delta_calculation()

            # Проверка на завершение процесса для задачи максимизации
            if self.max_min_bool:
                is_non_negative = True
                for x in self.delt[:self.size - self.limitation_calculation]:
                    if x < 0:
                        is_non_negative = False
                        break
                if is_non_negative:
                    self.final_table()
                    break
            # Проверка на завершение процесса для задачи минимизации
            else:
                is_non_positive = True
                for x in self.delt[:self.size - self.limitation_calculation]:
                    if x > 0:
                        is_non_positive = False
                        break
                if is_non_positive:
                    self.final_table()
                    break

            # Вычисление значений тета и вывод таблицы
            self.teta = self.teta_calculation()
            self.table_output()
            # Проверка, можно ли получить решение
            Verification_of_task_fulfilment = any(self.matrix_table[i][self.minimal_delta] >= 0 for i in range(self.list_ogran))
            if not Verification_of_task_fulfilment:
                print("\nРешение: У данной задачи нет допустимого решения")
                break
        # Проверка на наличие искусственных переменных в базисе
        if any(basis_var > self.list_x + self.list_ogran for basis_var in self.elementary_basis):
            print("\nРешение: У данной задачи нет допустимого решения, так как в оптимальном решении присутствуют искусственные переменные.\n")
            return

        if any(self.matrix_table[i][self.minimal_delta] >= 0 for i in range(self.list_ogran)):
            current_solution = [0] * self.size
            for i in range(self.list_ogran):
                current_solution[self.elementary_basis[i] - 1] = self.right_hand_side_values[i]
            formatted_answer = [self.line_output(x) for x in current_solution]
            print("Найденное решение:")
            print(f"F = {self.line_output(self.current_solution)}")
            print(f"Полученный вектор: ({' '.join(formatted_answer)})\n")

    def tabular_value_calculation(self):
        # Создаем копии текущей таблицы и правых частей ограничений
        matrix_table = [row[:] for row in self.matrix_table]
        new_table = [row[:] for row in self.matrix_table]
        right_hand_coppy = self.right_hand_side_values[:]
        
        # Обновляем базис: заменяем переменную в базисе на выбранную для входа в базис
        self.elementary_basis[self.minimal_teta] = self.minimal_delta + 1

        # Пересчитываем значения правых частей ограничений
        for i in range(self.list_ogran):
            if i == self.minimal_teta:
                # Делим правую часть минимального тета на элемент в разрешающем столбце
                right_hand_coppy[i] = self.right_hand_side_values[self.minimal_teta] / matrix_table[self.minimal_teta][self.minimal_delta]
            else:
                # Корректируем правые части для остальных строк
                right_hand_coppy[i] = self.right_hand_side_values[i] - (
                    self.right_hand_side_values[self.minimal_teta] * matrix_table[i][self.minimal_delta]
                ) / matrix_table[self.minimal_teta][self.minimal_delta]

        # Обновляем правую часть ограничений
        self.right_hand_side_values = right_hand_coppy

        # Обновляем значения таблицы по новым данным, основанным на разрешающем элементе
        for i in range(self.list_ogran):
            for j in range(self.size):
                if i == self.minimal_teta:
                    # Делим элементы разрешающей строки на разрешающий элемент
                    new_table[i][j] = matrix_table[self.minimal_teta][j] / matrix_table[self.minimal_teta][self.minimal_delta]
                else:
                    # Корректируем все остальные элементы таблицы
                    new_table[i][j] = matrix_table[i][j] - (
                        (matrix_table[self.minimal_teta][j] * matrix_table[i][self.minimal_delta]) / matrix_table[self.minimal_teta][self.minimal_delta]
                    )

        # Возвращаем обновленную таблицу для следующей итерации
        return new_table


    def teta_calculation(self):
        # Определяем индекс минимального дельта для максимизации или максимального дельта для минимизации
        if self.max_min_bool:
            # Для максимизации ищем минимальное значение среди отрицательных дельта
            negative_values = [x for x in self.delt if x < 0]
            min_negative_value = min(negative_values)
            self.minimal_delta = self.delt.index(min_negative_value)
        else:
            # Для минимизации ищем максимальное значение среди положительных дельта
            positive_values = [x for x in self.delt if x > 0]
            max_positive_value = max(positive_values)
            self.minimal_delta = self.delt.index(max_positive_value)

        # Создаем вектор направлений для текущего разрешающего столбца
        direct_vector = [self.matrix_table[i][self.minimal_delta] for i in range(self.list_ogran)]
        teta = []
        
        # Рассчитываем тета для каждой строки
        for i in range(self.list_ogran):
            if direct_vector[i] == 0:
                # Если значение в направляющем векторе равно 0, то тета бесконечно
                teta.append(self.infty)
            else:
                # Вычисляем тета как отношение правой части к элементу в направляющем векторе
                cal = self.right_hand_side_values[i] / direct_vector[i]
                # Добавляем значение в список тета, если оно положительное, иначе — бесконечность
                teta.append(cal if cal > 0 else self.infty)

        # Определяем минимальное значение тета и сохраняем его индекс как разрешающую строку
        self.minimal_teta = teta.index(min(teta))
        return teta

    def delta_calculation(self):
        # Находим значения коэффициентов целевой функции для базисных переменных
        targeted_basis = [self.target_function_variables[i] for i in self.elementary_basis]

        # Рассчитываем текущее значение целевой функции
        self.current_solution = self.scalar_product(targeted_basis, self.right_hand_side_values) - self.target_function_variables[0]

        # Вычисляем значения дельта для каждого столбца
        delt = []
        for i in range(self.size):
            # Формируем столбец из матрицы коэффициентов ограничений
            column = [self.matrix_table[j][i] for j in range(self.list_ogran)]
            # Вычисляем дельта для столбца как разность скалярного произведения и коэффициента целевой функции
            delt.append(self.scalar_product(column, targeted_basis) - self.target_function_variables[i + 1])

        # Возвращаем массив значений дельта для проверки условий оптимальности
        return delt
                
    def initial_table(self):
        print(f'\nТаблица с искусственными переменными (итерация: {self.number}):')
        headers = ["Cj"," "] + [self.line_output(elem) for elem in self.target_function_variables] + [" "]
        bx_row = ["", "Bx"] + [f"A{i}" for i in range(0, self.size + 1)] + ["teta"]
        rows = []
        min_teta_value = min(self.teta)
        # Определяем наибольшее отрицательное значение в deltах
        if (self.max_min_bool):
            max_negative_delta = min([d for d in self.delt if d < 0])
        else:
            max_negative_delta = max([d for d in self.delt if d > 0])
        
        for i in range(self.list_ogran):
            row = [
                self.line_output(self.target_function_variables[self.elementary_basis[i]]),
                f"x{int(self.elementary_basis[i])}",
                self.line_output(self.right_hand_side_values[i])
            ] + [self.line_output(elem) for elem in self.matrix_table[i]]
            teta = self.line_output_2(self.teta[i], None, min_teta_value, self.max_min_bool)
            row.append("besk" if teta == str(self.infty) else teta)
            rows.append(row)
        delta_row = [" ", "Δ(J)", self.line_output_2(self.current_solution, max_negative_delta, None, self.max_min_bool)] + [self.line_output_2(d, max_negative_delta, None, self.max_min_bool) for d in self.delt] + [" "]
        rows.append(delta_row)
        print(tabulate([bx_row] + rows, headers=headers, tablefmt="fancy_grid", stralign="center", numalign="center"))
        print(f"Вводим A{self.minimal_delta + 1}, Выводим A{self.elementary_basis[self.minimal_teta]}")
    
    # Изменение функции `table_output` для передачи наибольшего отрицательного значения
    def table_output(self):
        if self.number >= 1:
            print(f'\nНомер итерации: {self.number}')
        headers = ["Cj"," "] + [self.line_output(elem) for elem in self.target_function_variables] + [" "]
        bx_row = ["", "Bx"] + [f"A{i}" for i in range(0, self.size + 1)] + ["teta"]
        rows = []
        min_teta_value = min(self.teta)
        # Определяем наибольшее отрицательное значение в deltах
        if (self.max_min_bool):
            max_negative_delta = min([d for d in self.delt if d < 0])
        else:
            max_negative_delta = max([d for d in self.delt if d > 0])
        
        for i in range(self.list_ogran):
            row = [
                self.line_output(self.target_function_variables[self.elementary_basis[i]]),
                f"x{int(self.elementary_basis[i])}",
                self.line_output(self.right_hand_side_values[i])
            ] + [self.line_output(elem) for elem in self.matrix_table[i]]
            if self.number >= 1:
                teta = self.line_output_2(self.teta[i], None, min_teta_value, self.max_min_bool)
                row.append("besk" if teta == str(self.infty) else teta)
            rows.append(row)
        if self.number >= 1:
            delta_row = [" ", "Δ(J)", self.line_output_2(self.current_solution, max_negative_delta, None, self.max_min_bool)] + [self.line_output_2(d, max_negative_delta, None, self.max_min_bool) for d in self.delt] + [" "]
            rows.append(delta_row)
            print(tabulate([bx_row] + rows, headers=headers, tablefmt="fancy_grid", stralign="center", numalign="center"))
            print(f"Вводим A{self.minimal_delta + 1}, Выводим A{self.elementary_basis[self.minimal_teta]}")
        self.number += 1
    
    # Изменение функции `final_table` для передачи наибольшего отрицательного значения
    def final_table(self):
        print(f'\nФинальная таблица (итерация: {self.number}):')
        headers = ["Cj"," "] + [self.line_output(elem) for elem in self.target_function_variables] + [" "]
        bx_row = ["", "Bx"] + [f"A{i}" for i in range(0, self.size + 1)] + ["teta"]
        rows = []
        
        for i in range(self.list_ogran):
            row = [
                self.line_output(self.target_function_variables[self.elementary_basis[i]]),
                f"x{int(self.elementary_basis[i])}",
                self.line_output(self.right_hand_side_values[i])
            ] + [self.line_output(elem) for elem in self.matrix_table[i]]
            teta = self.line_output_2(self.teta[i])
            row.append("besk" if teta == str(self.infty) else teta)
            rows.append(row)
        delta_row = [" ", "Δ(J)", self.line_output_2(self.current_solution)] + [self.line_output_2(d) for d in self.delt] + [" "]
        rows.append(delta_row)
        print(tabulate([bx_row] + rows, headers=headers, tablefmt="fancy_grid", stralign="center", numalign="center"))

