---
name: tehla-wall-extraction
description: >
  Trích xuất và tính diện tích tường gạch (tehlové murivo / tehla) từ bản vẽ
  kiến trúc PDF hoặc CAD. Dùng skill này bất cứ khi nào người dùng upload bản vẽ
  và hỏi về tường gạch, xây gạch, priečky, POROTHERM, diện tích murivo, tính tiền
  xây tường, hoặc xuất kết quả ra Excel/PDF. QUAN TRỌNG: skill này chứa các quy
  tắc phân biệt tường gạch (tehla) với tường bê tông (ŽB/betón) – hai loại vật
  liệu hoàn toàn khác nhau, dễ nhầm lẫn khi đọc bản vẽ.
---

# Skill: Tehlové murivo – Quy trình trích xuất và tính diện tích

> **⚠️ Dữ liệu dùng để tính tiền công nhân viên. Tính sai còn nguy hiểm hơn dừng lại hỏi.**  
> Khi không chắc chắn bất kỳ thông số nào → xem `references/stop-and-ask.md` và hỏi người dùng.

## References – Đọc khi cần:
- `references/stop-and-ask.md` — Mẫu câu hỏi khi dừng lại (7 tình huống + cấu trúc câu hỏi)
- `references/wall-height-openings.md` — Chiều cao S.H. + cách đọc kích thước cửa/cửa sổ
- `references/hranice-poziarnych.md` — Phân biệt Hranice požiarnych úsekov với tehla

---

## BƯỚC 0 – RENDER BẢN VẼ

**Thư mục output:** Tạo 1 thư mục mới cùng tên với file input (PDF/CAD, bỏ phần mở rộng), ví dụ input `Pôdorys_1NP.pdf` → thư mục `Pôdorys_1NP/`. Mọi file output (Excel, PDF overlay, ảnh debug) đều lưu vào thư mục này.

```bash
pdftoppm -jpeg -r 150 -f 1 -l 1 input.pdf /tmp/page150  # tối thiểu
pdftoppm -jpeg -r 250 -f 1 -l 1 input.pdf /tmp/page250  # cho legend
```
```python
from PIL import Image
Image.MAX_IMAGE_PIXELS = None  # bắt buộc cho bản vẽ lớn
```

---

## BƯỚC 1 – ĐỌC LEGENDA MATERIÁLOV ⚠️ (Bước quan trọng nhất)

**Không được bỏ qua. Không được giả định vật liệu theo kích thước.**

Tìm bằng pixel đỏ: `red_mask = (arr[:,:,0]>180) & (arr[:,:,1]<80) & (arr[:,:,2]<80)`

### Bảng phân biệt vật liệu (chuẩn SK/CZ):

| Ký hiệu trong bản vẽ | Vật liệu | Tính? |
|----------------------|----------|-------|
| Hatch chéo **ĐỎ** đặc | Akustické tehlové murivo 250mm (POROTHERM) | ✅ TEHLA |
| Chữ **X ĐỎ** dày | Priečky brúsené tehly 140/100mm (PTH Profi) | ✅ TEHLA |
| Chữ **X ĐỎ** nhạt hơn | Priečky bytoch 115mm (PTH Profi, Rw=43dB) | ✅ TEHLA |
| Đường ngang ĐEN + nền **XÁM NHẠT** | Obvodová ŽB stena 300mm + zateplenie | ❌ ŽB |
| Đường ngang ĐEN (không xám) | Obvodová ŽB stena 200mm + zateplenie | ❌ ŽB |
| Hatch chéo ĐEN/XÁM | ŽB stena + MULTIPOR | ❌ ŽB |
| Đường ngang đen đơn | Betónové murivo 200/150/100mm | ❌ Betón |
| Đường đứt nét **CAM** `–·–·–·` | Hranice požiarnych úsekov | ❌ Không phải tường |
| Xanh lam + trắng | Sadrokartónové predsteny (ZTI) | ❌ Sadrokartón |

**Quy tắc vàng: Chỉ pixel MÀU ĐỎ mới là TEHLA. Đen + xám = ŽB/Betón.**  
Nếu ký hiệu không rõ hoặc không có trong bảng → ⛔ xem `references/stop-and-ask.md`  
Nếu thấy đường cam đứt nét → ⛔ xem `references/hranice-poziarnych.md`

---

## BƯỚC 2 – PHÁT HIỆN TEHLA BẰNG PIXEL MÀU

```python
def is_tehla_wall(arr, y1, y2, x1, x2):
    pad = 15  # mở rộng vùng scan để bắt hatch ở rìa
    r = arr[max(0,y1-pad):y2+pad, max(0,x1-pad):x2+pad]
    red_tehla  = np.sum((r[:,:,0]>160) & (r[:,:,1]<80)  & (r[:,:,2]<80))
    red_poziar = np.sum((r[:,:,0]>180) & (r[:,:,1]>80)  & (r[:,:,1]<140) & (r[:,:,2]<60))
    grey       = np.sum((r[:,:,0]>160) & (r[:,:,0]<240) &
                        (r[:,:,1]>160) & (r[:,:,1]<240) &
                        (r[:,:,2]>160) & (r[:,:,2]<240))
    if red_tehla > 15 and red_tehla > red_poziar * 2:
        return True,  "TEHLA"
    if red_poziar > red_tehla:
        return False, "Hranice požiarnych úsekov"
    if grey > 80:
        return False, "ŽB + zateplenie"
    return False, "ŽB / Betón"
```

**Luôn xác nhận bằng visual crop trước khi dùng kết quả.**

---

## BƯỚC 3 – TỌA ĐỘ VÀ SCALE

```python
# Scale từ grid dimension line (thường 7700mm)
scale_px_per_m = khoang_cach_px_giua_2_tick / (grid_mm / 1000)

# Tìm biên khối phòng bằng đường đen đậm
def find_wall_row(arr, r_min, r_max, c_min, c_max, min_black=500):
    for y in range(r_min, r_max, 5):
        n = np.sum((arr[y, c_min:c_max, 0]<60) &
                   (arr[y, c_min:c_max, 1]<60) &
                   (arr[y, c_min:c_max, 2]<60))
        if n > min_black: return y
    return None
```

**Vẽ grid debug trước khi dùng tọa độ:**
```python
d.line([(0,r),(W,r)], fill=(255,0,0), width=1)  # mỗi 200px
img.resize((W//4, H//4)).save("/tmp/grid_check.jpg")
# → Xem ảnh, xác nhận tọa độ khớp với phòng trong bản vẽ
```

---

## BƯỚC 4 – PHÂN LOẠI TƯỜNG THEO VỊ TRÍ

| Vị trí | Vật liệu thường gặp | Xác nhận |
|--------|---------------------|---------|
| Tường NGOÀI (bắc/đông/tây) | ŽB obvodová | Không có pixel đỏ |
| Tường NAM (phân cách hành lang) | TEHLA priečka | Có pixel đỏ |
| Vách ngăn giữa phòng | TEHLA priečka | Có pixel đỏ |
| Vách WC/Kúpeľňa bên trong | TEHLA nhẹ 100mm | Có pixel đỏ nhạt |
| Tường ZTI (ống nước) | Sadrokartón | Màu xanh/trắng |
| Thang máy/schodisko | ŽB | Không có pixel đỏ |

---

## BƯỚC 4b – CHIỀU CAO VÀ OPENINGS

**Không được dùng h = 3,000 m mặc định.**  
Đọc `S.H.` từng phòng trong bản vẽ → `Výška = S.H. − výška podlahy`  
Đọc kích thước otvor từ dimension line hoặc výkaz dverí.  
**Chi tiết đầy đủ → `references/wall-height-openings.md`**

Nếu không tìm thấy S.H. hoặc không đọc được kích thước cửa → ⛔ `references/stop-and-ask.md`

---

## BƯỚC 5 – TƯỜNG CHUNG (SHARED WALLS)

- Áp dụng **Metóda 2**: mỗi phòng tính đầy đủ, tường chung tính trong cả 2 phòng
- Đánh dấu `[1]` = lần đầu (tham chiếu), `[2]` = lần hai (duplicate, không cộng vào tổng phòng)
- Subtotal chỉ cộng các dòng `[1]` và dòng không có shared flag

---

## BƯỚC 6 – TÍNH DIỆN TÍCH (Phương pháp A)

```
Čistá plocha = (Dĺžka × Výška) − Σ (šírka_otvoru × výška_otvoru)
```

- Trừ **toàn bộ** diện tích otvor — không có ngưỡng tối thiểu
- Kích thước otvoru ≠ kích thước cánh cửa — luôn dùng kích thước **otvoru**
- Formula Excel: `=E{row}-F{row}` (**KHÔNG** phải `=F{row}-G{row}` — self-reference!)

---

## BƯỚC 7 – XUẤT EXCEL (tiếng Slovak)

| Cột | Nội dung | Ghi chú |
|-----|---------|---------|
| A | Wall ID (W-A1-1) | |
| B | Popis / umiestnenie | |
| C | Dĺžka (m) | |
| D | Výška (m) | Từ S.H., không phải 3,000 |
| E | Hrubá plocha (m²) | =C×D |
| F | Odpočet otvorov (m²) | Từ dimension line/výkaz |
| G | **Čistá plocha (m²)** | =E-F |
| H | Spoločná stena [1]/[2] | |
| I | Poznámka / zdroj | Ghi nguồn mọi giá trị |

**Màu dòng:** 🟢 `#E2EFDA` = TEHLA ✅ | 🔴 `#FCE4D6` = ŽB ❌ | 🟡 `#FFF2CC` = Shared [1] | 🍑 `#FFDAB9` = Shared [2]

**Cảnh báo bắt buộc trong mọi file:**
> *"Rozmery boli odčítané z PDF dokumentácie. Odporúčame overiť s originálnym DWG súborom pred realizáciou a platbou."*

---

## BƯỚC 8 – XUẤT PDF OVERLAY

```python
COLOR_MAP = {  # RGBA, alpha=150
    "tehla":    (25,  70, 190, 150),  # xanh dương
    "shared_1": (230, 170,  0, 150),  # vàng
    "shared_2": (220,  40, 40, 150),  # đỏ (dup)
    "check":    (30,  160, 80, 150),  # xanh lá
}
# Không tô màu lên tường ŽB/betón
# Tọa độ phải từ pixel scan, không ước lượng
```

---

## NGÔN NGỮ OUTPUT – BẮT BUỘC

Mọi file output (Excel, PDF, sơ đồ) dùng **tiếng Slovak**.

| Khái niệm | Slovak |
|-----------|--------|
| Diện tích thô | Hrubá plocha |
| Diện tích trừ cửa | Odpočet otvorov |
| Diện tích sạch | Čistá plocha |
| Chiều dài / cao / dày | Dĺžka / Výška / Hrúbka |
| Tổng cộng / Medzisúčet | Celkový súčet / Medzisúčet |
| Tường chung | Spoločná stena |
| Ghi chú | Poznámka |
| Tường ngoài / Vách ngăn | Obvodová stena / Priečka |

**Tên file output** (trong thư mục cùng tên với file input — xem BƯỚC 0):
```
<ten_file_input>/Vykaz_Tehloveho_Muriva_1NP.xlsx
<ten_file_input>/Vykaz_Tehloveho_Muriva_Schema_1NP.pdf
```

---

## CHECKLIST TRƯỚC KHI XUẤT

- [ ] Đã đọc LEGENDA MATERIÁLOV, hiểu ký hiệu tehla vs ŽB
- [ ] Đã xác nhận scale từ dimension line thực tế
- [ ] Đã xem grid debug, tọa độ khớp với bản vẽ
- [ ] Đã dùng `is_tehla_wall()` với `pad=15` cho từng tường
- [ ] Đã xem visual crop ít nhất 3–5 tường đại diện
- [ ] Tường BẮC/ĐÔNG/TÂY ngoài → ŽB, không tính
- [ ] Đã đọc S.H. từng phòng (không dùng 3,000 m mặc định)
- [ ] Đã đọc kích thước otvor từ bản vẽ (không giả định)
- [ ] Đã đánh dấu tường chung [1]/[2]
- [ ] Formula Excel là `=E-F`, không phải `=F-G`
- [ ] Mọi giá trị do người dùng xác nhận được ghi trong Poznámka
- [ ] File output bằng tiếng Slovak
- [ ] Có cảnh báo DWG trong file

---

## CÁC LỖI PHỔ BIẾN

| Lỗi | Nguyên nhân | Hậu quả | Phòng tránh |
|-----|------------|---------|------------|
| Tính tường ŽB vào tehla | Không đọc legend, giả định 300mm = tehla | Sai >50% diện tích | Luôn đọc legend, dùng pixel scan |
| Tọa độ overlay lệch | Ước lượng tọa độ từ mm | Overlay sai vị trí hoàn toàn | Pixel scan + grid debug |
| Self-reference formula | `G=F-G` thay vì `G=E-F` | 67 lỗi #VALUE! | Netto = Gross(E) − Deduct(F) |
| Tường chung cộng 2 lần | Không đánh dấu [2] | Tổng dư ~65 m² | Subtotal chỉ cộng [1] |
| Chiều cao mặc định 3,000 m | Không đọc S.H. | Sai diện tích mọi tường | Đọc S.H. từng phòng |
| Kích thước cửa giả định | Không đọc dimension line | Sai phần trừ opening | Đọc otvor từ bản vẽ |
| Nhầm Hranice với tehla | Pixel cam bị tính là đỏ | Tính thêm đường ranh giới | Dùng `red_poziar` filter |
| Nhầm sadrokartón ZTI | Không phân biệt predsteny | Tính dư ống kỹ thuật | Sadrokartón = xanh/trắng, không đỏ |

---

## GHI CHÚ CUỐI

> **Dữ liệu xuất từ skill này dùng để tính tiền công cho nhân viên.**  
> Sai số ±50–100 mm/tường khi đọc từ PDF → ±0,15–0,30 m²/tường.  
> Nếu dự án lớn hoặc giá trị cao → yêu cầu file DWG để đo chính xác hơn.
