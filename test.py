from memory.memory import (
    add_fact,
    get_facts,
    update_fact,
    delete_fact,
)

add_fact("Я изучаю Python")

print("После добавления:")
print(get_facts())

update_fact(
    "Я изучаю Python",
    "Я изучаю FastAPI"
)

print("После обновления:")
print(get_facts())

delete_fact("Я изучаю FastAPI")

print("После удаления:")
print(get_facts())
