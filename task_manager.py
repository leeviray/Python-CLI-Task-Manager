import argparse
import json
import os

FILE_NAME = "tasks.json"

def load_tasks():
    """Memuat tugas dari file JSON."""
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []

def save_tasks(tasks):
    """Menyimpan tugas ke file JSON."""
    with open(FILE_NAME, "w") as file:
        json.dump(tasks, file, indent=4)

def add_task(description):
    """Menambahkan tugas baru."""
    tasks = load_tasks()
    new_id = 1 if len(tasks) == 0 else tasks[-1]["id"] + 1
    
    new_task = {
        "id": new_id,
        "task": description,
        "done": False
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"✅ Tugas berhasil ditambahkan: '{description}' (ID: {new_id})")

def list_tasks():
    """Menampilkan semua tugas."""
    tasks = load_tasks()
    if not tasks:
        print("📭 Tidak ada tugas saat ini.")
        return

    print("\n📝 Daftar Tugas:")
    print("-" * 30)
    for t in tasks:
        status = "[x]" if t["done"] else "[ ]"
        print(f"{t['id']}. {status} {t['task']}")
    print("-" * 30 + "\n")

def complete_task(task_id):
    """Menandai tugas selesai berdasarkan ID."""
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == task_id:
            t["done"] = True
            save_tasks(tasks)
            print(f"🎉 Tugas ID {task_id} ditandai selesai!")
            return
    print(f"❌ Error: Tugas dengan ID {task_id} tidak ditemukan.")

def delete_task(task_id):
    """Menghapus tugas berdasarkan ID."""
    tasks = load_tasks()
    original_length = len(tasks)
    tasks = [t for t in tasks if t["id"] != task_id]
    
    if len(tasks) < original_length:
        save_tasks(tasks)
        print(f"🗑️ Tugas ID {task_id} berhasil dihapus.")
    else:
        print(f"❌ Error: Tugas dengan ID {task_id} tidak ditemukan.")

def main():
    # Setup Argument Parser
    parser = argparse.ArgumentParser(description="CLI Task Manager Sederhana")
    subparsers = parser.add_subparsers(dest="command", help="Perintah yang tersedia")

    # Command: add
    add_parser = subparsers.add_parser("add", help="Tambahkan tugas baru")
    add_parser.add_argument("description", type=str, help="Deskripsi tugas")

    # Command: list
    subparsers.add_parser("list", help="Lihat semua tugas")

    # Command: done
    done_parser = subparsers.add_parser("done", help="Tandai tugas selesai")
    done_parser.add_argument("id", type=int, help="ID tugas")

    # Command: delete
    delete_parser = subparsers.add_parser("delete", help="Hapus tugas")
    delete_parser.add_argument("id", type=int, help="ID tugas")

    args = parser.parse_args()

    # Eksekusi berdasarkan perintah
    if args.command == "add":
        add_task(args.description)
    elif args.command == "list":
        list_tasks()
    elif args.command == "done":
        complete_task(args.id)
    elif args.command == "delete":
        delete_task(args.id)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()