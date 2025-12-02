import os
import shutil
import zipfile

# === CẤU HÌNH ===
pack1_zip = "Fast-Better-Grass.zip"    # đường dẫn pack 1
pack2_zip = "Midnighttiggers-FCT-Default_1.20_V8.zip"    # đường dẫn pack 2
output_zip = "merged_pack.zip"  # tên file zip cuối cùng
temp_dir = "temp_merge"

# === BƯỚC 1: Tạo folder tạm ===
if os.path.exists(temp_dir):
    shutil.rmtree(temp_dir)
os.makedirs(temp_dir)

# === BƯỚC 2: Giải nén cả 2 pack ===
for pack_zip in [pack1_zip, pack2_zip]:
    with zipfile.ZipFile(pack_zip, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)

# === BƯỚC 3: Đảm bảo chỉ còn 1 pack.mcmeta ===
# ưu tiên giữ pack1.mcmeta, xóa pack2.mcmeta nếu trùng
pack_mcmeta_path = os.path.join(temp_dir, "pack.mcmeta")
if not os.path.exists(pack_mcmeta_path):
    # nếu pack1 không có, lấy từ pack2
    for f in os.listdir(temp_dir):
        if f.lower() == "pack.mcmeta":
            shutil.move(os.path.join(temp_dir, f), pack_mcmeta_path)

# === BƯỚC 4: Zip lại ===
with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(temp_dir):
        for file in files:
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, temp_dir)  # giữ cấu trúc
            zipf.write(file_path, arcname)

# === BƯỚC 5: Xong ===
shutil.rmtree(temp_dir)
print(f"✅ Gộp xong, tạo file: {output_zip}")
