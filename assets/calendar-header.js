(() => {
  const region = document.querySelector('.course-schedule');
  const table = region?.querySelector('.course-calendar');
  const head = table?.tHead;
  if (!head) return;

  // La copia visiva segue la pagina anche dentro il contenitore orizzontale.
  // L'intestazione originale conserva le associazioni accessibili con le celle.
  const floating = document.createElement('div');
  floating.className = 'course-schedule calendar-sticky-header';
  floating.setAttribute('aria-hidden', 'true');
  floating.hidden = true;
  const copy = table.cloneNode(false);
  copy.classList.remove('course-calendar');
  copy.removeAttribute('id');
  const copiedHead = head.cloneNode(true);
  copiedHead.querySelectorAll('[id]').forEach(node => node.removeAttribute('id'));
  copy.append(copiedHead);
  floating.append(copy);
  document.body.append(floating);

  const cells = Array.from(head.querySelectorAll('th'));
  const copiedCells = Array.from(copiedHead.querySelectorAll('th'));
  const pageHeader = document.getElementById('quarto-header');
  let pending = false;
  let sizesDirty = true;

  function update() {
    pending = false;
    const tableBox = table.getBoundingClientRect();
    const headBox = head.getBoundingClientRect();
    const regionBox = region.getBoundingClientRect();
    const top = Math.max(0, pageHeader?.getBoundingClientRect().bottom || 0);
    floating.hidden = headBox.top >= top || tableBox.bottom <= top;
    if (floating.hidden) return;

    if (sizesDirty) {
      cells.forEach((cell, index) => {
        copiedCells[index].style.width = `${cell.getBoundingClientRect().width}px`;
        copiedCells[index].style.textAlign = getComputedStyle(cell).textAlign;
      });
      sizesDirty = false;
    }
    floating.style.top = `${Math.min(top, tableBox.bottom - headBox.height)}px`;
    floating.style.left = `${regionBox.left + region.clientLeft}px`;
    floating.style.width = `${region.clientWidth}px`;
    copy.style.width = `${tableBox.width}px`;
    copy.style.transform = `translateX(${tableBox.left - regionBox.left - region.clientLeft}px)`;
  }

  function schedule() {
    if (pending) return;
    pending = true;
    requestAnimationFrame(update);
  }

  function resize() {
    sizesDirty = true;
    schedule();
  }

  window.addEventListener('scroll', schedule, { passive: true });
  region.addEventListener('scroll', schedule, { passive: true });
  window.addEventListener('resize', resize);
  pageHeader?.addEventListener('transitionend', schedule);
  const observer = new ResizeObserver(resize);
  [region, table, document.body, pageHeader].filter(Boolean).forEach(node => observer.observe(node));
  document.fonts.ready.then(resize);
  schedule();
})();
