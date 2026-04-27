"""seed_interview_data

Revision ID: 97296b82bf04
Revises: b4f4eaf691d3
Create Date: 2026-04-27 07:44:07.866244

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "97296b82bf04"
down_revision: Union[str, Sequence[str], None] = "b4f4eaf691d3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# ─────────────────────────────────────────────────────────────
#  ХЭШ-ТАБЛИЦЫ
# ─────────────────────────────────────────────────────────────
HASHTABLE_CONTENT = r"""# Хэш-таблицы

**Хэш-таблица** — структура данных, которая хранит пары ключ-значение и обеспечивает доступ к элементам за **O(1)** в среднем случае.

В Python хэш-таблица реализована как встроенный тип `dict`.

## Как это работает

При добавлении элемента Python вычисляет **хэш** ключа (целое число) и по нему определяет позицию в памяти. Это позволяет находить элемент напрямую, не перебирая всё подряд.

```python
phone_book = {}
phone_book["Иван"] = "89001234567"   # запись за O(1)
print(phone_book["Иван"])             # чтение за O(1)
```

## Основные операции

| Операция | Сложность | Пример |
|---|---|---|
| Вставка | O(1) среднее | `d[key] = value` |
| Чтение | O(1) среднее | `d[key]` |
| Удаление | O(1) среднее | `del d[key]` |
| Проверка наличия | O(1) среднее | `key in d` |

## Типичные паттерны

**Подсчёт частоты элементов:**
```python
def count_frequency(items):
    freq = {}
    for item in items:
        freq[item] = freq.get(item, 0) + 1
    return freq

count_frequency([1, 2, 2, 3, 3, 3])  # {1: 1, 2: 2, 3: 3}
```

**Кэширование уже виденных элементов:**
```python
def has_duplicate(nums):
    seen = set()
    for n in nums:
        if n in seen:
            return True
        seen.add(n)
    return False
```

## Когда использовать

Хэш-таблица — первый инструмент, когда нужно:
- быстро найти элемент по ключу
- посчитать количество вхождений
- проверить, встречался ли элемент раньше
- за один проход записать информацию и использовать её позже

## Коллизии

Иногда два разных ключа дают одинаковый хэш — это называется **коллизией**. Python разрешает их автоматически методом открытой адресации. Вам не нужно об этом думать, но важно понимать, что в худшем случае операции могут деградировать до O(n).

> **На собеседовании:** когда видите задачу «за O(n)» или «без вложенных циклов» — думайте о хэш-таблице.
"""

HASHTABLE_TASK1_DESC = r"""Напишите функцию `solution(nums, target)`, которая принимает список целых чисел `nums` и целое число `target`, и возвращает **индексы двух чисел**, сумма которых равна `target`.

Гарантируется, что ровно одно решение существует. Нельзя использовать один элемент дважды.

**Требования:**
- Сложность O(n) — без вложенных циклов
- Используй хэш-таблицу (словарь)

### Пример

```python
solution([2, 7, 11, 15], 9)   # → [0, 1]  (2 + 7 = 9)
solution([3, 2, 4], 6)        # → [1, 2]  (2 + 4 = 6)
solution([3, 3], 6)           # → [0, 1]
```

### Подсказка

Для каждого числа `x` нужная пара — это `target - x`. Сохраняй в словаре, какие числа ты уже видел.
"""

HASHTABLE_TASK1_STARTER = """\
def solution(nums, target):
    # Напиши своё решение здесь
    pass
"""

HASHTABLE_TASK1_SOLUTION = """\
def solution(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        complement = target - x
        if complement in seen:
            return [seen[complement], i]
        seen[x] = i
"""

HASHTABLE_TASK2_DESC = r"""Напишите функцию `solution(s)`, которая принимает строку `s` и возвращает **первый символ, который встречается только один раз**. Если такого нет — верните `""` (пустую строку).

**Требование:** сложность O(n).

### Пример

```python
solution("leetcode")    # → "l"
solution("aabb")        # → ""
solution("loveleetcode")# → "v"
```
"""

HASHTABLE_TASK2_STARTER = """\
def solution(s):
    # Напиши своё решение здесь
    pass
"""

HASHTABLE_TASK2_SOLUTION = """\
def solution(s):
    freq = {}
    for ch in s:
        freq[ch] = freq.get(ch, 0) + 1
    for ch in s:
        if freq[ch] == 1:
            return ch
    return ""
"""

HASHTABLE_TASK3_DESC = r"""Напишите функцию `solution(nums)`, которая принимает список целых чисел и возвращает список **уникальных дубликатов** — чисел, встречающихся в списке более одного раза.

Порядок в ответе не важен.

### Пример

```python
solution([4, 3, 2, 7, 8, 2, 3, 1])  # → [2, 3]
solution([1, 1, 2])                   # → [1]
solution([1])                         # → []
```
"""

HASHTABLE_TASK3_STARTER = """\
def solution(nums):
    # Напиши своё решение здесь
    pass
"""

HASHTABLE_TASK3_SOLUTION = """\
def solution(nums):
    freq = {}
    for n in nums:
        freq[n] = freq.get(n, 0) + 1
    return [k for k, v in freq.items() if v > 1]
"""

# ─────────────────────────────────────────────────────────────
#  ДЕРЕВЬЯ
# ─────────────────────────────────────────────────────────────
TREES_CONTENT = r"""# Деревья

**Дерево** — иерархическая структура данных. Каждый узел содержит значение и ссылки на дочерние узлы.

## Бинарное дерево поиска (BST)

В **BST** для каждого узла выполняется правило:
- все значения в **левом** поддереве **меньше** текущего узла
- все значения в **правом** поддереве **больше** текущего узла

```
        8
       / \
      3   10
     / \    \
    1   6    14
       / \
      4   7
```

**Реализация узла:**
```python
class TreeNode:
    def __init__(self, val=0):
        self.val = val
        self.left = None
        self.right = None
```

## Вставка в BST

```python
def insert(root, val):
    if root is None:
        return TreeNode(val)
    if val < root.val:
        root.left = insert(root.left, val)
    else:
        root.right = insert(root.right, val)
    return root
```

## Обходы дерева

| Обход | Порядок | Результат для дерева выше |
|---|---|---|
| In-order (LNR) | левый → узел → правый | 1, 3, 4, 6, 7, 8, 10, 14 |
| Pre-order (NLR) | узел → левый → правый | 8, 3, 1, 6, 4, 7, 10, 14 |
| Post-order (LRN) | левый → правый → узел | 1, 4, 7, 6, 3, 14, 10, 8 |

**In-order обход** BST всегда возвращает элементы в **отсортированном порядке** — это ключевое свойство.

```python
def inorder(root):
    if root is None:
        return []
    return inorder(root.left) + [root.val] + inorder(root.right)
```

## Сложность операций BST

| Операция | Среднее | Худший случай |
|---|---|---|
| Поиск | O(log n) | O(n) |
| Вставка | O(log n) | O(n) |
| Удаление | O(log n) | O(n) |

Худший случай — вырожденное дерево (все элементы вставлены по возрастанию). Решение — **сбалансированные деревья** (AVL, Red-Black).

> **На собеседовании:** большинство задач на деревья решается рекурсией. Сначала определите **базовый случай** (обычно `root is None`), потом — что делать с текущим узлом и как объединить результаты от левого и правого поддерева.
"""

TREES_TASK1_DESC = r"""Дан класс узла дерева:

```python
class TreeNode:
    def __init__(self, val=0):
        self.val = val
        self.left = None
        self.right = None
```

Напишите функцию `solution(root)`, которая принимает корень бинарного дерева и возвращает **максимальную глубину** дерева.

Глубина — количество узлов вдоль самого длинного пути от корня до листового узла.

### Пример

```
    3
   / \
  9  20
    /  \
   15   7
```

```python
solution(root)  # → 3
```
"""

TREES_TASK1_STARTER = """\
class TreeNode:
    def __init__(self, val=0):
        self.val = val
        self.left = None
        self.right = None


def solution(root):
    # Напиши своё решение здесь
    pass
"""

TREES_TASK1_SOLUTION = """\
class TreeNode:
    def __init__(self, val=0):
        self.val = val
        self.left = None
        self.right = None


def solution(root):
    if root is None:
        return 0
    left_depth = solution(root.left)
    right_depth = solution(root.right)
    return 1 + max(left_depth, right_depth)
"""

TREES_TASK2_DESC = r"""Дан класс узла дерева:

```python
class TreeNode:
    def __init__(self, val=0):
        self.val = val
        self.left = None
        self.right = None
```

Напишите функцию `solution(root)`, которая возвращает **in-order обход** (левый → узел → правый) в виде списка значений.

### Пример

```
  1
   \
    2
   /
  3
```

```python
solution(root)  # → [1, 3, 2]
```
"""

TREES_TASK2_STARTER = """\
class TreeNode:
    def __init__(self, val=0):
        self.val = val
        self.left = None
        self.right = None


def solution(root):
    # Напиши своё решение здесь
    pass
"""

TREES_TASK2_SOLUTION = """\
class TreeNode:
    def __init__(self, val=0):
        self.val = val
        self.left = None
        self.right = None


def solution(root):
    if root is None:
        return []
    return solution(root.left) + [root.val] + solution(root.right)
"""

TREES_TASK3_DESC = r"""Дан класс узла дерева:

```python
class TreeNode:
    def __init__(self, val=0):
        self.val = val
        self.left = None
        self.right = None
```

Напишите функцию `solution(root)`, которая проверяет, является ли бинарное дерево **симметричным** относительно своего центра.

### Пример

```
    1
   / \
  2   2       → True (симметрично)
 / \ / \
3  4 4  3
```

```
    1
   / \
  2   2       → False
   \   \
    3   3
```
"""

TREES_TASK3_STARTER = """\
class TreeNode:
    def __init__(self, val=0):
        self.val = val
        self.left = None
        self.right = None


def solution(root):
    # Напиши своё решение здесь
    pass
"""

TREES_TASK3_SOLUTION = """\
class TreeNode:
    def __init__(self, val=0):
        self.val = val
        self.left = None
        self.right = None


def solution(root):
    def is_mirror(left, right):
        if left is None and right is None:
            return True
        if left is None or right is None:
            return False
        return (
            left.val == right.val
            and is_mirror(left.left, right.right)
            and is_mirror(left.right, right.left)
        )

    return is_mirror(root.left, root.right) if root else True
"""

# ─────────────────────────────────────────────────────────────
#  СОРТИРОВКА (интервью)
# ─────────────────────────────────────────────────────────────
SORTING_INTERVIEW_CONTENT = r"""# Алгоритмы сортировки

Знание сортировок — обязательный минимум для технических собеседований. Нужно уметь реализовать базовые алгоритмы и понимать их сложность.

## Сравнение алгоритмов

| Алгоритм | Лучшее | Среднее | Худшее | Память |
|---|---|---|---|---|
| Bubble Sort | O(n) | O(n²) | O(n²) | O(1) |
| Selection Sort | O(n²) | O(n²) | O(n²) | O(1) |
| Insertion Sort | O(n) | O(n²) | O(n²) | O(1) |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) |
| Quick Sort | O(n log n) | O(n log n) | O(n²) | O(log n) |

## Пузырьковая сортировка (Bubble Sort)

Принцип: на каждой итерации «всплывает» наибольший элемент.

```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr
```

## Сортировка слиянием (Merge Sort)

Принцип: разбить массив на половины, отсортировать каждую рекурсивно, слить обратно.

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

## Быстрая сортировка (Quick Sort)

Принцип: выбрать опорный элемент (pivot), разбить массив на «меньше» и «больше», отсортировать рекурсивно.

```python
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)
```

> **На собеседовании:** обычно просят реализовать merge sort или объяснить разницу между ними. Ключевой вопрос — почему merge sort гарантирует O(n log n), а quick sort — нет.
"""

SORTING_TASK1_DESC = r"""Напишите функцию `solution(arr)`, которая реализует **сортировку слиянием** (Merge Sort) и возвращает отсортированный список.

### Пример

```python
solution([5, 2, 4, 6, 1, 3])  # → [1, 2, 3, 4, 5, 6]
solution([3, 1])               # → [1, 3]
solution([1])                  # → [1]
```

### Требование

Реализуй сортировку самостоятельно, без использования встроенной `sorted()`.
"""

SORTING_TASK1_STARTER = """\
def solution(arr):
    # Напиши своё решение здесь
    pass
"""

SORTING_TASK1_SOLUTION = """\
def solution(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = solution(arr[: mid])
    right = solution(arr[mid:])
    return _merge(left, right)


def _merge(left, right):
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
"""

SORTING_TASK2_DESC = r"""Напишите функцию `solution(nums, k)`, которая принимает список целых чисел `nums` и целое `k`, и возвращает **k-й наибольший** элемент.

Это k-й наибольший по значению, а не по индексу.

### Пример

```python
solution([3, 2, 1, 5, 6, 4], 2)  # → 5
solution([3, 2, 3, 1, 2, 4, 5, 5, 6], 4)  # → 4
```

### Подсказка

Отсортируй список в порядке убывания и возьми элемент с индексом `k - 1`. Можно использовать `sorted()`.
"""

SORTING_TASK2_STARTER = """\
def solution(nums, k):
    # Напиши своё решение здесь
    pass
"""

SORTING_TASK2_SOLUTION = """\
def solution(nums, k):
    return sorted(nums, reverse=True)[k - 1]
"""


def upgrade() -> None:
    # ── Хэш-таблицы ──────────────────────────────────────────
    op.execute(f"""
        INSERT INTO topics (slug, title, content, order_index, is_published, is_interview)
        VALUES (
            'interview-hashtables',
            'Хэш-таблицы',
            $topic${HASHTABLE_CONTENT}$topic$,
            1,
            true,
            true
        );
    """)

    op.execute(f"""
        INSERT INTO tasks (
            topic_id, title, description, starter_code, solution_code,
            order_index, time_limit_sec, memory_limit_mb, is_published
        )
        VALUES (
            (SELECT id FROM topics WHERE slug = 'interview-hashtables'),
            'Two Sum',
            $desc${HASHTABLE_TASK1_DESC}$desc$,
            $starter${HASHTABLE_TASK1_STARTER}$starter$,
            $solution${HASHTABLE_TASK1_SOLUTION}$solution$,
            1, 10, 256, true
        );
    """)

    op.execute(f"""
        INSERT INTO task_tests (task_id, test_code, is_hidden, order_index)
        VALUES
            (
                (SELECT id FROM tasks WHERE title = 'Two Sum'),
                'assert solution([2, 7, 11, 15], 9) == [0, 1], f"Expected [0, 1], got {{solution([2, 7, 11, 15], 9)}}"',
                false, 1
            ),
            (
                (SELECT id FROM tasks WHERE title = 'Two Sum'),
                'assert solution([3, 2, 4], 6) == [1, 2], f"Expected [1, 2], got {{solution([3, 2, 4], 6)}}"',
                false, 2
            ),
            (
                (SELECT id FROM tasks WHERE title = 'Two Sum'),
                'assert solution([3, 3], 6) == [0, 1], f"Expected [0, 1], got {{solution([3, 3], 6)}}"',
                true, 3
            );
    """)

    op.execute(f"""
        INSERT INTO tasks (
            topic_id, title, description, starter_code, solution_code,
            order_index, time_limit_sec, memory_limit_mb, is_published
        )
        VALUES (
            (SELECT id FROM topics WHERE slug = 'interview-hashtables'),
            'Первый уникальный символ',
            $desc${HASHTABLE_TASK2_DESC}$desc$,
            $starter${HASHTABLE_TASK2_STARTER}$starter$,
            $solution${HASHTABLE_TASK2_SOLUTION}$solution$,
            2, 10, 256, true
        );
    """)

    op.execute(f"""
        INSERT INTO task_tests (task_id, test_code, is_hidden, order_index)
        VALUES
            (
                (SELECT id FROM tasks WHERE title = 'Первый уникальный символ'),
                'assert solution("leetcode") == "l", f"Expected ''l'', got {{solution(''leetcode'')}}"',
                false, 1
            ),
            (
                (SELECT id FROM tasks WHERE title = 'Первый уникальный символ'),
                'assert solution("aabb") == "", f"Expected empty string, got {{solution(''aabb'')}}"',
                false, 2
            ),
            (
                (SELECT id FROM tasks WHERE title = 'Первый уникальный символ'),
                'assert solution("loveleetcode") == "v", f"Expected ''v'', got {{solution(''loveleetcode'')}}"',
                true, 3
            );
    """)

    op.execute(f"""
        INSERT INTO tasks (
            topic_id, title, description, starter_code, solution_code,
            order_index, time_limit_sec, memory_limit_mb, is_published
        )
        VALUES (
            (SELECT id FROM topics WHERE slug = 'interview-hashtables'),
            'Найти дубликаты',
            $desc${HASHTABLE_TASK3_DESC}$desc$,
            $starter${HASHTABLE_TASK3_STARTER}$starter$,
            $solution${HASHTABLE_TASK3_SOLUTION}$solution$,
            3, 10, 256, true
        );
    """)

    op.execute(f"""
        INSERT INTO task_tests (task_id, test_code, is_hidden, order_index)
        VALUES
            (
                (SELECT id FROM tasks WHERE title = 'Найти дубликаты'),
                'assert sorted(solution([4, 3, 2, 7, 8, 2, 3, 1])) == [2, 3]',
                false, 1
            ),
            (
                (SELECT id FROM tasks WHERE title = 'Найти дубликаты'),
                'assert solution([1]) == []',
                false, 2
            ),
            (
                (SELECT id FROM tasks WHERE title = 'Найти дубликаты'),
                'assert sorted(solution([1, 1, 2])) == [1]',
                true, 3
            );
    """)

    # ── Деревья ───────────────────────────────────────────────
    op.execute(f"""
        INSERT INTO topics (slug, title, content, order_index, is_published, is_interview)
        VALUES (
            'interview-trees',
            'Деревья',
            $topic${TREES_CONTENT}$topic$,
            2,
            true,
            true
        );
    """)

    op.execute(f"""
        INSERT INTO tasks (
            topic_id, title, description, starter_code, solution_code,
            order_index, time_limit_sec, memory_limit_mb, is_published
        )
        VALUES (
            (SELECT id FROM topics WHERE slug = 'interview-trees'),
            'Максимальная глубина дерева',
            $desc${TREES_TASK1_DESC}$desc$,
            $starter${TREES_TASK1_STARTER}$starter$,
            $solution${TREES_TASK1_SOLUTION}$solution$,
            1, 10, 256, true
        );
    """)

    op.execute(f"""
        INSERT INTO task_tests (task_id, test_code, is_hidden, order_index)
        VALUES
            (
                (SELECT id FROM tasks WHERE title = 'Максимальная глубина дерева'),
                $t$
root = TreeNode(3)
root.left = TreeNode(9)
root.right = TreeNode(20)
root.right.left = TreeNode(15)
root.right.right = TreeNode(7)
assert solution(root) == 3, f"Expected 3, got {{solution(root)}}"
$t$,
                false, 1
            ),
            (
                (SELECT id FROM tasks WHERE title = 'Максимальная глубина дерева'),
                'assert solution(None) == 0',
                false, 2
            ),
            (
                (SELECT id FROM tasks WHERE title = 'Максимальная глубина дерева'),
                $t$
root = TreeNode(1)
root.right = TreeNode(2)
assert solution(root) == 2
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
            (SELECT id FROM topics WHERE slug = 'interview-trees'),
            'Обход дерева in-order',
            $desc${TREES_TASK2_DESC}$desc$,
            $starter${TREES_TASK2_STARTER}$starter$,
            $solution${TREES_TASK2_SOLUTION}$solution$,
            2, 10, 256, true
        );
    """)

    op.execute(f"""
        INSERT INTO task_tests (task_id, test_code, is_hidden, order_index)
        VALUES
            (
                (SELECT id FROM tasks WHERE title = 'Обход дерева in-order'),
                $t$
root = TreeNode(1)
root.right = TreeNode(2)
root.right.left = TreeNode(3)
assert solution(root) == [1, 3, 2]
$t$,
                false, 1
            ),
            (
                (SELECT id FROM tasks WHERE title = 'Обход дерева in-order'),
                'assert solution(None) == []',
                false, 2
            ),
            (
                (SELECT id FROM tasks WHERE title = 'Обход дерева in-order'),
                $t$
root = TreeNode(4)
root.left = TreeNode(2)
root.right = TreeNode(6)
root.left.left = TreeNode(1)
root.left.right = TreeNode(3)
assert solution(root) == [1, 2, 3, 4, 6]
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
            (SELECT id FROM topics WHERE slug = 'interview-trees'),
            'Симметричное дерево',
            $desc${TREES_TASK3_DESC}$desc$,
            $starter${TREES_TASK3_STARTER}$starter$,
            $solution${TREES_TASK3_SOLUTION}$solution$,
            3, 10, 256, true
        );
    """)

    op.execute(f"""
        INSERT INTO task_tests (task_id, test_code, is_hidden, order_index)
        VALUES
            (
                (SELECT id FROM tasks WHERE title = 'Симметричное дерево'),
                $t$
root = TreeNode(1)
root.left = TreeNode(2)
root.right = TreeNode(2)
root.left.left = TreeNode(3)
root.left.right = TreeNode(4)
root.right.left = TreeNode(4)
root.right.right = TreeNode(3)
assert solution(root) == True
$t$,
                false, 1
            ),
            (
                (SELECT id FROM tasks WHERE title = 'Симметричное дерево'),
                $t$
root = TreeNode(1)
root.left = TreeNode(2)
root.right = TreeNode(2)
root.left.right = TreeNode(3)
root.right.right = TreeNode(3)
assert solution(root) == False
$t$,
                false, 2
            ),
            (
                (SELECT id FROM tasks WHERE title = 'Симметричное дерево'),
                'assert solution(None) == True',
                true, 3
            );
    """)

    # ── Сортировка (интервью) ─────────────────────────────────
    op.execute(f"""
        INSERT INTO topics (slug, title, content, order_index, is_published, is_interview)
        VALUES (
            'interview-sorting',
            'Алгоритмы сортировки',
            $topic${SORTING_INTERVIEW_CONTENT}$topic$,
            3,
            true,
            true
        );
    """)

    op.execute(f"""
        INSERT INTO tasks (
            topic_id, title, description, starter_code, solution_code,
            order_index, time_limit_sec, memory_limit_mb, is_published
        )
        VALUES (
            (SELECT id FROM topics WHERE slug = 'interview-sorting'),
            'Сортировка слиянием',
            $desc${SORTING_TASK1_DESC}$desc$,
            $starter${SORTING_TASK1_STARTER}$starter$,
            $solution${SORTING_TASK1_SOLUTION}$solution$,
            1, 10, 256, true
        );
    """)

    op.execute(f"""
        INSERT INTO task_tests (task_id, test_code, is_hidden, order_index)
        VALUES
            (
                (SELECT id FROM tasks WHERE title = 'Сортировка слиянием'),
                'assert solution([5, 2, 4, 6, 1, 3]) == [1, 2, 3, 4, 5, 6]',
                false, 1
            ),
            (
                (SELECT id FROM tasks WHERE title = 'Сортировка слиянием'),
                'assert solution([3, 1]) == [1, 3]',
                false, 2
            ),
            (
                (SELECT id FROM tasks WHERE title = 'Сортировка слиянием'),
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
            (SELECT id FROM topics WHERE slug = 'interview-sorting'),
            'K-й наибольший элемент',
            $desc${SORTING_TASK2_DESC}$desc$,
            $starter${SORTING_TASK2_STARTER}$starter$,
            $solution${SORTING_TASK2_SOLUTION}$solution$,
            2, 10, 256, true
        );
    """)

    op.execute(f"""
        INSERT INTO task_tests (task_id, test_code, is_hidden, order_index)
        VALUES
            (
                (SELECT id FROM tasks WHERE title = 'K-й наибольший элемент'),
                'assert solution([3, 2, 1, 5, 6, 4], 2) == 5',
                false, 1
            ),
            (
                (SELECT id FROM tasks WHERE title = 'K-й наибольший элемент'),
                'assert solution([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4',
                false, 2
            ),
            (
                (SELECT id FROM tasks WHERE title = 'K-й наибольший элемент'),
                'assert solution([1], 1) == 1',
                true, 3
            );
    """)


def downgrade() -> None:
    op.execute("""
        DELETE FROM topics
        WHERE slug IN (
            'interview-hashtables',
            'interview-trees',
            'interview-sorting'
        );
    """)
