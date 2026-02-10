import time
import os

if os.name == 'nt':
    import msvcrt
else:
    msvcrt = None 

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn


def scroll_to_bottom(driver: WebDriver, log):
    log.info("Memulai proses menggulir halaman (mode gulir halus)...")
    if os.name == 'nt':
        log.info("[bold yellow]TIPS:[/ ] Tekan [cyan]ENTER[/] atau [cyan]Q[/] kapan saja untuk berhenti menggulir dan memulai ekspor PDF.")
    
    last_page_count = -1
    interrupted_by_key = False
    
    try:
        while not interrupted_by_key:
            page_elements = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='page-container']")
            current_page_count = len(page_elements)

            if last_page_count == current_page_count:
                if current_page_count == 0:
                    log.error("Tidak ada konten dokumen yang ditemukan. URL mungkin salah atau halaman tidak dapat diakses.")
                else:
                    log.info(f"Jumlah halaman tidak bertambah ([bold yellow]{current_page_count}[/bold yellow]). Proses gulir selesai.")
                break

            log.info(f"Total halaman saat ini: [bold green]{current_page_count}[/bold green]. Menggulir perlahan...")
            last_page_count = current_page_count

            last_height = driver.execute_script("return document.body.scrollHeight")
            scroll_increment = 400
            current_scroll = 0

            with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), BarColumn(), TimeElapsedColumn(), transient=True) as progress:
                scroll_task = progress.add_task("[cyan]Menggulir...", total=last_height)
                while current_scroll < last_height:
                    if msvcrt and msvcrt.kbhit():
                        key = msvcrt.getwch().lower()
                        if key in ['\r', 'q']:
                            log.warning("Tombol berhenti terdeteksi!")
                            interrupted_by_key = True
                            break
                    
                    driver.execute_script(f"window.scrollBy(0, {scroll_increment});")
                    time.sleep(2)

                    current_scroll += scroll_increment
                    new_height = driver.execute_script("return document.body.scrollHeight")

                    if new_height > last_height:
                        last_height = new_height
                        progress.update(scroll_task, total=last_height)
                    progress.update(scroll_task, advance=scroll_increment)
            
            if interrupted_by_key:
                break

            log.info("Sudah mencapai dasar halaman. Memberi jeda untuk konten baru...")
            time.sleep(5)
    except KeyboardInterrupt:
        log.warning("CTRL+C terdeteksi. Menghentikan proses...")
        interrupted_by_key = True
    
    except Exception as e:
        log.error(f"Terjadi kesalahan saat menggulir: {e}", extra={"markup": True})
        return 0

    final_count = 0
    try:
        log.info("Menghitung halaman akhir yang sudah dimuat...")
        page_elements = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='page-container']")
        final_count = len(page_elements)
    except Exception:
        final_count = last_page_count if last_page_count != -1 else 0

    log.info(f"Selesai! Total akhir ditemukan: [bold green]{final_count}[/bold green] halaman.")
    return final_count