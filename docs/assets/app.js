(() => {
  const cards = [...document.querySelectorAll('.card')];
  const search = document.querySelector('#search');
  const filters = [...document.querySelectorAll('[data-category]')];
  let category = '全部';
  function filter() {
    const term = search.value.trim().toLocaleLowerCase();
    let count = 0;
    cards.forEach(card => {
      const match = (category === '全部' || card.dataset.group === category) && card.textContent.toLocaleLowerCase().includes(term);
      card.hidden = !match; count += Number(match);
    });
    document.querySelector('#count').textContent = `${count} 篇筆記`;
    document.querySelector('#empty').hidden = count > 0;
  }
  if (search) {
    search.addEventListener('input', filter);
    filters.forEach(button => button.addEventListener('click', () => {
      category = button.dataset.category;
      filters.forEach(b => b.setAttribute('aria-pressed', String(b === button)));
      filter();
    }));
  }
  const checks = [...document.querySelectorAll('[data-check]')];
  const status = document.querySelector('#check-status');
  let storageOK = true;
  const key = 'study-notes:v1:' + (document.querySelector('article')?.dataset.slug || '');
  let saved = [];
  try { const parsed = JSON.parse(localStorage.getItem(key) || '[]'); if (Array.isArray(parsed)) saved = parsed; } catch { storageOK = false; }
  function update() { if(status) status.textContent = `已勾選 ${checks.filter(c => c.checked).length} / ${checks.length} 項${storageOK ? ' · 僅儲存於此瀏覽器' : ' · 此瀏覽器無法保存，重新整理會重設'}`; }
  checks.forEach(input => {
    input.checked = saved.includes(input.dataset.check);
    input.addEventListener('change', () => {
      try { localStorage.setItem(key, JSON.stringify(checks.filter(c => c.checked).map(c => c.dataset.check))); } catch { storageOK = false; }
      update();
    });
  });
  update();
})();
