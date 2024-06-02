function initializeSignaturePage(email, signatureRequestId) {
  const documentLinks = document.querySelectorAll('.document-link');
  const pdfFrame = document.getElementById('pdf-frame');
  const nextDocButton = document.getElementById('next-doc');
  const prevDocButton = document.getElementById('prev-doc');
  const signButton = document.getElementById('sign-btn');
  const emailInput = document.getElementById('otp-email-input');
  const otpInput = document.getElementById('otp-input');
  const sendOtpBtn = document.getElementById('send-otp-btn');
  const verifyOtpBtn = document.getElementById('verify-otp-btn');
  let currentDocIndex = 0;
  let viewedDocs = new Set();
  let allScrolledToEnd = true;

  // Initial Load
  updateDocumentDisplay(currentDocIndex);

  documentLinks.forEach((link, index) => {
    link.addEventListener('click', (event) => {
      event.preventDefault();
      updateDocumentDisplay(index);
    });
  });

  nextDocButton.addEventListener('click', () => {
    if (currentDocIndex < documentLinks.length - 1) {
      updateDocumentDisplay(++currentDocIndex);
    }
  });

  prevDocButton.addEventListener('click', () => {
    if (currentDocIndex > 0) {
      updateDocumentDisplay(--currentDocIndex);
    }
  });

  function updateDocumentDisplay(index) {
    pdfFrame.src = documentLinks[index].dataset.url;
    currentDocIndex = index;
    viewedDocs.add(index);

    nextDocButton.disabled = index === documentLinks.length - 1;
    prevDocButton.disabled = index === 0;
    pdfFrame.onload = function() {
      checkScrollToEnd(this);
    }

    checkAllDocumentsViewed();
  }

  function checkAllDocumentsViewed() {
    signButton.disabled = viewedDocs.size !== documentLinks.length || !allScrolledToEnd;
  }

  signButton.addEventListener('click', () => {
    resetModal();
    $('#otpModal').modal('show');
  });

  sendOtpBtn.addEventListener('click', () => {
    sendOtpBtn.disabled = true; // Disable the button to prevent multiple clicks
    fetch('/api/v1/signe/send_otp', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
        'email': emailInput.value,
        'signature_request_id': signatureRequestId
      })
    }).then(response => {
      sendOtpBtn.disabled = false; // Re-enable the button
      if (response.ok) {
        alert('OTP sent successfully');
        otpInput.disabled = false;
        verifyOtpBtn.disabled = false;
      } else {
        alert('Failed to send OTP');
      }
    });
  });

  $('#otpModal').on('shown.bs.modal', function () {
    resetModal(); // Reset modal when opened
  });

  document.getElementById('otp-form').addEventListener('submit', (event) => {
    event.preventDefault();
    verifyOtpBtn.disabled = true; // Disable the button during request
    fetch('/api/v1/signe/verify_otp', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
        'email': emailInput.value,
        'otp': otpInput.value,
        'signature_request_id': signatureRequestId
      })
    }).then(response => {
      verifyOtpBtn.disabled = false; // Re-enable the button
      if (response.ok) {
        alert('Document signed successfully');
        $('#otpModal').modal('hide');
        resetModal();
      } else {
        alert('Failed to verify OTP');
      }
    });
  });

  function resetModal() {
    otpInput.value = ''; // Clear the OTP input
    otpInput.disabled = true; // Disable the OTP input until new OTP is sent
    verifyOtpBtn.disabled = true; // Disable verify button until OTP is entered
  }
}
