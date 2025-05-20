document.addEventListener("DOMContentLoaded", function () {
  console.log('modal.js loaded');

  const modal = document.getElementById('paymentModal');
  const closeBtn = modal?.querySelector('.close-button');
  const editBtn = document.getElementById('editForm');
  const proceedBtn = document.getElementById('proceedPayment');
  const bookingSection = document.getElementById('booking');

  if (!modal) return;

  closeBtn?.addEventListener('click', () => {
    modal.classList.remove('show');
    bookingSection?.scrollIntoView({ behavior: 'smooth' });
  });

  window.addEventListener('click', (e) => {
    if (e.target === modal) {
      modal.classList.remove('show');
      bookingSection?.scrollIntoView({ behavior: 'smooth' });
    }
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal.classList.contains('show')) {
      modal.classList.remove('show');
      bookingSection?.scrollIntoView({ behavior: 'smooth' });
    }
  });

  editBtn?.addEventListener('click', () => {
    modal.classList.remove('show');
    bookingSection?.scrollIntoView({ behavior: 'smooth' });
  });

  proceedBtn?.addEventListener('click', () => {
    const checkoutUrl = window.CHECKOUT_URL || "/create-checkout-session/";

    fetch(checkoutUrl, {
      method: "POST",
      body: new FormData(document.getElementById("bookingForm"))
    })
    .then(res => {
      if (!res.ok) {
        return res.text().then(text => {
          console.error("❌ Server returned error HTML:", text);
          throw new Error(`Server error ${res.status}`);
        });
      }
      return res.json();
    })
    .then(data => {
      console.log("✅ Ответ от сервера:", data);
      if (data.checkout_url) {
        window.location.href = data.checkout_url;
      } else {
        console.error("⚠️ checkout_url не пришёл:", data);
        alert("Ошибка: не удалось создать ссылку для оплаты.");
      }
    })
    .catch(err => {
      console.error("💥 Fetch ошибка:", err);
      alert("Произошла ошибка. Попробуйте позже.");
    });
  });
});