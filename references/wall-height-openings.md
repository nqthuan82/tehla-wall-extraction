# Chiều cao tường (S.H.) và Openings (cửa/cửa sổ)

## CHIỀU CAO – Đọc từ bản vẽ, KHÔNG giả định

### Ký hiệu cần tìm trong pôdorys:

| Ký hiệu | Ý nghĩa | Dùng để tính |
|---------|---------|-------------|
| `S.H. = +X,XXX` | Strop Hotový – trần hoàn thiện | ✅ Dùng làm výška tường |
| `H.H. = +X,XXX` | Hrubý strop – trần thô | ❌ Không dùng trực tiếp |
| `T.I. = +X,XXX` | Top of Insulation | ❌ Tham khảo |
| `±0,000` / `+0,120` | Cao độ sàn phòng | Trừ vào S.H. |

### Công thức:
```
Výška steny = S.H. − výška podlahy phòng đó
```

### Ví dụ từ bản vẽ A04A:
| Phòng | Sàn | S.H. | Výška steny |
|-------|-----|------|------------|
| OV-A1 | ±0,000 | +2,520 | **2,520 m** |
| OV-A5 | +0,120 | +2,720 | **2,600 m** |
| E1.07 | ±0,000 | T.I.=+2,610 | **≈2,610 m** |

### Nếu không tìm thấy S.H.: ⛔ DỪNG – xem `stop-and-ask.md`

---

## OPENINGS – Kích thước cửa / cửa sổ

### Phương pháp A (áp dụng): Trừ TOÀN BỘ diện tích otvor, không có ngưỡng tối thiểu.

```
Čistá plocha = (Dĺžka × Výška) − Σ (šírka_otvoru × výška_otvoru)
```

### 4 nguồn đọc kích thước – theo thứ tự ưu tiên:

**1. Dimension line trực tiếp cạnh cửa trong pôdorys** ← chính xác nhất
```
900 × 2120 mm → 0,900 × 2,120 = 1,908 m²
```

**2. Výkaz dverí / okien** (bảng schedule dưới pôdorys)
```
| D1 | Revízne dvierka 400×400 mm | 1 ks |
```

**3. Bảng ÚK – STAV. ÚPR.** (lỗ kỹ thuật trong tường tehla)
```
| ZTI13e | PRESTUP V TEHLOVEJ PRIEČKE HR. 100 mm | Ø200 |
```
→ Chỉ trừ nếu Ø > 150 mm hoặc rozmer > 200×200 mm

**4. Bảng VZT – STAV. ÚPR.** (lỗ thông gió trong tường tehla)
```
| VZT13d | PRESTUP V TEHLOVEJ PRIEČKE HR. 150 mm | 350×550 |
```
→ 350×550 = 0,19 m² — phải trừ

### Phân biệt loại opening:

| Ký hiệu trong pôdorys | Loại | Trừ? |
|-----------------------|------|------|
| Cung tròn (door swing) | Dvere (cửa đi) | ✅ |
| 3 đường song song trong tường | Okno (cửa sổ) | ✅ |
| Hình chữ nhật nhỏ, không cung | Revízne dvierka | ✅ nếu trong tehla |
| Ký hiệu Ø tròn > 150 mm | Prestup ZTI/VZT | ✅ |
| Ký hiệu Ø tròn ≤ 150 mm | Kabel/potrubie nhỏ | ❌ |

### Lưu ý quan trọng:
- Kích thước trong bản vẽ = kích thước **OTVORU** (lỗ trong tường), không phải cánh cửa
- Otvor 900×2120 mm ≠ krídlo 860×2070 mm — luôn dùng kích thước otvor
- Cửa nằm một phần trong ŽB, một phần trong tehla → ⛔ DỪNG – xem `stop-and-ask.md`

### Ghi trong Poznámka Excel:
```
"Odpočet: okno 1760×1500 = 2,640 m² (z výkazu okien A04A)"
"Odpočet: dvere 900×2120 = 1,908 m² (z pôdorysu A04A)"
"ZTI13e Ø200 = 0,031 m² – nezapočítané (< 0,05 m²)"
```
