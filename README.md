# Sidekick PDF Exporter

Minimal CLI tool untuk **mengunduh dan mengekspor dokumen College Sidekick ke format PDF** menggunakan Selenium WebDriver.

## Fitur

- CLI sederhana dengan pengelolaan WebDriver otomatis
- Ekspor dokumen College Sidekick ke **PDF**
- Mendukung **mode headless / non-headless**

## Prasyarat

* **Python 3.10+**
* **Google Chrome** terpasang
* **Poetry**

## Instalasi & Penggunaan

Clone repositori ini, lalu instal dependensi menggunakan Poetry:

```bash
git clone https://github.com/RozhakDev/SidekickPdfExporter.git
cd SidekickPdfExporter
poetry install
````

Jalankan CLI dengan perintah berikut:

```bash
poetry run sidekick-pdf-exporter <URL> [OPTIONS]
```

Contoh:

```bash
poetry run sidekick-pdf-exporter https://www.collegesidekick.com/study-docs/XXXXXX --no-headless
```

## Opsi CLI

| Opsi            | Deskripsi                                      |
| --------------- | ---------------------------------------------- |
| `URL`           | URL dokumen College Sidekick                   |
| `--output PATH` | Path file output PDF *(default: document.pdf)* |
| `--no-headless` | Menjalankan browser dengan GUI                 |

## Catatan Teknis

* Tool ini menggunakan **Selenium WebDriver** karena konten College Sidekick dirender via JavaScript.
* Mode headless direkomendasikan untuk penggunaan otomatis.

## Lisensi

MIT License