document.addEventListener("DOMContentLoaded", function () {
  const bookingForm = document.getElementById('bookingForm');
  const confirmation = document.getElementById('confirmationMessage');

  if (!bookingForm) return;

  bookingForm.addEventListener('submit', function (e) {
    e.preventDefault();

    const formData = {
      fullName: bookingForm.fullName.value,
      email: bookingForm.email.value,
      birthDate: bookingForm.birthDate.value,
      birthTime: bookingForm.birthTime.value,
      birthPlace: bookingForm.birthPlace.value,
      focusArea: bookingForm.focusArea.value
    };

    fetch("/send_booking_request/", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      body: JSON.stringify(formData)
    })
      .then(response => {
        if (!response.ok) throw new Error('Network error');
        return response.json();
      })
      .then(data => {
        if (data.status === 'ok') {
          bookingForm.reset();
          confirmation.style.display = 'block';
          const modal = document.getElementById('paymentModal');
          modal.classList.add('show');
        }
      })
      .catch(error => {
        alert('An error occurred: ' + error.message);
      });
  });

 function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  const focusAreaInput = document.getElementById('focusArea');
  const charCountDisplay = document.getElementById('charCount');

  if (focusAreaInput) {
    focusAreaInput.addEventListener('input', function () {
      const length = focusAreaInput.value.length;
      charCountDisplay.textContent = `${length} / 1000 characters`;
    });
  }
});