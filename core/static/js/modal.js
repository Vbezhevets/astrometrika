document.addEventListener("DOMContentLoaded", function () {
  console.log('modal.js loaded');

  const modal = document.getElementById('paymentModal');
  if (!modal) return;

  const closeBtn = modal.querySelector('.close-button');
  const manualBtn = document.getElementById('manualDetailsButton');
  const manualDetails = document.getElementById('manualDetails');


  if (window.location.hash === '#paymentModal') {
    modal.classList.add('show');
    if (window.history.replaceState) {
      window.history.replaceState(null, null, window.location.pathname);
    }
  }


  closeBtn?.addEventListener('click', () => modal.classList.remove('show'));


  window.addEventListener('click', (e) => {
    if (e.target === modal) {
      modal.classList.remove('show');
    }
  });


  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal.classList.contains('show')) {
      modal.classList.remove('show');
    }
  });


  manualBtn?.addEventListener('click', () => {
    manualDetails.style.display = 'block';
  });


  document.addEventListener('click', function (e) {
    if (e.target.classList.contains('copy-btn')) {
      const text = e.target.getAttribute('data-copy');
      navigator.clipboard.writeText(text).then(() => {
        e.target.textContent = '✅';
        setTimeout(() => {
          e.target.textContent = '📋';
        }, 1500);
      });
    }
  });
});