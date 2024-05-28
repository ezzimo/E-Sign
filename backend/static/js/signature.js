function initializeSignaturePage(email, signatureRequestId) {
    const documentLinks = document.querySelectorAll('.document-link');
    const pdfFrame = document.getElementById('pdf-frame');
    const nextDocButton = document.getElementById('next-doc');
    const signButton = document.getElementById('sign-btn');
    let currentDocIndex = 0;
    let viewedDocs = new Set();
  
    documentLinks.forEach((link, index) => {
      link.addEventListener('click', (event) => {
        event.preventDefault();
        pdfFrame.src = link.dataset.url;
        currentDocIndex = index;
        viewedDocs.add(index);
  
        if (index === documentLinks.length - 1) {
          nextDocButton.disabled = true;
          if (viewedDocs.size === documentLinks.length) {
            signButton.disabled = false;
          }
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
        viewedDocs.add(currentDocIndex);
  
        if (currentDocIndex === documentLinks.length - 1) {
          nextDocButton.disabled = true;
          if (viewedDocs.size === documentLinks.length) {
            signButton.disabled = false;
          }
        }
      }
    });
  
    signButton.addEventListener('click', () => {
      const emailInput = document.getElementById('otp-email-input');
      emailInput.value = email;
      const otpInput = document.getElementById('otp-input');
      const sendOtpBtn = document.getElementById('send-otp-btn');
      const verifyOtpBtn = document.getElementById('verify-otp-btn');
  
      sendOtpBtn.addEventListener('click', () => {
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
          if (response.ok) {
            alert('OTP sent successfully');
            otpInput.disabled = false;
            verifyOtpBtn.disabled = false;
          } else {
            alert('Failed to send OTP');
          }
        });
      });
  
      document.getElementById('otp-form').addEventListener('submit', (event) => {
        event.preventDefault();
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
          if (response.ok) {
            alert('Document signed successfully');
            $('#otpModal').modal('hide');
            documentLinks.forEach((link, index) => {
              const checkIcon = document.createElement('span');
              checkIcon.classList.add('badge', 'bg-success', 'ms-2');
              checkIcon.innerText = '✓';
              if (!link.querySelector('.bg-success')) {
                link.appendChild(checkIcon);
              }
            });
          } else {
            alert('Failed to verify OTP');
          }
        });
      });
  
      $('#otpModal').modal('show');
    });
  }
