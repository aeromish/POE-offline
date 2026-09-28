with open("src/scenes/BattleScene.ts", "r", encoding="utf-8") as f:
    content = f.read()

# Xóa khai báo biến không dùng
content = content.replace("  private hintsText!: Phaser.GameObjects.Text;\n", "")
content = content.replace("this.hintsText = this.add.text(", "this.add.text(")

with open("src/scenes/BattleScene.ts", "w", encoding="utf-8") as f:
    f.write(content)

print("Đã sửa xong lỗi hintsText!")