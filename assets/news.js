(() => {
  const list = document.getElementById('news-list');
  const more = document.getElementById('news-more');
  const less = document.getElementById('news-less');
  if (!list || !more || !less) return;
  const items = Array.from(list.children);
  const initial = 1;
  let visible = initial;
  const update = () => {
    items.forEach((item, index) => { item.hidden = index >= visible; });
    more.hidden = visible >= items.length;
    less.hidden = visible <= initial;
  };
  more.addEventListener('click', () => {
    const next = items[visible];
    visible += 5;
    update();
    // Quando il pulsante scompare, conserva il punto di lettura da tastiera.
    if (more.hidden && next) {
      next.tabIndex = -1;
      next.focus({ preventScroll: true });
    }
  });
  less.addEventListener('click', () => {
    visible = initial;
    update();
    // Il comando usato scompare: torna al pulsante rimasto visibile.
    more.focus();
  });
  update();
})();
