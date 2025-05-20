document.addEventListener("DOMContentLoaded", function () {
  const bookingForm = document.getElementById("bookingForm");

  if (bookingForm) {
    bookingForm.addEventListener("submit", function (e) {
      e.preventDefault();

      const checkedRadio = bookingForm.querySelector('input[name="readingTopic"]:checked');
      const readingTopicValue = checkedRadio?.value || "";
      const readingTopicText = checkedRadio?.nextElementSibling.textContent || "";

      const formData = {
        fullName: bookingForm.fullName.value,
        email: bookingForm.email.value,
        birthDate: bookingForm.birthDate.value,
        birthTime: bookingForm.birthTime.value,
        birthPlace: bookingForm.birthPlace.value,
        focusArea: bookingForm.focusArea.value,
        readingTopic: readingTopicValue
      };


      document.getElementById('summaryFullName').textContent = formData.fullName;
      document.getElementById('summaryEmail').textContent = formData.email;
      document.getElementById('summaryBirthDate').textContent = formData.birthDate;
      document.getElementById('summaryBirthTime').textContent = formData.birthTime;
      document.getElementById('summaryBirthPlace').textContent = formData.birthPlace;
    //   document.getElementById('summaryFocusArea').textContent = formData.focusArea;
      document.getElementById('summaryReadingTopic').textContent = readingTopicText;

      const modal = document.getElementById("paymentModal");
      modal.classList.add("show");
    });
  }
});