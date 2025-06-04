# Panduan Deploy Django ke Render

Panduan ini menjelaskan langkah-langkah untuk melakukan deploy project Django Anda ke [Render](https://render.com/) dengan benar.

## 1. Clone Repository

```bash
# Clone project Anda
git clone https://github.com/username/repo-anda.git
cd repo-anda/api
```

## 2. Persiapan Project

- Pastikan folder `img/` dan semua file static/media sudah di-commit ke repository.
- Pastikan file `requirements.txt` sudah lengkap.
- Isi file `build.sh` seperti berikut:

```sh
#!/bin/bash
set -e
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata shoppit/fixtures/products.json
python manage.py collectstatic --noinput
```

- Di `settings.py`, gunakan environment variable untuk data sensitif (sudah disiapkan):
  - `SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', ...)`
  - `DEBUG = os.getenv('RENDER', None) is None`
  - `MEDIA_URL = '/img/'`
  - `MEDIA_ROOT = os.path.join(BASE_DIR, 'img')`

- Di `api/urls.py`, pastikan ada baris berikut:

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

## 3. Buat Web Service Baru di Render

1. Buka [Render Dashboard](https://dashboard.render.com/).
2. Klik **New Web Service**.
3. Hubungkan ke repo GitHub/GitLab Anda.
4. Jika perlu, set root directory ke `api`.
5. Build command:
   ```sh
   ./build.sh
   ```
6. Start command:
   ```sh
   gunicorn api.wsgi:application
   ```
7. Tambahkan environment variable:
   - `DJANGO_SECRET_KEY` (isi dengan secret key Anda)
   - `DATABASE_URL` (jika pakai Postgres)
   - `RENDER=1` (agar DEBUG=False)

## 4. File Static dan Media

- File static akan dikumpulkan ke `staticfiles/` dan dilayani oleh WhiteNoise.
- File media (img/) harus ada di repo atau di-upload ke server.
- Untuk production, sebaiknya gunakan cloud storage (S3, dsb) untuk file media.

## 5. Migrasi dan Data Awal

- Script `build.sh` akan menjalankan migrate dan load data awal dari `shoppit/fixtures/products.json`.

## 6. Akses Aplikasi

- Setelah deploy, aplikasi bisa diakses di URL dari Render.
- Admin: `/admin/`
- API: `/core/`, `/products/`, dll.

## 7. Troubleshooting

- Jika gambar tidak muncul, pastikan folder `img/` ada di repo dan tidak di `.gitignore`.
- Cek shell Render: `ls -l img` untuk memastikan file ada.
- Untuk masalah static/media, cek `settings.py` dan `urls.py`.

---

Untuk info lebih lanjut, lihat [Dokumentasi Render Django](https://render.com/docs/deploy-django) atau tanya di komunitas Render.
