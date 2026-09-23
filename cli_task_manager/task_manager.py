#!/usr/bin/env python3

import argparse
import json
from pathlib import Path


class Task:
    def __init__(self, id, title):
        self.id = id
        self.title = title
        self.status = False

    def __str__(self):
        status_icon = '[+]' if self.status else '[-]'
        return f'[{self.id}] {status_icon} {self.title}'

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.current_id = 1

    def add_task(self, text):
        new_task = Task(self.current_id, text)
        self.tasks.append(new_task)
        self.current_id += 1
        print('Task added')

    def list_tasks(self, show_all, show_completed):
        if not self.tasks:
            print('Task list is empty')
            return
        
        for task in self.tasks:
            if show_completed and not task.status:
                continue
            if not show_all and not show_completed and task.status:
                continue
            print(task)

    def complete_task(self, id):
        for task in self.tasks:
            if task.id == id:
                task.status = True
                print(f'Task {task.id} marked as completed')
                return
        print(f'Task with id {id} not found')

    def remove_task(self, id):
        for task in self.tasks:
            if task.id == id:
                self.tasks.remove(task)
                print(f'Task {id} removed')
                return
        print(f'Task with id {id} not found')

    def save_to_file(self):
        raw_tasks = []

        for task in self.tasks:
            raw_tasks.append({'id': task.id, 'title': task.title, 'status': task.status})

        with open('tasks.json', 'w', encoding='utf-8') as file:
            json.dump(raw_tasks, file, ensure_ascii=False, indent=4)

    def load_from_file(self):
        if not Path('tasks.json').exists():
            return
        
        with open('tasks.json', 'r', encoding='utf-8') as file:
            raw_tasks = json.load(file)

        for i in raw_tasks:
            task = Task(i['id'], i['title'])
            task.status = i['status']
            self.tasks.append(task)

        if self.tasks:
            self.current_id = max(task.id for task in self.tasks) + 1


def main():
    manager = TaskManager()

    manager.load_from_file()

    parser = argparse.ArgumentParser(description='CLI Task Manager')

    subparcers = parser.add_subparsers(dest='command', title='Available commands', required=True)

    parser_add = subparcers.add_parser('add', help='Add new task')
    parser_add.add_argument('text', type=str, help='Task text')

    parser_list = subparcers.add_parser('list', help='List tasks')
    parser_list.add_argument('-a', '--all', action='store_true', help='List all tasks')
    parser_list.add_argument('-c', '--completed', action='store_true', help='List completed tasks')

    parser_done = subparcers.add_parser('done', help='Complete a task')
    parser_done.add_argument('id', type=int, help='Task id')

    parser_remove = subparcers.add_parser('remove', help='Remove a task')
    parser_remove.add_argument('id', type=int, help='Task id')

    args = parser.parse_args()

    if args.command == 'add':
        manager.add_task(args.text)
    elif args.command == 'list':
        manager.list_tasks(show_all=args.all, show_completed=args.completed)
    elif args.command == 'done':
        manager.complete_task(args.id)
    elif args.command == 'remove':
        manager.remove_task(args.id)

    manager.save_to_file()

if __name__ == '__main__':
    main()