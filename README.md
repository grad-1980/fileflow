# fileflow

`fileflow` — это CLI-утилита для последовательной обработки текстовых файлов
через настраиваемый pipeline процессоров.

Проект сделан как учебный, с упором на чистую архитектуру, ООП и тестируемость.

## Features

- Последовательная обработка файлов через pipeline
- Расширяемые процессоры (каждый — отдельный класс)
- Поддержка CLI-флагов:
    - `--strip`
    - `--lower`
    - `--drop-empty`
    - `--grep SUBSTR`
    - `--replace OLD NEW`
    - `--head N`
    - `--tail N`
- Вывод результата в stdout или файл
- Подробный отчёт о выполнении (steps, chars before/after)
- Полное покрытие тестами (core, processors, pipeline, CLI)

## Installation

Клонируйте репозиторий и установите пакет в editable-режиме:

```bash
git clone https://github.com/<your-username>/fileflow.git
cd fileflow
python -m venv venv
source venv/bin/activate
pip install -e .
```

## Quick start

Обработка файла и вывод в stdout:

```bash
fileflow run input.txt --strip --drop-empty
```

Запись результата в файл:

```bash
fileflow run input.txt --strip --lower --out output.txt
```

Фильтрация и замена:

```bash
fileflow run input.txt --strip --replace error ERROR --grep ERROR
```

Ограничение количества строк:

```bash
fileflow run input.txt --head 10
fileflow run input.txt --tail 5
```

## Available processors

| Processor          | Description                            |
|--------------------|----------------------------------------|
| StripProcessor     | Убирает пробелы по краям каждой строки |
| LowercaseProcessor | Приводит текст к нижнему регистру      |
| DropEmptyProcessor | Удаляет пустые и пробельные строки     |
| GrepProcessor      | Оставляет строки, содержащие подстроку |
| ReplaceProcessor   | Заменяет подстроку OLD на NEW          |
| HeadProcessor      | Оставляет первые N строк               |
| TailProcessor      | Оставляет последние N строк            |

## Architecture

Проект построен вокруг идеи pipeline:

- `Pipeline` применяет процессоры последовательно и полиморфно
- `FileData` — неизменяемый объект данных
- `FileProcessor` — базовый интерфейс процессора
- `Pipeline` — композиция процессоров
- Каждый процессор:
    - не знает о других
    - возвращает новый `FileData`
- Ошибки процессоров оборачиваются в доменные исключения

CLI — тонкая оболочка, которая:

- парсит аргументы
- собирает pipeline
- запускает обработку

## Tests

Проект полностью покрыт тестами с использованием `pytest`.

Запуск тестов:

```bash
pytest
```

Покрытие включает:

- core и pipeline
- процессоры
- CLI (через subprocess)

## Project status

Проект завершён как учебный и используется как часть портфолио.
Фокус проекта — архитектура, тестируемость и чистый CLI-интерфейс.