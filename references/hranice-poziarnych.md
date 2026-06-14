# Hranice požiarnych úsekov – Phân biệt với TEHLA

## Vấn đề: Đường ranh giới chống cháy có pixel đỏ/cam → dễ nhầm là tehla

| Đặc điểm | TEHLA (hatch đỏ) | Hranice požiarnych úsekov |
|-----------|-----------------|--------------------------|
| Pattern | Hatch chéo đặc, liên tục | Đường đứt nét `–·–·–·` mảnh |
| Màu | Đỏ đậm `R>160, G<80, B<80` | Cam nhạt `R>180, G>80<140, B<60` |
| Chiều dày | Bằng chiều dày tường (10–30px) | Rất mảnh (1–3px) |
| Liên tục? | Solid fill | Dash-dot pattern |
| Vị trí | Bên trong tường (fill) | Dọc theo ranh giới phòng/khu vực |

## Code phân biệt:

```python
red_tehla  = np.sum((r[:,:,0]>160) & (r[:,:,1]<80)  & (r[:,:,2]<80))
red_poziar = np.sum((r[:,:,0]>180) & (r[:,:,1]>80)  & (r[:,:,1]<140) & (r[:,:,2]<60))

# Chỉ là TEHLA nếu đỏ đậm >> cam ranh giới
if red_tehla > 15 and red_tehla > red_poziar * 2:
    return True, "TEHLA"
if red_poziar > red_tehla:
    return False, "Hranice požiarnych úsekov – KHÔNG PHẢI TEHLA"
```

## Nhận biết bằng mắt:
- **Đường mảnh, đứt quãng, màu cam** → hranice, bỏ qua
- **Vùng tô đặc, chéo chéo, màu đỏ** → tehla ✅
