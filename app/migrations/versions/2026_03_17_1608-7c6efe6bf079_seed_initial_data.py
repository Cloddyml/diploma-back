"""seed_initial_data

Revision ID: 7c6efe6bf079
Revises: 19e326560919
Create Date: 2026-03-17 16:08:17.086596

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "7c6efe6bf079"
down_revision: Union[str, Sequence[str], None] = "19e326560919"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

TOPIC_CONTENT = r"""# NumPy

**NumPy** (Numerical Python) — фундаментальная библиотека для научных вычислений в Python.
Она предоставляет высокопроизводительный многомерный массив `ndarray` и инструменты для работы с ним.

## Установка

```bash
pip install numpy
```

## Основы: ndarray

В основе NumPy лежит объект `ndarray` — однородный многомерный массив:

```python
import numpy as np

a = np.array([1, 2, 3, 4, 5])
print(a)        # [1 2 3 4 5]
print(a.shape)  # (5,)
print(a.dtype)  # например, int64 (на 32-битных системах и Windows может быть int32)
```

## Полезные операции

| Операция         | Метод              | Описание                        |
|------------------|--------------------|---------------------------------|
| Сумма элементов  | `np.sum(a)`        | Сумма всех элементов            |
| Среднее          | `np.mean(a)`       | Среднее арифметическое          |
| Максимум         | `np.max(a)`        | Наибольший элемент              |
| Минимум          | `np.min(a)`        | Наименьший элемент              |
| Сортировка       | `np.sort(a)`       | Возвращает отсортированный массив|

> **Совет:** NumPy-операции работают над всем массивом сразу — это называется *векторизацией*.
> Избегай Python-циклов там, где можно обойтись операциями NumPy — это на порядки быстрее.

## Пример задачи

Допустим, нужно найти сумму всех элементов массива:

```python
import numpy as np

def solution(arr):
    return int(np.sum(arr))

print(solution([1, 2, 3]))  # 6
```
"""

TASK_DESCRIPTION = r"""Напишите функцию `solution(arr)`, которая принимает список чисел и возвращает **сумму всех элементов** в виде целого числа.

### Требования

- Используй `numpy` для вычисления суммы
- Функция должна возвращать значение типа `int`

### Пример

```python
solution([1, 2, 3, 4, 5])  # → 15
solution([0, -1, 1])        # → 0
solution([100])             # → 100
```

### Ограничения

- Длина массива: от 1 до 10 000 элементов
- Элементы массива: целые числа от -10 000 до 10 000
"""

STARTER_CODE = """\
import numpy as np


def solution(arr):
    # Напиши своё решение здесь
    pass
"""

SOLUTION_CODE = """\
import numpy as np


def solution(arr):
    return int(np.sum(arr))
"""

TEST_1 = """\
assert solution([1, 2, 3, 4, 5]) == 15, f"Expected 15, got {solution([1, 2, 3, 4, 5])}"\
"""

TEST_2 = """\
assert solution([0, -1, 1]) == 0, f"Expected 0, got {solution([0, -1, 1])}"\
"""

TEST_3_HIDDEN = """\
import numpy as np
big = list(range(1, 101))
assert solution(big) == 5050, f"Expected 5050, got {solution(big)}"\
"""


def upgrade() -> None:
    op.execute("""
            TRUNCATE TABLE ai_interactions, task_tests, submissions, tasks, topics
            RESTART IDENTITY CASCADE;
        """)

    op.execute(f"""
            INSERT INTO topics (slug, title, content, order_index, is_published)
            VALUES (
                'numpy',
                'NumPy',
                $topic${TOPIC_CONTENT}$topic$,
                1,
                true
            );
        """)

    op.execute(f"""
            INSERT INTO tasks (
                topic_id, title, description,
                starter_code, solution_code,
                order_index, time_limit_sec, memory_limit_mb, is_published
            )
            VALUES (
                1,
                'Сумма элементов массива',
                $desc${TASK_DESCRIPTION}$desc$,
                $starter${STARTER_CODE}$starter$,
                $solution${SOLUTION_CODE}$solution$,
                1,
                10,
                1024,
                true
            );
        """)

    op.execute(f"""
            INSERT INTO task_tests (task_id, test_code, is_hidden, order_index)
            VALUES
                (1, $t1${TEST_1}$t1$, false, 1),
                (1, $t2${TEST_2}$t2$, false, 2),
                (1, $t3${TEST_3_HIDDEN}$t3$, true,  3);
        """)


def downgrade() -> None:
    op.execute("DELETE FROM topics WHERE slug = 'numpy';")
