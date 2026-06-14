# Mẫu câu hỏi khi dừng lại – Nguyên tắc ⛔

**Dữ liệu này dùng để tính tiền công nhân viên. Tính sai còn nguy hiểm hơn dừng lại hỏi.**

## 7 tình huống BẮT BUỘC dừng lại

| # | Tình huống | KHÔNG được làm |
|---|-----------|---------------|
| 1 | Ký hiệu vật liệu không rõ (pixel đỏ thấp, không khớp legend) | Giả định tehla hoặc ŽB |
| 2 | Không tìm thấy `S.H.` cho phòng đó | Dùng 3,000 m mặc định |
| 3 | Không đọc được kích thước otvor cửa/cửa sổ | Dùng kích thước giả định |
| 4 | Không xác định được hrúbka (độ dày) | Giả định 200 hoặc 300 mm |
| 5 | Bản vẽ mờ, ký hiệu chồng lên nhau | Đoán theo vị trí |
| 6 | Tường nằm ở ranh giới hai khu vực vật liệu khác nhau | Lấy một trong hai |
| 7 | Ký hiệu không xuất hiện trong legend | Bỏ qua hoặc tự phân loại |

## Cấu trúc câu hỏi bắt buộc – luôn nêu rõ 5 yếu tố:

```
⛔ Không xác định được [THÔNG SỐ]:

  Phòng:    [Tên phòng + mã, VD: OV-A3 (E1.02b)]
  Ký hiệu:  [Wall ID, VD: W-A3-4]
  Vị trí:   [Mô tả chính xác: góc nào, giáp phòng nào, gần lưới cột nào]
  Vấn đề:   [Mô tả cụ thể tại sao không xác định được]

  Các lựa chọn:
  a) ...
  b) ...
```

## Khi có nhiều thông số chưa rõ – hỏi một lần duy nhất:

```
⛔ CẦN XÁC NHẬN TRƯỚC KHI TÍNH – [X] thông số chưa rõ:

| # | Phòng / Tường   | Vị trí              | Vấn đề         |
|---|----------------|---------------------|----------------|
| 1 | W-A3-4 / OV-A3 | Vách đông, giáp A4  | Tehla hay ŽB?  |
| 2 | W-WC / E1.05   | Góc tây-nam         | S.H. = ? m     |
| 3 | W-A2-4 / OV-A2 | Vách đông, giáp A3  | Otvor š×v = ?  |
```

## Ghi trong Poznámka sau khi nhận xác nhận:

```
"Hrúbka 150 mm – potvrdené užívateľom (nie z výkresu)"
"S.H. = 2,610 m – prevzaté z E1.07, S.H. pre E1.05 nenájdené"
"Otvor 900×2120 – potvrdené užívateľom"
```
