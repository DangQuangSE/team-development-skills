# game-asset-skills

AI skill package giúp render **AI game art asset** (character/sprite, icon/UI/item, background/tileset) đúng ngay trong 1-2 prompt, thay vì phải sửa đi sửa lại nhiều lần. Dành cho solo dev dùng chat-based AI (Claude chat, Gemini chat, ChatGPT) để ren asset thủ công.

## Mục lục skill

| Skill | Vai trò |
|---|---|
| [game-asset-prompt](./skills/game-asset-prompt/) | Sinh prompt chuẩn theo style bible của project + checklist hậu-kiểm + hướng dẫn hậu kỳ |

---

## Cài đặt

Copy skill vào project của bạn:

```bash
cp -r game-asset-skills/skills/game-asset-prompt <your-project>/skills/
```

Hoặc mở thẳng thư mục `game-asset-skills/` trong Claude Code là dùng được ngay.

---

## Cách dùng

1. Lần đầu gọi skill trong 1 project: trả lời bộ câu hỏi ngắn (≤6 câu) để tạo `art-style-bible.md` ở root project — lưu art direction, palette, resolution, góc nhìn, line weight.
2. Các lần sau: skill tự đọc bible, chỉ hỏi thêm 1-2 câu riêng cho asset đang cần (loại asset, tên, pose/kích thước).
3. Copy prompt sinh ra, paste vào Claude/Gemini/ChatGPT chat để ren ảnh.
4. Đối chiếu kết quả với checklist hậu-kiểm skill đưa ra; nếu sai kỹ thuật (nền không trong suốt, sai size), làm theo hướng dẫn hậu kỳ đi kèm.

Skill không gọi API ren ảnh và không tự động xử lý ảnh — chỉ sinh prompt + hướng dẫn, người dùng tự copy-paste và hậu kỳ thủ công.
