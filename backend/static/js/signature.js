function initializeSignaturePage(email) {
    const documentLinks = document.querySelectorAll('.document-link');
    const pdfFrame = document.getElementById('pdf-frame');
    const nextDocButton = document.getElementById('next-doc');
    const signButton = document.getElementById('sign-btn');
    let currentDocIndex = 0;
  
    documentLinks.forEach((link, index) => {
      link.addEventListener('click', (event) => {
        event.preventDefault();
        pdfFrame.src = link.dataset.url;
        currentDocIndex = index;
        if (index === documentLinks.length - 1) {
          nextDocButton.disabled = true;
          signButton.disabled = false;
        } else {
          nextDocButton.disabled = false;
          signButton.disabled = true;
        }
      });
    });
  
    nextDocButton.addEventListener('click', () => {
      if (currentDocIndex < documentLinks.length - 1) {
        currentDocIndex++;
        pdfFrame.src = documentLinks[currentDocIndex].dataset.url;
        if (currentDocIndex === documentLinks.length - 1) {
          nextDocButton.disabled = true;
          signButton.disabled = false;
        }
      }
    });
  
    signButton.addEventListener('click', () => {
      fetch('/api/v1/signe/send_otp', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          'email': email
        })
      }).then(response => {
        if (response.ok) {
          $('#otpModal').modal('show');
        } else {
          alert('Failed to send OTP');
        }
      });
    });
  
    document.getElementById('otp-form').addEventListener('submit', (event) => {
      event.preventDefault();
      const otp = document.getElementById('otp-input').value;
      fetch('/api/v1/signe/verify_otp', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          'email': email,
          'otp': otp
        })
      }).then(response => {
        if (response.ok) {
          alert('Document signed successfully');
          $('#otpModal').modal('hide');
        } else {
          alert('Failed to verify OTP');
        }
      });
    });
  }
  