extends Node2D


func _ready() -> void:
	var file_path = "res://2222.txt"
	read_text_file(file_path)

# func _process(delta: float) -> void:
#     pass

func read_text_file(file_path: String) -> void:
	var file = FileAccess.open(file_path, FileAccess.READ)
	var content = file.get_as_text()
	print(content)
