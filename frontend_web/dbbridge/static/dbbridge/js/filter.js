

  document.querySelectorAll('form select, form input').forEach(el => {
    el.addEventListener('change', () => {
      el.form.submit();
    });
  });


  const searchInput = document.querySelector('input[name="name"]');
  if (searchInput) {
    let timeout = null;
    searchInput.addEventListener('input', () => {
      clearTimeout(timeout);
      timeout = setTimeout(() => {
        searchInput.form.submit();
      }, 500);
    });
  }


  document.querySelectorAll('.bookmark-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      const target = document.getElementById(tab.dataset.target);
      document.querySelectorAll('.filter-panel').forEach(panel => {
        panel.style.display = panel === target && panel.style.display !== 'block' ? 'block' : 'none';
      });
    });
  });