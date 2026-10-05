(() => {
  const list = document.getElementById('news-list');
  const more = document.getElementById('news-more');
  if (!list || !more) return;
  const items = Array.from(list.children);
  let visible = 3;
  const update = () => {
    items.forEach((item, index) => { item.hidden = index >= visible; });
    more.hidden = visible >= items.length;
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
  update();
})();
