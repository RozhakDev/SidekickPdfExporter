import base64
import os
from selenium.webdriver.remote.webdriver import WebDriver
from rich.console import Console
from rich.panel import Panel


def export_to_pdf(driver: WebDriver, log):
    log.info("Membersihkan halaman dengan memanipulasi DOM...")
    try:
        javascript_cleaner = """
            const body = document.body;
            const pageContainers = document.querySelectorAll("div[data-testid='page-container']");
            if (pageContainers.length === 0) {
                return false;
            }
            body.innerHTML = '';
            pageContainers.forEach(page => { body.appendChild(page); });
            return true; // Sukses
        """
        success = driver.execute_script(javascript_cleaner)
        if not success:
            log.error("Tidak ditemukan 'page-container' untuk diekspor. Proses cetak dibatalkan.")
            return None
        
        log.info("Membuat PDF dari konten yang sudah bersih...")
        result = driver.execute_cdp_cmd("Page.printToPDF", {
            "landscape": False,
            "displayHeaderFooter": False,
            "printBackground": True,
            "preferCSSPageSize": True,
        })
        return base64.b64decode(result['data'])
    except Exception as e:
        log.error(f"Gagal saat membersihkan halaman atau mencetak PDF: {e}", extra={"markup": True})
        return None


def save_pdf(pdf_bytes: bytes, output_path: str, log):
    if not pdf_bytes:
        log.warning("Tidak ada data PDF untuk disimpan.")
        return
    try:
        with open(output_path, "wb") as f:
            f.write(pdf_bytes)

        console = Console()
        absolute_path = os.path.abspath(output_path)
        success_message = (
            f"[bold green]🎉 SELAMAT! PROSES SELESAI SEMPURNA 🎉[/bold green]\n\n"
            f"File PDF lengkap berhasil disimpan di: [cyan]{absolute_path}[/cyan]"
        )
        console.print(
            Panel(
                success_message,
                title="[bold yellow]Ekspor Berhasil[/bold yellow]",
                border_style="green",
                padding=(1, 2)
            )
        )
    except IOError as e:
        log.error(f"Gagal menyimpan file PDF: {e}", extra={"markup": True})