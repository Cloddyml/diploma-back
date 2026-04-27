"""seed_learning_data

Revision ID: 2a26ded24831
Revises: 97296b82bf04
Create Date: 2026-04-27 07:54:20.999491

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "2a26ded24831"
down_revision: Union[str, Sequence[str], None] = "97296b82bf04"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# ─────────────────────────────────────────────────────────────
#  АЛГОРИТМЫ СОРТИРОВКИ (учебная тема)
# ─────────────────────────────────────────────────────────────
SORTING_LEARN_CONTENT = r"""# Алгоритмы сортировки

Сортировка — одна из базовых тем в программировании. Понимание того, как работают разные алгоритмы сортировки, помогает писать эффективный код и хорошо объяснять решения на собеседованиях.

## Зачем изучать сортировку?

В Python есть встроенная функция `sorted()` и метод `.sort()`, которые используют алгоритм Timsort. Они быстрее любой самостоятельной реализации. Но знание базовых алгоритмов развивает понимание сложности, рекурсии и структур данных.

## Сортировка пузырьком (Bubble Sort)

Простейший алгоритм. На каждом проходе сравниваем соседние элементы и меняем их местами, если они стоят не по порядку. Самый большой элемент «всплывает» в конец.

```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        # После i-го прохода последние i элементов уже на месте
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr
```

**Сложность:** O(n²) — медленная, зато понятная.

## Сортировка выбором (Selection Sort)

На каждом шаге находим минимальный элемент в оставшейся части и ставим его на нужное место.

```python
def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr
```

**Сложность:** O(n²) — всегда одинакова, независимо от входных данных.

## Сортировка вставками (Insertion Sort)

Работает как раскладывание карт: берём следующий элемент и вставляем его в нужное место среди уже отсортированных.

```python
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr
```

**Сложность:** O(n²) в худшем случае, но O(n) для почти отсортированных данных.

## Сортировка слиянием (Merge Sort)

Делим массив пополам, рекурсивно сортируем каждую половину, потом сливаем два отсортированных массива.

```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[: mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    return result + left[i:] + right[j:]
```

**Сложность:** O(n log n) всегда. Требует дополнительную память O(n).

## Когда что использовать

- **Bubble/Selection/Insertion** — для обучения, для маленьких массивов (< 20 элементов)
- **Merge sort** — когда важна стабильная сортировка и гарантированное O(n log n)
- **Quick sort** — на практике часто быстрее merge sort, хотя в худшем случае O(n²)
- **sorted() в Python** — в реальном коде всегда используй встроенное
"""

SORTING_LEARN_TASK1_DESC = r"""Напишите функцию `solution(arr)`, которая реализует **сортировку пузырьком** и возвращает отсортированный по возрастанию список.

Не используй `sorted()` или `.sort()`.

### Пример

```python
solution([64, 34, 25, 12, 22, 11, 90])  # → [11, 12, 22, 25, 34, 64, 90]
solution([5, 1, 4, 2, 8])               # → [1, 2, 4, 5, 8]
solution([1])                            # → [1]
```
"""

SORTING_LEARN_TASK1_STARTER = """\
def solution(arr):
    # Напиши своё решение здесь
    # Подсказка: сравнивай соседние элементы arr[j] и arr[j+1]
    # и меняй их местами, если arr[j] > arr[j+1]
    pass
"""

SORTING_LEARN_TASK1_SOLUTION = """\
def solution(arr):
    arr = list(arr)
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr
"""

SORTING_LEARN_TASK2_DESC = r"""Напишите функцию `solution(arr)`, которая реализует **сортировку выбором** (Selection Sort) и возвращает отсортированный список.

Алгоритм: на каждом шаге находим индекс минимального элемента в неотсортированной части и ставим его на нужное место.

Не используй `sorted()` или `.sort()`.

### Пример

```python
solution([64, 25, 12, 22, 11])  # → [11, 12, 22, 25, 64]
solution([3, 2, 1])             # → [1, 2, 3]
```
"""

SORTING_LEARN_TASK2_STARTER = """\
def solution(arr):
    # Напиши своё решение здесь
    # Подсказка: для каждой позиции i найди индекс минимума
    # в arr[i:] и поменяй arr[i] с этим минимумом
    pass
"""

SORTING_LEARN_TASK2_SOLUTION = """\
def solution(arr):
    arr = list(arr)
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr
"""

SORTING_LEARN_TASK3_DESC = r"""Напишите функцию `solution(arr)`, которая реализует **сортировку вставками** (Insertion Sort) и возвращает отсортированный список.

Алгоритм: берём элемент с позиции i и «вставляем» его на правильное место среди уже отсортированных элементов слева.

Не используй `sorted()` или `.sort()`.

### Пример

```python
solution([12, 11, 13, 5, 6])  # → [5, 6, 11, 12, 13]
solution([4, 3, 2, 1])        # → [1, 2, 3, 4]
```
"""

SORTING_LEARN_TASK3_STARTER = """\
def solution(arr):
    # Напиши своё решение здесь
    # Подсказка: для каждого i, сохрани arr[i] в key,
    # сдвигай элементы вправо пока они > key,
    # потом вставь key на освободившееся место
    pass
"""

SORTING_LEARN_TASK3_SOLUTION = """\
def solution(arr):
    arr = list(arr)
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr
"""

# ─────────────────────────────────────────────────────────────
#  NUMPY — дополнительные задания к существующей теме
# ─────────────────────────────────────────────────────────────
NUMPY_TASK2_DESC = r"""Напишите функцию `solution(arr)`, которая принимает список чисел и возвращает **словарь** со следующими статистическими характеристиками:

- `"mean"` — среднее значение (округлить до 4 знаков)
- `"std"` — стандартное отклонение (округлить до 4 знаков)
- `"min"` — минимум
- `"max"` — максимум

Используй NumPy.

### Пример

```python
solution([1, 2, 3, 4, 5])
# → {"mean": 3.0, "std": 1.4142, "min": 1.0, "max": 5.0}
```
"""

NUMPY_TASK2_STARTER = """\
import numpy as np


def solution(arr):
    # Напиши своё решение здесь
    pass
"""

NUMPY_TASK2_SOLUTION = """\
import numpy as np


def solution(arr):
    a = np.array(arr, dtype=float)
    return {
        "mean": round(float(np.mean(a)), 4),
        "std": round(float(np.std(a)), 4),
        "min": float(np.min(a)),
        "max": float(np.max(a)),
    }
"""

NUMPY_TASK3_DESC = r"""Напишите функцию `solution(matrix)`, которая принимает двумерный список (матрицу) и возвращает **транспонированную матрицу** в виде списка списков.

Используй NumPy.

### Пример

```python
solution([[1, 2, 3], [4, 5, 6]])
# → [[1, 4], [2, 5], [3, 6]]
```
"""

NUMPY_TASK3_STARTER = """\
import numpy as np


def solution(matrix):
    # Напиши своё решение здесь
    pass
"""

NUMPY_TASK3_SOLUTION = """\
import numpy as np


def solution(matrix):
    return np.array(matrix).T.tolist()
"""

# ─────────────────────────────────────────────────────────────
#  PANDAS
# ─────────────────────────────────────────────────────────────
PANDAS_CONTENT = r"""# Pandas

**Pandas** — библиотека для работы с табличными данными. Если NumPy работает с числовыми массивами, то Pandas предназначен для данных со смешанными типами, пропусками, метками — как таблицы в Excel или SQL.

## Основные структуры

### Series

Одномерный массив с метками (индексом):

```python
import pandas as pd

s = pd.Series([10, 20, 30], index=["a", "b", "c"])
print(s["b"])  # 20
```

### DataFrame

Двумерная таблица — набор Series с общим индексом:

```python
df = pd.DataFrame({
    "name": ["Иван", "Мария", "Пётр"],
    "age": [25, 30, 22],
    "score": [88, 95, 71],
})
```

## Основные операции

**Выбор столбца:**
```python
df["age"]              # Series
df[["age", "score"]]   # DataFrame с несколькими столбцами
```

**Фильтрация строк:**
```python
df[df["age"] > 24]
df[df["score"] >= 88]
```

**Агрегация:**
```python
df["score"].mean()
df["score"].max()
df.describe()
```

**GroupBy:**
```python
df.groupby("group")["score"].mean()
```

**Создание нового столбца:**
```python
df["passed"] = df["score"] >= 80
```

## Зачем это нужно

Pandas используется везде, где есть данные в табличном формате:
- анализ данных и отчёты
- предобработка данных перед машинным обучением
- чтение CSV, Excel, SQL-таблиц

> **Совет:** метод `.loc[строки, столбцы]` для выборки по меткам, `.iloc[i, j]` — по позициям.
"""

PANDAS_TASK1_DESC = r"""Напишите функцию `solution(data)`, которая принимает словарь `data` с ключами `"name"` (список строк) и `"score"` (список чисел), создаёт DataFrame и возвращает **список имён студентов, набравших 80 и более баллов**, отсортированный по алфавиту.

### Пример

```python
data = {
    "name": ["Иван", "Мария", "Пётр", "Анна"],
    "score": [88, 95, 71, 80],
}
solution(data)  # → ["Анна", "Иван", "Мария"]
```
"""

PANDAS_TASK1_STARTER = """\
import pandas as pd


def solution(data):
    # Создай DataFrame из словаря data
    # Отфильтруй строки где score >= 80
    # Верни список имён, отсортированный по алфавиту
    pass
"""

PANDAS_TASK1_SOLUTION = """\
import pandas as pd


def solution(data):
    df = pd.DataFrame(data)
    passed = df[df["score"] >= 80]["name"]
    return sorted(passed.tolist())
"""

PANDAS_TASK2_DESC = r"""Напишите функцию `solution(data)`, которая принимает словарь с ключами `"department"` и `"salary"`, создаёт DataFrame и возвращает **словарь** со средней зарплатой по каждому отделу (округлить до 2 знаков).

### Пример

```python
data = {
    "department": ["IT", "HR", "IT", "HR", "IT"],
    "salary": [100000, 60000, 120000, 65000, 90000],
}
solution(data)
# → {"HR": 62500.0, "IT": 103333.33}
```
"""

PANDAS_TASK2_STARTER = """\
import pandas as pd


def solution(data):
    # Создай DataFrame
    # Используй groupby("department")["salary"].mean()
    # Верни словарь {отдел: средняя_зарплата}
    pass
"""

PANDAS_TASK2_SOLUTION = """\
import pandas as pd


def solution(data):
    df = pd.DataFrame(data)
    result = df.groupby("department")["salary"].mean()
    return {k: round(v, 2) for k, v in result.items()}
"""

PANDAS_TASK3_DESC = r"""Напишите функцию `solution(data)`, которая принимает словарь с ключами `"name"`, `"math"`, `"python"`, создаёт DataFrame, добавляет столбец `"average"` (среднее math и python), и возвращает имя студента с **наивысшим средним баллом**.

### Пример

```python
data = {
    "name": ["Иван", "Мария", "Пётр"],
    "math": [80, 95, 70],
    "python": [90, 85, 95],
}
solution(data)  # → "Мария"  (среднее: 90)
```
"""

PANDAS_TASK3_STARTER = """\
import pandas as pd


def solution(data):
    # Создай DataFrame
    # Добавь столбец average = (math + python) / 2
    # Верни имя студента с максимальным average
    pass
"""

PANDAS_TASK3_SOLUTION = """\
import pandas as pd


def solution(data):
    df = pd.DataFrame(data)
    df["average"] = (df["math"] + df["python"]) / 2
    return df.loc[df["average"].idxmax(), "name"]
"""

# ─────────────────────────────────────────────────────────────
#  Тест-коды с Python-словарями выносим в отдельные переменные,
#  чтобы f-string не интерпретировал фигурные скобки внутри них.
# ─────────────────────────────────────────────────────────────
_P1_T1 = (
    'data = {"name": ["Иван", "Мария", "Пётр", "Анна"], "score": [88, 95, 71, 80]}\n'
    'assert solution(data) == ["Анна", "Иван", "Мария"]'
)
_P1_T2 = 'data = {"name": ["А", "Б"], "score": [50, 60]}\nassert solution(data) == []'
_P1_T3 = (
    'data = {"name": ["X", "Y", "Z"], "score": [100, 80, 79]}\n'
    'assert solution(data) == ["X", "Y"]'
)

_P2_T1 = (
    'data = {"department": ["IT", "HR", "IT", "HR", "IT"], "salary": [100000, 60000, 120000, 65000, 90000]}\n'
    "result = solution(data)\n"
    "assert result['HR'] == 62500.0\n"
    "assert result['IT'] == round((100000 + 120000 + 90000) / 3, 2)"
)
_P2_T2 = (
    'data = {"department": ["A", "A"], "salary": [100, 200]}\n'
    "assert solution(data) == {'A': 150.0}"
)
_P2_T3 = (
    'data = {"department": ["X"], "salary": [99999]}\n'
    "assert solution(data) == {'X': 99999.0}"
)

_P3_T1 = (
    'data = {"name": ["Иван", "Мария", "Пётр"], "math": [80, 95, 70], "python": [90, 85, 95]}\n'
    'assert solution(data) == "Мария"'
)
_P3_T2 = (
    'data = {"name": ["А", "Б"], "math": [100, 50], "python": [100, 50]}\n'
    'assert solution(data) == "А"'
)
_P3_T3 = (
    'data = {"name": ["X"], "math": [70], "python": [80]}\nassert solution(data) == "X"'
)


def upgrade() -> None:
    # ── Алгоритмы сортировки (учебная тема) ──────────────────
    op.execute(f"""
        INSERT INTO topics (slug, title, content, order_index, is_published, is_interview)
        VALUES (
            'sorting',
            'Алгоритмы сортировки',
            $topic${SORTING_LEARN_CONTENT}$topic$,
            2,
            true,
            false
        );
    """)

    op.execute(f"""
        INSERT INTO tasks (
            topic_id, title, description, starter_code, solution_code,
            order_index, time_limit_sec, memory_limit_mb, is_published
        )
        VALUES (
            (SELECT id FROM topics WHERE slug = 'sorting'),
            'Сортировка пузырьком',
            $desc${SORTING_LEARN_TASK1_DESC}$desc$,
            $starter${SORTING_LEARN_TASK1_STARTER}$starter$,
            $solution${SORTING_LEARN_TASK1_SOLUTION}$solution$,
            1, 10, 256, true
        );
    """)

    op.execute("""
        INSERT INTO task_tests (task_id, test_code, is_hidden, order_index)
        VALUES
            (
                (SELECT id FROM tasks WHERE title = 'Сортировка пузырьком'),
                'assert solution([64, 34, 25, 12, 22, 11, 90]) == [11, 12, 22, 25, 34, 64, 90]',
                false, 1
            ),
            (
                (SELECT id FROM tasks WHERE title = 'Сортировка пузырьком'),
                'assert solution([5, 1, 4, 2, 8]) == [1, 2, 4, 5, 8]',
                false, 2
            ),
            (
                (SELECT id FROM tasks WHERE title = 'Сортировка пузырьком'),
                'assert solution([1]) == [1]',
                true, 3
            );
    """)

    op.execute(f"""
        INSERT INTO tasks (
            topic_id, title, description, starter_code, solution_code,
            order_index, time_limit_sec, memory_limit_mb, is_published
        )
        VALUES (
            (SELECT id FROM topics WHERE slug = 'sorting'),
            'Сортировка выбором',
            $desc${SORTING_LEARN_TASK2_DESC}$desc$,
            $starter${SORTING_LEARN_TASK2_STARTER}$starter$,
            $solution${SORTING_LEARN_TASK2_SOLUTION}$solution$,
            2, 10, 256, true
        );
    """)

    op.execute("""
        INSERT INTO task_tests (task_id, test_code, is_hidden, order_index)
        VALUES
            (
                (SELECT id FROM tasks WHERE title = 'Сортировка выбором'),
                'assert solution([64, 25, 12, 22, 11]) == [11, 12, 22, 25, 64]',
                false, 1
            ),
            (
                (SELECT id FROM tasks WHERE title = 'Сортировка выбором'),
                'assert solution([3, 2, 1]) == [1, 2, 3]',
                false, 2
            ),
            (
                (SELECT id FROM tasks WHERE title = 'Сортировка выбором'),
                'assert solution([1, 1, 1]) == [1, 1, 1]',
                true, 3
            );
    """)

    op.execute(f"""
        INSERT INTO tasks (
            topic_id, title, description, starter_code, solution_code,
            order_index, time_limit_sec, memory_limit_mb, is_published
        )
        VALUES (
            (SELECT id FROM topics WHERE slug = 'sorting'),
            'Сортировка вставками',
            $desc${SORTING_LEARN_TASK3_DESC}$desc$,
            $starter${SORTING_LEARN_TASK3_STARTER}$starter$,
            $solution${SORTING_LEARN_TASK3_SOLUTION}$solution$,
            3, 10, 256, true
        );
    """)

    op.execute("""
        INSERT INTO task_tests (task_id, test_code, is_hidden, order_index)
        VALUES
            (
                (SELECT id FROM tasks WHERE title = 'Сортировка вставками'),
                'assert solution([12, 11, 13, 5, 6]) == [5, 6, 11, 12, 13]',
                false, 1
            ),
            (
                (SELECT id FROM tasks WHERE title = 'Сортировка вставками'),
                'assert solution([4, 3, 2, 1]) == [1, 2, 3, 4]',
                false, 2
            ),
            (
                (SELECT id FROM tasks WHERE title = 'Сортировка вставками'),
                'assert solution([1, 2, 3]) == [1, 2, 3]',
                true, 3
            );
    """)

    # ── NumPy — дополнительные задания ───────────────────────
    op.execute(f"""
        INSERT INTO tasks (
            topic_id, title, description, starter_code, solution_code,
            order_index, time_limit_sec, memory_limit_mb, is_published
        )
        VALUES (
            (SELECT id FROM topics WHERE slug = 'numpy'),
            'Статистика массива',
            $desc${NUMPY_TASK2_DESC}$desc$,
            $starter${NUMPY_TASK2_STARTER}$starter$,
            $solution${NUMPY_TASK2_SOLUTION}$solution$,
            2, 10, 1024, true
        );
    """)

    op.execute("""
        INSERT INTO task_tests (task_id, test_code, is_hidden, order_index)
        VALUES
            (
                (SELECT id FROM tasks WHERE title = 'Статистика массива'),
                $t$
result = solution([1, 2, 3, 4, 5])
assert result["mean"] == 3.0
assert result["min"] == 1.0
assert result["max"] == 5.0
$t$,
                false, 1
            ),
            (
                (SELECT id FROM tasks WHERE title = 'Статистика массива'),
                $t$
result = solution([10, 10, 10])
assert result["std"] == 0.0
assert result["mean"] == 10.0
$t$,
                false, 2
            ),
            (
                (SELECT id FROM tasks WHERE title = 'Статистика массива'),
                $t$
import numpy as np
result = solution([1, 2, 3, 4, 5])
assert abs(result["std"] - round(float(np.std([1, 2, 3, 4, 5])), 4)) < 1e-4
$t$,
                true, 3
            );
    """)

    op.execute(f"""
        INSERT INTO tasks (
            topic_id, title, description, starter_code, solution_code,
            order_index, time_limit_sec, memory_limit_mb, is_published
        )
        VALUES (
            (SELECT id FROM topics WHERE slug = 'numpy'),
            'Транспонирование матрицы',
            $desc${NUMPY_TASK3_DESC}$desc$,
            $starter${NUMPY_TASK3_STARTER}$starter$,
            $solution${NUMPY_TASK3_SOLUTION}$solution$,
            3, 10, 1024, true
        );
    """)

    op.execute("""
        INSERT INTO task_tests (task_id, test_code, is_hidden, order_index)
        VALUES
            (
                (SELECT id FROM tasks WHERE title = 'Транспонирование матрицы'),
                'assert solution([[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]]',
                false, 1
            ),
            (
                (SELECT id FROM tasks WHERE title = 'Транспонирование матрицы'),
                'assert solution([[1, 2], [3, 4]]) == [[1, 3], [2, 4]]',
                false, 2
            ),
            (
                (SELECT id FROM tasks WHERE title = 'Транспонирование матрицы'),
                'assert solution([[5]]) == [[5]]',
                true, 3
            );
    """)

    # ── Pandas ────────────────────────────────────────────────
    op.execute(f"""
        INSERT INTO topics (slug, title, content, order_index, is_published, is_interview)
        VALUES (
            'pandas',
            'Pandas',
            $topic${PANDAS_CONTENT}$topic$,
            3,
            true,
            false
        );
    """)

    op.execute(f"""
        INSERT INTO tasks (
            topic_id, title, description, starter_code, solution_code,
            order_index, time_limit_sec, memory_limit_mb, is_published
        )
        VALUES (
            (SELECT id FROM topics WHERE slug = 'pandas'),
            'Фильтрация студентов',
            $desc${PANDAS_TASK1_DESC}$desc$,
            $starter${PANDAS_TASK1_STARTER}$starter$,
            $solution${PANDAS_TASK1_SOLUTION}$solution$,
            1, 10, 1024, true
        );
    """)

    op.execute(f"""
        INSERT INTO task_tests (task_id, test_code, is_hidden, order_index)
        VALUES
            (
                (SELECT id FROM tasks WHERE title = 'Фильтрация студентов'),
                $t${_P1_T1}$t$,
                false, 1
            ),
            (
                (SELECT id FROM tasks WHERE title = 'Фильтрация студентов'),
                $t${_P1_T2}$t$,
                false, 2
            ),
            (
                (SELECT id FROM tasks WHERE title = 'Фильтрация студентов'),
                $t${_P1_T3}$t$,
                true, 3
            );
    """)

    op.execute(f"""
        INSERT INTO tasks (
            topic_id, title, description, starter_code, solution_code,
            order_index, time_limit_sec, memory_limit_mb, is_published
        )
        VALUES (
            (SELECT id FROM topics WHERE slug = 'pandas'),
            'Средняя зарплата по отделам',
            $desc${PANDAS_TASK2_DESC}$desc$,
            $starter${PANDAS_TASK2_STARTER}$starter$,
            $solution${PANDAS_TASK2_SOLUTION}$solution$,
            2, 10, 1024, true
        );
    """)

    op.execute(f"""
        INSERT INTO task_tests (task_id, test_code, is_hidden, order_index)
        VALUES
            (
                (SELECT id FROM tasks WHERE title = 'Средняя зарплата по отделам'),
                $t${_P2_T1}$t$,
                false, 1
            ),
            (
                (SELECT id FROM tasks WHERE title = 'Средняя зарплата по отделам'),
                $t${_P2_T2}$t$,
                false, 2
            ),
            (
                (SELECT id FROM tasks WHERE title = 'Средняя зарплата по отделам'),
                $t${_P2_T3}$t$,
                true, 3
            );
    """)

    op.execute(f"""
        INSERT INTO tasks (
            topic_id, title, description, starter_code, solution_code,
            order_index, time_limit_sec, memory_limit_mb, is_published
        )
        VALUES (
            (SELECT id FROM topics WHERE slug = 'pandas'),
            'Лучший студент',
            $desc${PANDAS_TASK3_DESC}$desc$,
            $starter${PANDAS_TASK3_STARTER}$starter$,
            $solution${PANDAS_TASK3_SOLUTION}$solution$,
            3, 10, 1024, true
        );
    """)

    op.execute(f"""
        INSERT INTO task_tests (task_id, test_code, is_hidden, order_index)
        VALUES
            (
                (SELECT id FROM tasks WHERE title = 'Лучший студент'),
                $t${_P3_T1}$t$,
                false, 1
            ),
            (
                (SELECT id FROM tasks WHERE title = 'Лучший студент'),
                $t${_P3_T2}$t$,
                false, 2
            ),
            (
                (SELECT id FROM tasks WHERE title = 'Лучший студент'),
                $t${_P3_T3}$t$,
                true, 3
            );
    """)


def downgrade() -> None:
    op.execute("""
        DELETE FROM topics
        WHERE slug IN ('sorting', 'pandas');
    """)
    op.execute("""
        DELETE FROM tasks
        WHERE topic_id = (SELECT id FROM topics WHERE slug = 'numpy')
          AND title IN ('Статистика массива', 'Транспонирование матрицы');
    """)
