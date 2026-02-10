import typer
from pathlib import Path
from typing_extensions import Annotated

from . import exporter
from . import browser
from . import utils
from . import scroller


app = typer.Typer(
    name="sidekick-pdf-exporter",
    help="Ekspor dokumen College Sidekick ke format PDF.",
    add_completion=False,
    rich_markup_mode="rich"
)


@app.command()
def main(
    url: Annotated[str, typer.Argument(
        help="URL dokumen College Sidekick yang akan diproses.",
    )],
    output: Annotated[Path, typer.Option(
        "--output", "-o",
        help="Path output PDF (default: document.pdf di direktori kerja saat ini).",
        writable=True,
        resolve_path=True,
    )] = Path("document.pdf"),
    headless: Annotated[bool, typer.Option(
        "--headless/--no-headless",
        help="Menjalankan browser dalam mode headless (tanpa GUI) untuk performa lebih cepat.",
    )] = True,
):
    log = utils.setup_logger()
    driver = None

    try:
        log.info(f"Memulai proses untuk URL: [link={url}]{url}[/link]", extra={"markup": True})

        log.info("Mempersiapkan browser...")
        driver = browser.setup_driver(headless=headless)
        if not driver:
            raise RuntimeError("Gagal menginisialisasi WebDriver. Proses dihentikan.")

        log.info(f"Mengakses URL...")
        driver.get(url)

        page_count = scroller.scroll_to_bottom(driver, log)

        if page_count > 0:
            pdf_data = exporter.export_to_pdf(driver, log)
            exporter.save_pdf(pdf_data, str(output), log)
        else:
            log.warning("Tidak ada halaman yang berhasil dimuat, proses pembuatan PDF dilewati.")
    except Exception as e:
        log.error(f"Terjadi kesalahan yang tidak terduga: {e}", extra={"markup": True})
        raise typer.Exit(code=1)
    
    finally:
        if driver:
            log.info("Menutup browser...")
            try:
                driver.quit()
            except Exception:
                log.warning("Gagal menutup browser secara normal. Mungkin koneksi sudah terputus.")


if __name__ == "__main__":
    app()